---
title: "Troubleshoot Fission Setup"
weight: 2
description: >
  Diagnose and fix problems installing or upgrading Fission: Helm, CRDs, and the admission webhook.
---

This page covers problems that surface while installing or upgrading Fission itself with Helm — failed releases, CRD mismatches, and admission-webhook certificate errors.
For problems with a running function, build, or trigger, see [Troubleshooting]({{% ref "/docs/trouble-shooting/_index.en.md" %}}).
For cluster-level problems (DNS, kubeconfig, volumes), see [Troubleshoot your Kubernetes cluster]({{% ref "/docs/trouble-shooting/setup/kubernetes.md" %}}).

## First, confirm the install is healthy

After a Helm install or upgrade, run the health check before debugging anything else:

```bash
$ fission check
```

If every service reports *running fine* and Fission is *up-to-date*, your control plane is healthy and the problem is likely in a function, package, or trigger rather than the install.

If a service is missing or restarting, inspect its pod:

```bash
$ kubectl -n fission get pods
$ kubectl -n fission describe pod <pod>
$ kubectl -n fission logs <pod>
```

{{% notice info %}}
Fission's CRDs are versioned with the `fission.io/v1` API group and are installed and upgraded **separately from the Helm chart**.
The chart does not update CRDs on `helm upgrade`, so a large share of upgrade problems trace back to a CRD that was never updated to match the new server.
See [CRD upgrade issues](#crd-upgrade-issues) below.
{{% /notice %}}

## Helm install issues

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `helm install` fails with "namespace not found" | The target namespace does not exist; the chart does not create it. | Create it first: `kubectl create namespace fission`, then install into it. |
| `helm install` fails because CRDs are missing | Fission CRDs were never applied; the chart expects them to already exist. | Apply the CRDs before installing the chart (see below), then re-run `helm install`. |
| Release already exists | A previous install (possibly failed) left a release of the same name. | `helm list -n fission` to find it, then `helm uninstall <name> -n fission` or `helm upgrade` instead. |
| Pods stuck `Pending` | No schedulable nodes or unsatisfiable resource requests. | `kubectl -n fission describe pod <pod>` and read `Events`; add capacity or lower requests. |
| `storagesvc` stuck `Pending`, PVC unbound | No default StorageClass / no dynamic provisioning. | Provision storage, or disable persistence — see [Dynamic Volume Provisioning]({{% ref "/docs/trouble-shooting/setup/kubernetes.md" %}}). |

The supported install sequence creates the namespace, applies the CRDs, then installs the chart:

```bash
$ export FISSION_NAMESPACE="fission"
$ kubectl create namespace $FISSION_NAMESPACE
$ kubectl create -k "github.com/fission/fission/crds/v1?ref={{< release-version >}}"
$ helm install fission fission-charts/fission-all --namespace $FISSION_NAMESPACE \
    --version {{< chart-version >}}
```

{{% notice info %}}
Fission requires Kubernetes 1.32 or newer.
If `fission check --pre` reports the Kubernetes version is not compatible, upgrade the cluster before installing.
{{% /notice %}}

See the full [installation guide]({{% ref "/docs/installation/_index.en.md" %}}) for prerequisites and options.

## CRD upgrade issues

CRDs are applied with `kubectl` against `github.com/fission/fission/crds/v1` and are **not** touched by `helm upgrade`.
When you upgrade Fission, update the CRDs to the matching version in the same step.

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| New fields rejected on `fission ... create`/`apply` after upgrade | CRDs are older than the upgraded server and lack the new schema. | Update the CRDs to the new version (`kubectl replace`, below), then retry. |
| `helm upgrade` succeeded but new behaviour is missing | CRDs were not updated, so new validation/status fields are absent. | Apply the CRDs for the target version. |
| `CustomResourceDefinition ... already exists` on `kubectl create` | CRDs were previously installed. | Use `kubectl replace` instead of `kubectl create`. |

Update CRDs to the version you are upgrading to:

```bash
$ kubectl replace -k "github.com/fission/fission/crds/v1?ref={{< release-version >}}"
```

{{% notice info %}}
In {{< release-version >}}, the CRDs carry status subresources with conditions, and the API server enforces CEL (Common Expression Language) validation rules — for example, executor-type and scale constraints.
Some validations that previously lived in admission webhooks (HTTPTrigger, TimeTrigger, and CanaryConfig) now run as CEL rules in the CRDs, so keeping CRDs in sync with the server is more important than before.
{{% /notice %}}

Follow the [upgrade guide]({{% ref "/docs/installation/upgrade.md" %}}) for version-specific notes before upgrading.

## Webhook certificate issues

Fission ships an admission webhook that validates Function, Package, Environment, KubernetesWatchTrigger, and MessageQueueTrigger resources.
Its `failurePolicy` is `Fail`, so when the API server cannot reach the webhook — or the TLS handshake fails — the API server **rejects** creates and updates of those resources.

By default the chart generates a self-signed CA and serving certificate for the webhook.
You can instead supply your own certificate material (`webhook.caBundlePEM`, `webhook.crtPEM`, `webhook.keyPEM`) or let cert-manager issue it (`webhook.certManager.enabled`).

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `create`/`update` of a function, package, or environment fails with a webhook / x509 / certificate error | The CA bundle on the webhook configuration no longer matches the serving certificate the webhook pod presents. | Reinstall or upgrade the chart so the CA bundle and serving cert are regenerated together, or supply matching `webhook.caBundlePEM`/`crtPEM`/`keyPEM` values. |
| `create`/`update` hangs then fails with "connection refused" / "context deadline exceeded" to the webhook service | The webhook pod is not running or not ready; with `failurePolicy: Fail` the request is denied. | `kubectl -n fission get pods -l svc=webhook-service` and `kubectl -n fission logs <webhook-pod>`; restore the pod, then retry. |
| `webhook.certManager.enabled=true` but requests still fail | cert-manager is not installed or has not issued the `Certificate` yet. | Confirm cert-manager is running and the webhook `Certificate` is `Ready` before relying on it. |

Confirm the webhook is healthy:

```bash
$ kubectl -n fission get pods -l svc=webhook-service
$ kubectl -n fission logs <webhook-pod>
$ fission check
```

A healthy `fission check` reports `webhook is running fine`.

## Related

- [Troubleshooting overview]({{% ref "/docs/trouble-shooting/_index.en.md" %}})
- [Troubleshoot your Kubernetes cluster]({{% ref "/docs/trouble-shooting/setup/kubernetes.md" %}})
- [Installation guide]({{% ref "/docs/installation/_index.en.md" %}})
- [Upgrade guide]({{% ref "/docs/installation/upgrade.md" %}})
