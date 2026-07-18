---
title: "Environment Variable"
date: 2019-12-06T17:02:55+08:00
description: >
  Set environment variables on Fission environment pods via PodSpec, including exposing Kubernetes Secrets and ConfigMaps to your function.
---

**Set environment variables on a function's PodSpec to control runtime behavior or expose Kubernetes Secrets and ConfigMaps.**
For example, set `GOMAXPROCS` to tune a Go function's runtime, or inject a secret value without hardcoding it.
Add an `env` field to the PodSpec to do either.

{{% notice info %}}
Docker doesn't support changing a container's configuration after it's created.
To keep behavior consistent across executor types, Fission currently only supports setting environment variables at the Environment level.
{{% /notice %}}

## Add environment variable

Add an `env` entry to the `fetcher` container in the environment spec:

```yaml
apiVersion: fission.io/v1
kind: Environment
...
spec:
  runtime:
    podspec:
      containers:
      - name: fetcher
        env:
        - name: LOG_LEVEL
          value: info
```

The container now has the variable set:

```sh
$ kubectl exec -it <pod> -c fetcher sh
/ # env
LOG_LEVEL=info
```

## Expose Secret/ConfigMap as environment variable

First, create a ConfigMap called `my-configmap`:

```bash
$ kubectl create configmap my-configmap --from-literal=TEST_KEY="TESTVALUE"
```

Then reference it from the environment spec's PodSpec using `configMapKeyRef`:

```yaml
apiVersion: fission.io/v1
kind: Environment
...
spec:
  runtime:
    podspec:
      containers:
      - name: fetcher
        env:
          - name: TEST_KEY
            valueFrom:
              configMapKeyRef:
                name: my-configmap
                key: TEST_KEY
```

The ConfigMap value is now available as an environment variable in the container:

```sh
$ kubectl exec -it <pod> -c fetcher sh
/ # env
TEST_KEY=TESTVALUE
```
