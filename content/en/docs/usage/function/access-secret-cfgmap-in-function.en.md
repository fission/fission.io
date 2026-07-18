---
title: "Accessing Secrets/ConfigMaps"
draft: false
weight: 4
description: >
  Mount Kubernetes Secrets and ConfigMaps into a Fission function and read their values for API keys and configuration.
---

**Fission functions can mount Kubernetes [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) and [ConfigMaps](https://kubernetes.io/docs/concepts/storage/volumes/#configmap) as files, so your code can read API keys and other configuration at runtime.**
Use Secrets for sensitive values like API keys and authentication tokens.
Use ConfigMaps for any other configuration that doesn't need to be secret.

## Create a Secret or a ConfigMap

You can create a Secret or ConfigMap with the Kubernetes CLI:

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

## Accessing Secrets and ConfigMaps

Secrets and ConfigMaps are accessed the same way.
Each is a set of key-value pairs, and Fission exposes each key as a file your function can read.

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

# confimap my-configmap
/configs/default/my-configmap/TEST_KEY
```

This Python function (`leaker.py`) reads both files and returns the Secret `my-secret` and ConfigMap `my-configmap` values:

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
# Provide multiple Configmaps
$ fission fn create --name <fn-name> --env <env-name> --code <your-source> --configmap <configmap-one> --configmap <configmap-two>

# Provide multiple Secrets
$ fission fn create --name <fn-name> --env <env-name> --code <your-source> --secret <secret-one> --secret <secret-two>
```

Run the function to confirm both values are readable:

```bash
$ fission function test --name leaker
ConfigMap: TESTVALUE
Secret: TESTVALUE
```

## Updating Secrets and ConfigMaps

{{% notice note %}}
If a large number of functions use the same ConfigMap or Secret, updating it will cause a large number of pods to be re-created at once.
Make sure the cluster has enough capacity to absorb that short spike of pods terminating and starting.
{{% /notice %}}

Updating a ConfigMap or Secret updates the function pods, and the new value is used for subsequent function executions.
How long the change takes to reflect depends on how long the rolling update takes to finish.

{{% notice note %}}
In Fission versions prior to 1.4, an updated Secret or ConfigMap value may not reach the function, which can keep reading a cached, older value.
{{% /notice %}}
