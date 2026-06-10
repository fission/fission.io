---
title: "OCI image packages"
draft: false
weight: 36
description: >
  Ship function code as an OCI image instead of an archive: build a code-only image, create a package with --oci, pin digests, use private registries, and optionally mount code via Kubernetes image volumes.
---

Starting with Fission v1.26.0, a package's deployment archive can be an **OCI image** instead of a zip archive.
You build an image whose filesystem contains your function code, push it to any OCI registry, and reference it when creating the package:

```bash
$ fission package create --name hello --env python \
    --oci registry.example.com/myteam/hello-code:v1
```

Everything else — environments, functions, triggers, entry points — works exactly as with archive-based packages.

#### Why deliver code as an image?

* **Faster, cache-friendly cold starts**: nodes and registries cache image layers, so repeated fetches of the same code are cheap, and there is no zip download + extract step from Fission's internal storage.
* **Standard supply-chain tooling**: code images can be signed (`cosign`), scanned, replicated, and promoted with the same tooling you already use for runtime images.
* **Registry-native workflows**: CI pipelines that already push images need no extra upload step to Fission's storage service.

OCI delivery is **opt-in per package**.
Archive-based packages remain the default and are unaffected.

#### Building a compatible code image

The image's filesystem must contain exactly what an *extracted deployment archive* would contain — your code files at the image root (or under a sub-path, see below).
The environment's runtime still comes from the environment image; the code image carries **only your code**.

For a Python function with a `main` entry point in `hello.py`:

```python
# hello.py
def main():
    return "Hello, world!\n"
```

```dockerfile
# Dockerfile
FROM scratch
COPY hello.py /
```

```bash
$ docker build -t registry.example.com/myteam/hello-code:v1 .
$ docker push registry.example.com/myteam/hello-code:v1
```

Multi-file packages work the same way — copy the whole directory:

```dockerfile
FROM scratch
COPY src/ /
```

