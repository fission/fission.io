---
title: "Secrets, ConfigMaps, and Environment Variables"
draft: false
weight: 4
description: >
  Mount Kubernetes Secrets and ConfigMaps into a Fission function as files, or inject them and literal values as per-function environment variables.
---

**Fission functions read configuration through two channels.**
The first channel is [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and [ConfigMaps](https://kubernetes.io/docs/concepts/storage/volumes/#configmap) mounted as files.
The second channel, starting with Fission {{< release-version >}}, is per-function environment variables, which can also project Secret and ConfigMap values.
Use Secrets for sensitive values such as API keys and tokens.
Use ConfigMaps for configuration that is not secret.
Use environment variables for 12-factor configuration such as `DATABASE_URL` or `LOG_LEVEL`.

## Create a Secret or a ConfigMap

Create a Secret or ConfigMap with the Kubernetes CLI:

```bash
$ kubectl -n default create secret generic my-secret --from-literal=TEST_KEY="TESTVALUE"

$ kubectl -n default create configmap my-configmap --from-literal=TEST_KEY="TESTVALUE"
```

Or, use `kubectl create -f <filename.yaml>` to create these from a YAML file.

```yaml
apiVersion: v1
kind: Secret
metadata:
  namespace: default
  name: my-secret
data:
  TEST_KEY: VEVTVFZBTFVF # value after base64 encode
type: Opaque

---
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: default
  name: my-configmap
data:
  TEST_KEY: TESTVALUE
```

The object must be in the same namespace as the function.

## Access as files

Attach a Secret or ConfigMap to a function with `--secret` or `--configmap`.
Fission exposes each key of the object as a file:

```text
# Secret path
/secrets/<namespace>/<name>/<key>

# ConfigMap path
/configs/<namespace>/<name>/<key>
```

From the previous example, the paths are:

```text
# secret my-secret
/secrets/default/my-secret/TEST_KEY

# configmap my-configmap
/configs/default/my-configmap/TEST_KEY
```

This Python function (`leaker.py`) reads both files and returns the values:

```python
# leaker.py

def main():
    path = "/configs/default/my-configmap/TEST_KEY"
    f = open(path, "r")
    config = f.read()
    f.close()

    path = "/secrets/default/my-secret/TEST_KEY"
    f = open(path, "r")
    secret = f.read()
    f.close()

    msg = "ConfigMap: %s\nSecret: %s" % (config, secret)

    return msg, 200
```

Create an environment and a function:

```bash
# create python env
$ fission env create --name python --image ghcr.io/fission/python-env

# create function named "leaker"
$ fission fn create --name leaker --env python --code leaker.py --secret my-secret --configmap my-configmap
```

To attach multiple ConfigMaps or Secrets, repeat the flag:

```bash
# Provide multiple ConfigMaps
$ fission fn create --name <fn-name> --env <env-name> --code <your-source> --configmap <configmap-one> --configmap <configmap-two>

# Provide multiple Secrets
$ fission fn create --name <fn-name> --env <env-name> --code <your-source> --secret <secret-one> --secret <secret-two>
```

On `fission fn update`, the `--secret` and `--configmap` lists replace the function's previous lists.

Run the function to confirm both values are readable:

```bash
$ fission function test --name leaker
ConfigMap: TESTVALUE
Secret: TESTVALUE
```

{{% notice info %}}
The poolmgr and newdeploy executors write these files through the fetcher.
The container executor has no fetcher: it projects a name-only `--secret` / `--configmap` reference as environment variables instead of files.
See the [executor support matrix](#executor-support) below.
{{% /notice %}}

### Change the mount path

By default an object's files land under `/secrets/<namespace>/<name>` or `/configs/<namespace>/<name>`.
Set `mountPath` on the reference in the function spec to redirect them.
There is no `fn create` / `fn update` flag for it.
Edit the spec YAML instead (the `fission spec` workflow or `kubectl`):

```yaml
# in the Function spec
secrets:
  - namespace: default
    name: my-secret
    mountPath: app/creds   # files land at /secrets/app/creds/<key>
configmaps:
  - namespace: default
    name: my-configmap
    mountPath: app/conf    # files land at /configs/app/conf/<key>
```

Rules, enforced at admission:

- The path is **relative** to the `/secrets` or `/configs` root; absolute paths are rejected.
- No two Secrets (or two ConfigMaps) on one function may resolve to the same directory.
- Environments with `allowedFunctionsPerContainer: infinite` do not support `mountPath` — their pods share one file tree across functions.

All three executors honor `mountPath`: poolmgr and newdeploy through the fetcher, the container executor through a native read-only volume.
On the container executor the env-var projection of a name-only reference remains in addition to the mounted files.

For the local loop, `fission fn run-local` reproduces the same layout with `--secret-mount NAME=PATH` and `--configmap-mount NAME=PATH`.

## Inject environment variables

Starting with Fission {{< release-version >}}, a function carries its own environment variables: literal values, single Secret/ConfigMap keys, or whole-object projections.

{{% notice warning %}}
Per-function environment variables work on the **newdeploy** and **container** executors only.
The **poolmgr** executor (the default) does not support them yet; admission rejects the function rather than deploying it with empty variables.
Poolmgr support is phase 2 of RFC-0030 and is tracked in [fission/fission#3666](https://github.com/fission/fission/issues/3666).
{{% /notice %}}

Create the objects to project:

```bash
$ kubectl -n default create secret generic db-creds \
  --from-literal=username=app --from-literal=password=hunter2

$ kubectl -n default create configmap app-config \
  --from-literal=LOG_LEVEL=debug --from-literal=REGION=eu-west-1
```

This Python function (`env-reader.py`) reads its process environment:

```python
# env-reader.py
import os

def main():
    return "\n".join([
        "DATABASE_URL=%s" % os.environ["DATABASE_URL"],
        "DB_PASSWORD=%s" % os.environ["DB_PASSWORD"],
        "LOG_LEVEL=%s" % os.environ["LOG_LEVEL"],
        "REGION=%s" % os.environ["REGION"],
    ]), 200
```

Create the function with all three flag forms — a literal, a renamed single key, and a whole-object projection:

```bash
$ fission fn create --name env-reader --env python --code env-reader.py \
  --executortype newdeploy \
  --env-var DATABASE_URL=postgres://db.default:5432/app \
  --env-from-secret db-creds/password:DB_PASSWORD \
  --env-from-configmap app-config
```

```bash
$ fission fn test --name env-reader
DATABASE_URL=postgres://db.default:5432/app
DB_PASSWORD=hunter2
LOG_LEVEL=debug
REGION=eu-west-1
```

The reference forms of `--env-from-secret` and `--env-from-configmap`:

| Form | Result |
| --- | --- |
| `name` | Projects every key of the object as an environment variable. |
| `name/key` | Injects one key; the variable takes the key's name. |
| `name/key:ENV` | Injects one key; the variable is named `ENV`. |

All three flags are repeatable.
`--env` keeps its existing meaning — the Environment name — so literals use `--env-var` (short form `-e`).

Without `--executortype newdeploy`, the create is rejected, because the default executor is poolmgr:

```text
$ fission fn create --name env-reader --env python --code env-reader.py --env-var LOG_LEVEL=debug
Error: ... FunctionSpec.Env: ... env/envFrom are not supported on the poolmgr executor yet
(lands with RFC-0030 phase 2); use the newdeploy or container executor
```

### Replacement on update

The three env flags replace the function's env configuration **as one unit**.
Pass every env flag the function needs in one `fn update`:

```bash
$ fission fn update --name env-reader \
  --env-var DATABASE_URL=postgres://db.default:5432/app \
  --env-var LOG_LEVEL=info \
  --env-from-secret db-creds/password:DB_PASSWORD \
  --env-from-configmap app-config
```

Passing only some of the three flags removes the variables set through the omitted flags.
The CLI prints a warning when that happens.
An env change is a runtime-affecting update: the function's pods roll and new pods see the new values.

### Precedence and reserved names

- `--env-var` literals win over `--env-from-*` whole-object projections.
- A `name/key` selection counts as a literal-level entry, so a named single key also beats a whole-object projection.
- Function env wins over environment variables from the Environment's pod spec.
- Platform-reserved names are rejected at admission: any `FISSION_*` name, `RESOURCE_VERSION_COUNT`, the proxy set (`HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, in either case), `LD_PRELOAD`, `NODE_OPTIONS`, and `PYTHONPATH`.

{{% notice note %}}
A Secret value injected as an environment variable is visible to `kubectl exec` and to crash handlers — the standard Kubernetes caveat.
For high-sensitivity material, prefer the [file mount](#access-as-files) pattern.
{{% /notice %}}

## Executor support

| Access pattern | poolmgr | newdeploy | container |
| --- | --- | --- | --- |
| `--secret` / `--configmap` as files | Yes (fetcher) | Yes (fetcher) | No — projected as env vars instead |
| `mountPath` redirect (spec field) | Yes (fetcher) | Yes (fetcher) | Yes (native volume) |
| `--env-var` / `--env-from-secret` / `--env-from-configmap` | No — rejected at admission ([#3666](https://github.com/fission/fission/issues/3666)) | Yes | Yes |

On the container executor, combining `--env-from-*` with `--secret` / `--configmap` is rejected: `envFrom` replaces the legacy whole-object projection, so declare the objects in `--env-from-*` instead of alongside it.

## Updating Secrets and ConfigMaps

Updating a Secret or ConfigMap recycles the pods of every function that references it — through `--secret` / `--configmap` or through the env flags.
Subsequent executions see the new value; how fast depends on how long the rolling update takes.
Kubernetes never refreshes environment variables in a running container, so env values change only when pods are recreated.

{{% notice note %}}
If a large number of functions use the same ConfigMap or Secret, updating it re-creates a large number of pods at once.
Make sure the cluster has enough capacity to absorb that short spike of pods terminating and starting.
{{% /notice %}}

## Related

- [Executors](/docs/usage/function/executor/) — what poolmgr, newdeploy, and container executors are.
- [Container functions](/docs/usage/function/container-functions/) — the container executor workflow.
- [`fission function create` reference](/docs/reference/fission-cli/fission_function_create/) — the full flag list.
- [CRD reference](/docs/reference/crd-reference/) — the `env`, `envFrom`, and `mountPath` fields on the `Function` resource.
