---
title: "Kubernetes"
weight: 1
description: >
  Diagnose cluster-level problems that affect Fission: DNS, kubeconfig, persistent volumes, and autoscaling.
---

This page covers problems that originate in the Kubernetes cluster rather than in Fission, but which stop Fission from working.
If `fission check` reports services as unhealthy, or the CLI cannot reach the cluster at all, work through the sections below.
For Helm, CRD, and webhook problems, see [Troubleshoot your Fission setup]({{% ref "/docs/trouble-shooting/setup/fission.md" %}}).

## In-cluster DNS

Fission components address each other by Kubernetes service name, so in-cluster DNS must be working.
A DNS outage typically shows up as components failing to reach each other and `fission check` reporting services as not running.

First, confirm the cluster DNS pods are running:

```bash
$ kubectl -n kube-system get pod | grep dns
coredns-fb8b8dccf-bjxmj                  1/1     Running   1          65m
```

Then resolve a Fission service from inside the cluster.
Look up the service, then run `nslookup` from a throwaway pod:

```bash
$ kubectl -n fission get svc
NAME       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
executor   ClusterIP   10.103.121.81   <none>        80/TCP    2d

$ kubectl -n fission run busybox --image=busybox --restart=Never --rm -it -- \
    nslookup executor
Server:   10.96.0.10
Address:  10.96.0.10:53

Name:     executor.fission.svc.cluster.local
Address:  10.103.121.81
```

The resolved address should match the `CLUSTER-IP` from the previous command.

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `fission check` reports services down, but pods are `Running` | In-cluster DNS resolution is broken. | Verify CoreDNS pods are `Running`; run the `nslookup` test above. |
| Component log shows a lookup failure resolving another service | DNS pods are down or the cluster DNS service is unreachable. | Restore CoreDNS, then re-run `fission check`. |

For deeper DNS debugging, see the [Kubernetes DNS resolution guide](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/).

## Connecting to the cluster (kubeconfig)

The Fission CLI talks directly to the Kubernetes API server, so it needs a valid kubeconfig.
If the CLI cannot connect, it cannot read Fission resources or port-forward to components.

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CLI cannot reach the cluster | `~/.kube/config` is missing or `KUBECONFIG` is wrong. | Confirm `~/.kube/config` exists or set `KUBECONFIG` to the correct file; verify with `kubectl get nodes`. |
| `error upgrading connection` during port-forward | The target pod was not found, is restarting, or RBAC denies port-forward. | Check the pod status (`kubectl -n fission get pods`) and your permissions, then retry. |

If you run a managed cluster, follow your provider's steps to add credentials to `~/.kube/config`:

- GKE: <https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl>
- EKS: <https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html>
- AKS: <https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli#connect-to-the-cluster>

## Persistent volumes

The storage service needs a persistent volume when persistence is enabled (the default), unless you use an external object store such as S3.
Without dynamic provisioning, its PersistentVolumeClaim stays `Pending` and the pod never starts.

After provisioning is configured, you should be able to list bound claims and volumes:

```bash
$ kubectl -n fission get pvc
NAME                  STATUS   VOLUME       CAPACITY   ACCESS MODES   STORAGECLASS   AGE
fission-storage-pvc   Bound    pvc-733e...  8Gi        RWO            hostpath       75m
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `storagesvc` pod stuck `Pending` | Its PVC is unbound — no default StorageClass or no dynamic provisioner. | Configure [dynamic provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/), or disable persistence (below). |

If the platform cannot provide persistent volumes, disable persistence at install time:

```bash
$ helm install fission fission-charts/fission-all --namespace fission \
    --set persistence.enabled=false
```

## Autoscaling prerequisites

Fission scales function replicas through the Kubernetes Horizontal Pod Autoscaler, which needs the metrics server installed and serving metrics.

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Functions do not scale under load | The metrics server is not installed. | Install the [metrics server](https://github.com/kubernetes-sigs/metrics-server); on minikube run `minikube addons enable metrics-server`. |
| HPA `TARGETS` shows `<unknown>` | The metrics server was just installed and has not collected data yet. | Wait a few minutes; if it persists, verify the metrics server is healthy. |

An HPA with unknown targets looks like this right after install:

```bash
$ kubectl get hpa
NAME         REFERENCE               TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   <unknown>/50%   1         10        1          3m3s
```

Follow the [HPA walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) to verify the metrics server.

{{% notice info %}}
Message-queue triggers scale through [KEDA](https://keda.sh) (v2.20), not the HPA metrics path.
If a `mqtrigger` does not scale, confirm KEDA is installed and reconciling its `ScaledObject` — that is separate from the metrics server above.
{{% /notice %}}

## Related

- [Troubleshooting overview]({{% ref "/docs/trouble-shooting/_index.en.md" %}})
- [Troubleshoot your Fission setup]({{% ref "/docs/trouble-shooting/setup/fission.md" %}})
- [Installation guide]({{% ref "/docs/installation/_index.en.md" %}})
