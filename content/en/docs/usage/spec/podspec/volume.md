---
title: "Volume"
date: 2019-12-06T16:50:52+08:00
description: >
  Define and mount Kubernetes volumes on Fission function containers through PodSpec so stateful functions can access attached data.
---

**PodSpec lets you attach a Kubernetes volume to a function's container.**
Functions are typically stateless, but workloads like data pipelines need access to attached data.
You **define a volume** and then **mount it on a specific container**.
The example below creates a volume with the Kubernetes downward API, which dumps pod label information into a file, and mounts it on the function container at `/etc/funcdata`.

```yaml
apiVersion: fission.io/v1
kind: Environment
...
spec:
  podspec:
    # A container which will be merged with for pool manager
    containers:
    - name: nodep
      image: ghcr.io/fission/node-env
      volumeMounts:
        - name: funcvol
          mountPath: /etc/funcdata
          readOnly: true
    volumes:
      - name: funcvol
        downwardAPI:
          items:
            - path: "labels"
              fieldRef:
                fieldPath: metadata.labels
```
