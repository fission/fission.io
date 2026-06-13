---
title: "Building a Custom Environment"
draft: false
weight: 40
description: >
  Build or modify a Fission environment: implement the specialize HTTP contract, write the runtime and builder images, test locally, and add a new language.
---

This guide walks through building a Fission environment from scratch, modifying an existing one, and adding support for a brand-new language.
It is the hands-on companion to the [Environments concept guide]({{% ref "/docs/concepts/environments.md" %}}), which explains *what* an environment is; here we cover *how* to build one.

By the end you will understand the runtime HTTP contract every environment must implement, how the optional builder turns source into a deployment package, and the exact files you need to ship a new language.

{{% notice info %}}
The reference implementation for every shipped environment lives in the [fission/environments](https://github.com/fission/environments) repository.
The Python, Node.js, Go, and Rust environments there are the best templates to copy from — this guide refers to them throughout.
{{% /notice %}}

## When you need a custom environment

You need to build or modify an environment when you want to:

- Add a language Fission does not yet ship (the focus of [issue #193](https://github.com/fission/fission.io/issues/193)).
- Pin a different language/runtime version (for example a newer Python or Go base image).
- Bake system libraries, certificates, or shared dependencies into the runtime image.
- Change how source code is compiled or how dependencies are fetched (the builder).

If you only need to *use* an existing environment, you do not need this page — see [Create Environment]({{% ref "environments.en.md" %}}) instead.

## How an environment is structured

An environment is one or two container images:

- A **runtime container** (always required) — an HTTP server that loads your function on demand and then serves invocations.
- A **builder container** (optional) — compiles source code and gathers dependencies, turning a source archive into a runnable deployment archive.

You only need a builder for languages that compile or fetch dependencies.
For interpreted single-file functions, the runtime container alone is enough.
See [How specialization loads your code]({{% ref "/docs/concepts/environments.md" %}}#how-specialization-loads-your-code) for the lifecycle.

## The runtime contract

This is the heart of every environment.
A runtime image is a generic HTTP server that listens on **port 8888** and implements these endpoints:

| Method & path | Purpose |
| --- | --- |
| `GET /healthz` | Readiness/liveness probe. Return `200 OK` once the server is up. |
| `POST /specialize` | **v1 protocol.** Load the user function from the fixed path `/userfunc/user`. No request body. |
| `POST /v2/specialize` | **v2 protocol.** Load the function described by the JSON body `{"filepath": "...", "functionName": "..."}`. `filepath` may be a single file or a built package directory. |
| any other path/method | After specialization, route the request to the loaded user function and return its response. |

The lifecycle is deliberately simple:

1. A pod starts as a **generic, unspecialized** server.
   Before specialization, any request to `/` should return a clear error such as `Container not specialized`.
2. The executor sends exactly one **specialize** request, which loads the user's code and caches it in memory.
3. From then on the container is **warm** and serves all invocations for that one function.

{{% notice info %}}
A container specializes **exactly once**.
Fission's pool manager replaces whole pods rather than re-specializing them, so you never need to handle a second specialize call.
Implement **both** `/specialize` (v1) and `/v2/specialize` (v2) — v2 is the modern path that supports builders and packaged directories, while v1 keeps single-file snippets working.
{{% /notice %}}

### How `functionName` is interpreted

The `functionName` field in the v2 body is language-specific — it is your environment's contract with function authors:

- **Python** — `module.function` (loaded with `importlib`, e.g. `hello.main`).
- **Node.js** — `filename.funcname`, or a bare filename for the default export.
- **Go** — a symbol exported by the compiled plugin (`.so`), looked up with `plugin.Lookup`.
- **JVM** — a fully-qualified class implementing `io.fission.Function`.
- **Rust** — the name of a compiled binary in the deploy package, spawned as a child process.

Pick a convention that is natural for your language and document it in your environment's README.

## Anatomy of a runtime image

The simplest runtime is an interpreted language that loads code in the same process as the server.
Python is the canonical example.

Its runtime `Dockerfile` builds a minimal image whose entrypoint is the server:

```dockerfile
FROM python:3.13-alpine
WORKDIR /app
RUN apk add --update --no-cache gcc python3-dev build-base libev-dev libffi-dev bash
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY *.py /app/
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python3"]
CMD ["server.py"]
```

The `server.py` it runs is a small HTTP server that:

- serves `GET /healthz`,
- on `POST /v2/specialize`, reads `{"filepath", "functionName"}`, imports the module, and caches the function object,
- routes every other request to that cached function.

The v2 loader is the only non-trivial part — it handles both a single file and a built package directory:

```python
def load_v2(specialize_info):
    filepath = specialize_info['filepath']
    handler = specialize_info['functionName']      # e.g. "hello.main"
    moduleName, funcName = handler.rsplit(".", 1)
    if os.path.isdir(filepath):                    # a built package
        sys.path.append(filepath)
        mod = importlib.import_module(moduleName)
    else:                                          # a single source file
        mod = import_src(filepath)
    return getattr(mod, funcName)                  # cache this and serve it
```

Compiled languages follow the same contract but differ in *how* they load code:

{{< tabs "runtime-styles" >}}
{{< tab "Interpreted (Python, Node.js, Ruby, PHP)" >}}
The server and the user function run in the **same process**.
Specialize imports the user module and keeps a reference to the function.
This is the simplest model and the best starting point for a new language.
{{< /tab >}}
{{< tab "Plugin (Go)" >}}
The builder compiles the user code into a Go **plugin** (`.so`).
At specialize time the server calls `plugin.Open` and `plugin.Lookup` to resolve the exported symbol, then dispatches requests to it.
The plugin must be built with the exact same Go toolchain as the runtime.
{{< /tab >}}
{{< tab "Separate process (Rust)" >}}
The builder compiles the user code into a **standalone server binary**.
The runtime ships only a small **supervisor** that, at specialize time, spawns the function binary on an internal port and reverse-proxies all requests to it.
If the function process exits, the supervisor exits too so the pod is replaced.
This keeps the runtime image tiny and isolates user code.
{{< /tab >}}
{{< /tabs >}}

## The builder contract

A builder is needed when source code must be compiled or its dependencies fetched.
A builder image must provide an executable at **`/usr/local/bin/build`** that:

1. reads source from the directory in the `SRC_PKG` environment variable,
2. produces a deployable artifact in the directory in the `DEPLOY_PKG` environment variable,
3. exits `0` on success, non-zero on failure.

The build script is short and language-specific.
Examples from the shipped environments:

{{< tabs "builder-scripts" >}}
{{< tab "Python" >}}
```sh
#!/bin/sh
set -euxo pipefail
if [ -f ${SRC_PKG}/requirements.txt ]; then
    pip3 install -r ${SRC_PKG}/requirements.txt -t ${SRC_PKG}
fi
cp -r ${SRC_PKG} ${DEPLOY_PKG}
```
Dependencies are installed next to the source, then the whole tree is copied so the runtime can add it to `sys.path`.
{{< /tab >}}
{{< tab "Node.js" >}}
```sh
#!/bin/sh
cd ${SRC_PKG}
npm install && cp -r ${SRC_PKG} ${DEPLOY_PKG}
```
`npm install` populates `node_modules/`, then the tree (now with dependencies) is copied to the deploy package.
{{< /tab >}}
{{< tab "Go" >}}
```sh
#!/bin/bash
set -eux
# ... place source under GOPATH, init go.mod if needed ...
go build -buildmode=plugin -o ${DEPLOY_PKG} .
```
Go compiles the source into a plugin written directly into the deploy package.
{{< /tab >}}
{{< /tabs >}}

In your environment repo the build script (often `build.sh` or `defaultBuildCmd`) is copied into the builder image and marked executable:

```dockerfile
COPY builder/build.sh /usr/local/bin/build
RUN chmod +x /usr/local/bin/build
```

To understand how the cluster invokes your builder, see the [builder pod architecture]({{% ref "/docs/architecture/builder-pod.md" %}}) and [Packages and builds]({{% ref "/docs/concepts/packages-and-builds.md" %}}).

## Modifying an existing environment

The most common change is bumping a base-image or runtime version.
Working in a clone of [fission/environments](https://github.com/fission/environments):

1. Update the base image / version in the environment's `Dockerfile` (or its build args).
2. Update the matching build args in **both** the runtime `Makefile` **and** the `builder/Makefile`, and in `skaffold.yaml` if present.
   The same pins are duplicated in these places and CI fails if they drift.
3. Bump the `version` field in the environment's `envconfig.json`.
   This is what triggers a new image release when the change merges.
4. Regenerate the catalog with `make update-env-json` — never hand-edit `environments.json`.

{{% notice warning %}}
The shared build rules in `rules.mk` default `DOCKER_FLAGS` to `--push`, so a bare `make` will try to push to `ghcr.io`.
For local builds, override it and target a single platform — see [Build and test locally](#build-and-test-locally) below.
{{% /notice %}}

## Adding support for a new language

Use the most recently added environment, [rust/](https://github.com/fission/environments/tree/master/rust), as your template — it exercises every pattern.
Create a new top-level directory in the environments repo (for example `mylang/`) containing:

1. **A runtime server** that implements the [runtime contract](#the-runtime-contract): `GET /healthz`, `POST /specialize`, `POST /v2/specialize`, and request routing on port `8888`.
   Start from the Python or Node.js server — the same-process model is simplest.
2. **A runtime `Dockerfile`** that installs the language and runs your server (see the Python example above).
3. **A builder** (only if your language compiles or needs dependency installation): `builder/Dockerfile` plus a `build.sh` copied to `/usr/local/bin/build` that honors `SRC_PKG`/`DEPLOY_PKG`.
4. **An `envconfig.json`** describing the images for the catalog.
   For example:

   ```json
   [
     {
       "kind": "environment",
       "name": "MyLang Environment",
       "image": "mylang-env",
       "builder": "mylang-builder",
       "runtimeVersion": "1.0",
       "version": "0.1.0",
       "shortDescription": "Fission MyLang environment.",
       "status": "Beta",
       "examples": "https://github.com/fission/examples/tree/main/mylang",
       "readme": "https://github.com/fission/environments/tree/master/mylang"
     }
   ]
   ```

5. **A `Makefile`** that includes `../rules.mk` and declares your image build args (copy from `rust/Makefile` and `rust/builder/Makefile`).
6. **Tests** — a minimal function fixture plus a local/kind test, mirroring `rust/tests/`.

Then:

7. Run `make update-env-json` to add your environment to `environments.json`.
8. Open a PR against [fission/environments](https://github.com/fission/environments).
   On merge, CI builds and publishes `ghcr.io/fission/mylang-env` (and the builder) at the version in `envconfig.json`.

Finally, surface the new language on this website's [Environments catalog](/environments/) by running `tools/environments.py` to regenerate `static/data/environments.json` — see the **updating-environments-and-examples** workflow and [tools/README.md](https://github.com/fission/fission.io/blob/main/tools/README.md).

## Build and test locally

Build the runtime (and builder) image into your local Docker daemon — note the overrides that avoid pushing and target a single platform:

```bash
cd mylang/
make mylang-env-img DOCKER_FLAGS=--load PLATFORMS=linux/arm64
cd builder/
make mylang-builder-img DOCKER_FLAGS=--load PLATFORMS=linux/arm64
```

Smoke-test the runtime contract before deploying.
Run the image, then exercise the endpoints:

```bash
docker run --rm -p 8888:8888 ghcr.io/fission/mylang-env:dev

# in another shell
curl -s localhost:8888/healthz                       # expect 200
curl -s -XPOST localhost:8888/v2/specialize \
  -d '{"filepath":"/path/in/container","functionName":"hello.main"}'
curl -s localhost:8888/                              # should run your function
```

When the image works, load it into your cluster and create an environment from it:

```bash
fission env create --name mylang --version 3 \
                   --image ghcr.io/fission/mylang-env:dev \
                   --builder ghcr.io/fission/mylang-builder:dev \
                   --poolsize 2
```

Then create a function and invoke it to confirm the full path works end to end — see [Create Function]({{% ref "functions.en.md" %}}).

## Publish

Once merged to [fission/environments](https://github.com/fission/environments), the release workflow detects every unpublished `image:version` pair from `envconfig.json` and pushes it to `ghcr.io/fission/<image>:<version>` plus a `latest` tag.
Bumping the `version` in `envconfig.json` is the single action that cuts a release, and versions are independent per environment.

## Related

- [Environments]({{% ref "/docs/concepts/environments.md" %}}) — concepts: runtime vs builder, specialization, the versioned interface.
- [Create Environment]({{% ref "environments.en.md" %}}) — using `fission env create` with an existing image.
- [Language environments]({{% ref "/docs/usage/languages/" %}}) — per-language setup and entry-point signatures.
- [Packages and builds]({{% ref "/docs/concepts/packages-and-builds.md" %}}) — how the builder turns source into a deployment archive.
- [Builder pod]({{% ref "/docs/architecture/builder-pod.md" %}}) — how the cluster runs your builder.
- [Environments catalog](/environments/) — all available runtime and builder images.