You can also build code images without a Docker daemon using [`crane`](https://github.com/google/go-containerregistry/tree/main/cmd/crane):

```bash
$ tar -cf code.tar hello.py
$ crane append --base scratch --new_layer code.tar \
    --new_tag registry.example.com/myteam/hello-code:v1
```

##### Base image recommendations

* **Use `FROM scratch`.**
  The code image is never executed as a container — Fission only reads its filesystem — so it needs no shell, libc, or OS layer.
  A scratch-based code image is a few kilobytes, pulls fast, and has no CVE surface.
* Do **not** base the code image on the environment/runtime image.
  The runtime is supplied by the environment; duplicating it in the code image wastes pull time and storage and changes nothing at runtime.
* If your build pipeline cannot produce `FROM scratch` images, any minimal base works — Fission extracts the *merged* filesystem, so whatever the image contains beyond your code is extracted too.
  Keep it small and put code under a dedicated directory combined with `subPath` (below) so OS files are excluded.

#### Creating packages and functions

Create the package and reference it from a function as usual:

```bash
$ fission package create --name hello --env python \
    --oci registry.example.com/myteam/hello-code:v1
$ fission fn create --name hello --pkg hello --entrypoint hello.main
$ fission route create --name hello --function hello --url /hello --method GET
$ curl http://$FISSION_ROUTER/hello
Hello, world!
```

`fission fn create --oci <ref>` is a shortcut that creates the package and the function in one step, and `fission package update --name hello --oci <ref:v2>` switches a package to a new image (followed by `fn update` to roll running functions, exactly like archive updates).

The package spec exposes a few more fields than the CLI flag; use spec files for these:

```yaml
apiVersion: fission.io/v1
kind: Package
metadata:
  name: hello
spec:
  environment:
    name: python
  deployment:
    type: oci
    oci:
      image: registry.example.com/myteam/hello-code:v1
      # Optional: pin the exact content; the pull fails on any mismatch.
      digest: sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
      # Optional: code lives under /app inside the image (must be a directory).
      subPath: app
      # Optional: registry credentials, resolved in the function namespace.
      imagePullSecrets:
        - name: regcred
```

{{% notice info %}}
**Pin digests in production.**
A package references an image; re-pushing the same tag with different content is **not** detected automatically (functions roll only on package update).
Setting `digest` makes the reference immutable and the pull verifiable.
{{% /notice %}}

#### Private registries

Code-image pulls resolve credentials in this order:

1. The **`fission-fetcher` service account's `imagePullSecrets`** — the cluster-wide default for all packages.
2. The **package's own `imagePullSecrets`** — per-package credentials, set in the package spec.
3. **Anonymous** access.

Both secret sources are resolved in the namespace the function pods run in.
For functions in the `default` namespace that is the configured function namespace (`fission-function` in many installs); for functions in other namespaces it is the function's own namespace.
Confirm with `kubectl get pods -l environmentName=<env> -A` if unsure.

##### Step 1 — create a registry secret

Create a standard `docker-registry` secret in the function-pod namespace (see the [Kubernetes guide](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) for registry-specific details):

```bash
$ kubectl create secret docker-registry regcred \
    --namespace fission-function \
    --docker-server=registry.example.com \
    --docker-username=ci-bot \
    --docker-password="$REGISTRY_TOKEN"
```

##### Step 2a — cluster-wide: attach the secret to the fetcher service account

Patch the `fission-fetcher` service account in the same namespace; every OCI package pull then uses it without any per-package configuration:

```bash
$ kubectl patch serviceaccount fission-fetcher \
    --namespace fission-function \
    -p '{"imagePullSecrets": [{"name": "regcred"}]}'
```

##### Step 2b — per-package: reference the secret in the package spec

For credentials scoped to one package (e.g. different teams pulling from different registries), set `imagePullSecrets` in the package spec instead:

```yaml
apiVersion: fission.io/v1
kind: Package
metadata:
  name: hello
spec:
  environment:
    name: python
  deployment:
    type: oci
    oci:
      image: registry.example.com/myteam/hello-code:v1
      imagePullSecrets:
        - name: regcred
```

##### Verifying

Create a function on the package and invoke it; on a credential problem the function returns a 5xx and the fetcher log names the registry error:

```bash
$ kubectl logs <function-pod> -c fetcher -n fission-function | grep -i "error extracting OCI image"
```

{{% notice warning %}}
Fission does not validate that the referenced secrets exist or hold working credentials — a missing or wrong secret surfaces only at pull time.
With [image volumes](#optional-mount-code-with-kubernetes-image-volumes) enabled, the **kubelet** performs the pull using the same two secret sources (the pod inherits both), so the same setup keeps working — but pull errors then appear as pod events (`kubectl describe pod`, `ErrImagePull`) rather than fetcher logs.
{{% /notice %}}

Runtime/environment images are pulled by the kubelet independently of package images; for those, see [Pull an Image From a Private Registry]({{% ref "/docs/usage/function/private-registry.md" %}}).

#### Insecure (plain-HTTP) registries

Plain-HTTP registries are refused by default.
To allow specific hosts (e.g. an in-cluster registry for development), set the Helm value:

```yaml
fetcher:
  allowInsecureRegistries: "registry.dev.svc.cluster.local:5000"
```

This is a comma-separated host allowlist, not a global switch — every other registry still requires TLS.
Localhost and private (RFC-1918) IP addresses are implicitly trusted by the underlying client, matching Docker's behavior.

#### Optional: mount code with Kubernetes image volumes

By default the per-pod fetcher pulls and extracts the image (this works on every supported Kubernetes version).
On Kubernetes **1.33+** you can instead let the **kubelet** mount the code image directly into function pods as an [image volume](https://kubernetes.io/docs/tasks/configure-pod-container/image-volumes/), removing the fetch-and-extract step from the cold-start path entirely:

```yaml
executor:
  enableOCIImageVolume: true
```

On clusters below 1.33 the setting is detected as unsupported and packages silently stay on the fetcher path.
Be aware of the behavioral differences when image volumes are active:

* **The kubelet pulls the image, not Fission.**
  Image references resolve with the node's DNS and containerd's registry configuration — a registry reachable only through cluster DNS (a ClusterIP `Service` name) will not resolve.
  Use a registry address that nodes can reach.
* Poolmgr functions that reference **Secrets or ConfigMaps**, and functions on **v1 environments**, automatically fall back to the fetcher path (those features need the fetcher inside the pod).
* The code mount is **read-only**.
  Runtimes that write next to the code (Python bytecode caches, JVM work files) should write elsewhere; the standard Fission environments handle this.
* `subPath` must point to a **directory** inside the image (kubelets reject file sub-paths).
* The `digest` pin is enforced by the kubelet through the volume's image reference.

#### Limitations

* OCI delivery applies to **deployment** archives only; source packages (built by a builder on the cluster) keep using archives.
* The container executor is unrelated to OCI packages — it already runs your full container image and ignores packages entirely.
* `--oci` cannot be combined with `--code`, `--src`, or `--deploy`; a package has exactly one code source.
