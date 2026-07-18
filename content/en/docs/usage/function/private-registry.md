---
title: "Pull an Image From a Private Registry"
weight: 6
description: >
  Pull environment images from a private registry by passing an imagePullSecret to fission environment create with --imagepullsecret.
---

**With 1.7.0+, you can specify which credential kubelet uses to pull images from a private registry.**

First, follow the [kubernetes guide](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) to create the secret.

{{% notice warning %}}
The secret must be created in the namespace where the function pods run.
By default this is the namespace where your Fission resources live (for example, `default`); confirm with `kubectl get pods -l environmentName=<env>` to see where the pods are scheduled.
{{% /notice %}}

Then, specify the secret when creating the environment.

For example, this creates a nodejs environment using secret `docker-secret` as credential.  

```bash
$ fission environment create --name nodejs --image ghcr.io/fission/node-env \
    --imagepullsecret "docker-secret"
```

You should see `imagePullSecrets` in the environment deployment, like the following.

```bash
$ kubectl -n fission-function get deploy -l environmentName=nodejs -o yaml

apiVersion: v1
items:
- apiVersion: extensions/v1beta1
  kind: Deployment
  metadata:
    name: poolmgr-nodejs-default-217063
    namespace: fission-function
    ...
  spec:
    ...
    template:
      ...
      spec:
        ...
        imagePullSecrets:
        - name: docker-secret

```

{{% notice warning %}}
Fission won't check that the secret exists, nor verify that the setting works.<br>
Check the pod status yourself to ensure everything works as expected.
{{% /notice %}}
