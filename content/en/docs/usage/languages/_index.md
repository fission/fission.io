---
title: "Languages (Environment)"
weight: 50
description: >
  Supported language runtimes and how environments provide them
---

An **environment is the language-specific runtime in which your function executes.**

Every Fission function references exactly one environment.
The environment supplies a container image with the language runtime, a small web server that loads your code, and (optionally) a builder image that compiles source and fetches dependencies.
This page lists the runtimes Fission ships, explains the environment interface versions, and links to per-language guides.

## Supported language images

The following pre-built environments are published to `ghcr.io/fission/<name>` and maintained in the [fission/environments](https://github.com/fission/environments) repository.
Each environment has a runtime image (`*-env`) and, where dependency building is supported, a builder image (`*-builder`).

| Language | Runtime image | Builder image | Guide |
|----------|---------------|---------------|-------|
| Node.js | `ghcr.io/fission/node-env` | `ghcr.io/fission/node-builder` | [Node.js]({{% ref "nodejs.md" %}}) |
| Python | `ghcr.io/fission/python-env` | `ghcr.io/fission/python-builder` | [Python]({{% ref "python.md" %}}) |
| Go | `ghcr.io/fission/go-env` | `ghcr.io/fission/go-builder` | [Go]({{% ref "go.md" %}}) |
| Java (JVM) | `ghcr.io/fission/jvm-env` | `ghcr.io/fission/jvm-builder` | [Java]({{% ref "java.md" %}}) |
| Ruby | `ghcr.io/fission/ruby-env` | `ghcr.io/fission/ruby-builder` | [environments repo](https://github.com/fission/environments/tree/master/ruby) |
| PHP | `ghcr.io/fission/php-env` | `ghcr.io/fission/php-builder` | [environments repo](https://github.com/fission/environments/tree/master/php7) |
| Binary / Bash | `ghcr.io/fission/binary-env` | `ghcr.io/fission/binary-builder` | [environments repo](https://github.com/fission/environments/tree/master/binary) |
| Perl | `ghcr.io/fission/perl-env` | _none_ | [environments repo](https://github.com/fission/environments/tree/master/perl) |
| .NET | `ghcr.io/fission/dotnet-env` | _none_ | [environments repo](https://github.com/fission/environments/tree/master/dotnet) |
| .NET Core | `ghcr.io/fission/dotnet20-env` | `ghcr.io/fission/dotnet20-builder` | [environments repo](https://github.com/fission/environments/tree/master/dotnet20) |
| TensorFlow Serving | `ghcr.io/fission/tensorflow-serving-env` | _none_ | [environments repo](https://github.com/fission/environments/tree/master/tensorflow-serving) |

{{% notice info %}}
The [environment portal](/environments/) lists every published image and its available tags, generated from the [fission/environments](https://github.com/fission/environments) repository.
You can also bring your own runtime by packaging any container that speaks the [Fission environment interface](https://github.com/fission/environments).
{{% /notice %}}

## Environment interface versions

Fission supports three environment interface versions: v1, v2, and v3.
The interface version controls how your code is loaded and whether builders and pool tuning are available.

### v1

- Loads a function from a **single file**, which suits interpreted languages such as Python and JavaScript.
- Does **not** let you choose an entrypoint when the file defines several.

### v2 (recommended)

- The function code can live in a directory, or a single file can expose multiple entrypoints.
- **Loads a function by a specific entrypoint**, so you must provide one.
- Supports downloading dependencies and compiling source through a builder (optional).

### v3 (recommended)

- Includes everything in v2.
- Lets you tune the pre-warmed pool size per environment.

### Which interface version should I choose

If all source code and dependencies fit into a single, non-compiled file, the v1 interface is enough.

If your function needs third-party dependencies at runtime, or is written in a compiled language, choose v2 so you can load from a directory or binary with a specific entrypoint.

If you also want to tune the size of the environment's pre-warmed pool, use v3.

## Selecting an interface version

Pass the `--version` flag to `fission environment create`:

```bash
fission environment create --name go \
  --image ghcr.io/fission/go-env-1.26 \
  --builder ghcr.io/fission/go-builder-1.26 \
  --version 3
```

## Related

- [Functions]({{% ref "../function/_index.en.md" %}}) — create and invoke functions once an environment exists.
- [Environment portal](/environments/) — browse every published runtime and builder image.
- [fission/environments](https://github.com/fission/environments) — build or extend your own runtime.
