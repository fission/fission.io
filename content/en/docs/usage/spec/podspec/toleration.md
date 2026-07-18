---
title: "Toleration"
date: 2019-12-06T16:48:14+08:00
description: >
  Add tolerations to a Fission environment's PodSpec so functions schedule onto tainted nodes reserved for specific hardware or workloads.
---

**Add tolerations to a function's PodSpec so it schedules only onto nodes with matching taints.**

Taints and tolerations control pod scheduling in Kubernetes.
A taint on a node repels pods; a toleration on a pod lets it land on a node with a matching taint.
This is useful when specific pods need machines with certain hardware or capabilities, such as CPU-intensive instances.

You specify tolerations on a function's PodSpec in the environment spec.
The example below taints two nodes with `reservation=fission` and two nodes with `reservation=microservices`, so that functions schedule onto the nodes reserved for them and long-running microservices schedule onto the others.

```bash
$ kubectl taint nodes gke-fission-dev-default-pool-87c8b616-549c \
    gke-fission-dev-default-pool-87c8b616-5q2c reservation=fission:NoSchedule
node "gke-fission-dev-default-pool-87c8b616-549c" tainted
node "gke-fission-dev-default-pool-87c8b6aCloud16-5q2c" tainted

$ kubectl taint nodes gke-fission-dev-default-pool-87c8b616-pg05 \
    gke-fission-dev-default-pool-87c8b616-t5q1 reservation=microservices:NoSchedule
node "gke-fission-dev-default-pool-87c8b616-pg05" tainted
node "gke-fission-dev-default-pool-87c8b616-t5q1" tainted
```

Create a nodejs environment spec file:

```bash
$ fission env create --spec --name nodejs --image ghcr.io/fission/node-env --builder ghcr.io/fission/node-builder
```

Add the PodSpec toleration for `reservation=fission` to `.spec.runtime`:

```yaml
apiVersion: fission.io/v1
kind: Environment
...
spec:
  runtime:
    podspec:
      tolerations:
      - key: "reservation"
        operator: "Equal"
        value: "fission"
        effect: "NoSchedule"
```

You should now have an environment spec file like this:

```yaml
apiVersion: fission.io/v1
kind: Environment
metadata:
  creationTimestamp: null
  name: nodejs
  namespace: default
spec:
  builder:
    command: build
    image: ghcr.io/fission/node-builder
  imagepullsecret: ""
  keeparchive: false
  poolsize: 3
  resources: {}
  runtime:
    image: ghcr.io/fission/node-env
    podspec:
      tolerations:
      - key: "reservation"
        operator: "Equal"
        value: "fission"
        effect: "NoSchedule"
  version: 2
```

After applying the specs and running the function, the pods land only on nodes with taints that match the toleration:

```bash
$ kubectl get pod -o wide
NAME                                                 READY     STATUS    RESTARTS   AGE       IP             NODE
newdeploy-pyfunc-default-kgsuik0l-66cd755675-jgjj6   2/2       Running   0          51s       10.16.177.16   gke-fission-dev-default-pool-87c8b616-549c
poolmgr-python-default-okhvkdsv-57b866b774-hbz7q     2/2       Running   0          49s       10.16.176.34   gke-fission-dev-default-pool-87c8b616-5q2c
poolmgr-python-default-okhvkdsv-57b866b774-hqnl2     2/2       Running   0          49s       10.16.176.35   gke-fission-dev-default-pool-87c8b616-5q2c
poolmgr-python-default-okhvkdsv-57b866b774-pmtzv     2/2       Running   0          49s       10.16.177.17   gke-fission-dev-default-pool-87c8b616-549c
```
