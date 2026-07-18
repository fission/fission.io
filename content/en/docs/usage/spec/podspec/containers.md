---
title: "Sidecar and Init Container"
date: 2019-12-06T16:52:08+08:00
description: >
  Add init containers and sidecar containers to a Fission environment's PodSpec to run setup or auxiliary processes alongside functions.
---

## Init container

**Init containers run setup work — such as fetching data from a remote bucket — before the function container starts.**

PodSpec lets you **define init containers** and use volumes, as shown in the previous example.

```yaml
apiVersion: fission.io/v1
kind: Environment
...
spec:
  runtime:
    podspec:
      initContainers:
      - name: init-py
        image: ghcr.io/fission/python-env
        command: ['sh', '-c', 'cat /etc/infopod/labels']
        volumeMounts:
          - name: infopod
            mountPath: /etc/infopod
            readOnly: false
      volumes:
        - name: infopod
          downwardAPI:
            items:
              - path: "labels"
                fieldRef:
                  fieldPath: metadata.labels
```

The init container runs first, before the function containers start:

```bash
$ kubectl get pod
NAME                                               READY     STATUS            RESTARTS   AGE
poolmgr-python-default-9eik2gxd-6fdc8d9696-hkkgn   0/2       Init:0/1          0          10s
poolmgr-python-default-9eik2gxd-6fdc8d9696-lpmgl   0/2       PodInitializing   0          10s
poolmgr-python-default-9eik2gxd-6fdc8d9696-tkmdc   0/2       PodInitializing   0          10s
```

The init container prints the mounted file; verify this in its logs:

```bash
$ kubectl logs -f poolmgr-python-default-9eik2gxd-6fdc8d9696-lpmgl -c init-py
environmentName="python"
environmentNamespace="default"
environmentUid="68e3f909-3e86-11e9-9378-42010aa00057"
executorInstanceId="dqaukdxy"
executorType="poolmgr"
pod-template-hash="2987485252"
```

## Sidecar container

**Sidecar containers run alongside the function container** by adding an extra entry to PodSpec's `containers` list:

```yaml
    podspec:
      # A container which will be merged with for pool manager
      containers:
      - name: nodep
        image: ghcr.io/fission/node-env
        volumeMounts:
          - name: funcvol
            mountPath: /etc/funcdata
            readOnly: true
      # A additional container in the pods
      - name: yanode
        image: ghcr.io/fission/node-env
        command: ['sh', '-c', 'sleep 36000000000']
```
