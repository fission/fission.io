---
title: "Upgrade Guide"
weight: 60
description: >
  Upgrade guidance 1.13 onwards
---

{{% notice warning %}}
Fission upgrades currently cause a short downtime, though we work to minimize it.
Please upvote [issue #1856](https://github.com/fission/fission/issues/1856) so we can prioritize fixing it.
{{% /notice %}}

## Upgrade to the latest Fission version

### Upgrade/Replace the CRDs

```sh
kubectl replace -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
```

### Install the latest Fission CLI

Please make sure you have the latest CLI installed. Refer to [Fission CLI Installation]({{< ref "_index.en.md#install-fission-cli">}})

### Upgrade Fission chart

 Update the helm repo and upgrade by mentioning the namespace Fission is installed in :

```sh
export FISSION_NAMESPACE="fission"
helm repo update
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

_See [configuration](#configuration) below._

## Upgrade to {{< release-version >}} release

{{< release-version >}} raises the minimum supported Kubernetes version to **1.32** and continues the security-hardening line.
Before upgrading, confirm your cluster is on Kubernetes 1.32 or newer — the Helm chart now refuses to install on anything older.

Three breaking changes need attention:

1. **Kubernetes 1.32 minimum.** Clusters below 1.32 are rejected by the chart's `kubeVersion` constraint and fail the runtime `fission check` floor. The fluentbit `PodSecurityPolicy` manifest and the `logger.podSecurityPolicy` Helm value are removed (PSP no longer exists in Kubernetes 1.32); use Pod Security Admission instead.
2. **HTTPTrigger path validation at admission.** Empty paths, `..` traversal, root-only `/`, and paths that collide with router-owned routes (`/router-healthz`, `/readyz`, `/_version`, `/auth/login`) or shadow `/fission-function/<ns>/<name>` are now rejected. The `fission` CLI already enforced these; raw `kubectl apply` no longer bypasses them. Fix offending trigger paths before upgrading.
3. **PodSpec capabilities are an allowlist.** `Environment` and `Function` PodSpecs may only add `NET_BIND_SERVICE`; every container is forced to `drop: ["ALL"]`. Specs that added other capabilities are rejected, and workloads that silently relied on the OCI default cap set will see those caps stripped.

The HTTPTrigger / TimeTrigger / CanaryConfig admission webhooks are also removed in favor of API-server CEL validation.
A side effect: a raw `kubectl apply` of an invalid cron schedule, CORS origin, or ingress path is now **admitted and flagged with a `…=False` status condition** (for example `Scheduled=False`, `RouteAdmitted=False`) rather than rejected at creation.
The `fission` CLI still rejects these client-side, so the common path is unchanged.

See the [{{< release-version >}} release notes]({{% ref "../releases/v1.25.0.md" %}}#upgrade-notes) for the full list of breaking changes and the action each one requires.

## Upgrade to 1.24.x release

v1.24.0 is a security-hardening release.
The admission webhooks now reject cross-namespace references and dangerous PodSpec fields, deny cross-origin browser requests by default, and stop mounting the `fission-builder` ServiceAccount token into user builder containers.
Specs that rely on the rejected primitives will fail admission after upgrade, so review them first.

See the [v1.24.0 release notes]({{% ref "../releases/v1.24.0.md" %}}#upgrade-notes) for the full list of breaking changes and the action each one requires.

## Upgrade to 1.23.x release

v1.23.0 enables HMAC-signed internal authentication between Fission control-plane services by default.
This introduces two changes operators should plan for before upgrading.

### Public router no longer serves `/fission-function/<ns>/<name>`

The router now binds two listeners — a public one (port `8888`, unchanged for user `HTTPTrigger` traffic) and a new internal one (port `8889`, hosting `/fission-function/<ns>/<name>`).
This closes [GHSA-3g33-6vg6-27m8](https://github.com/fission/fission/security/advisories/GHSA-3g33-6vg6-27m8): function-invocation routes are no longer reachable from the public listener.

**Any external tooling that today curls `/fission-function/...` against the public router URL (typically through an Ingress) will get `404` after upgrade.**
Audit before upgrading and migrate any such caller to use a proper `HTTPTrigger`, or route through the internal Service (in-cluster only).

### KEDA message-queue triggers and the connector signing gap

`internalAuth.enabled` defaults to `true` in v1.23.0.
Upstream `fission/kafka-http-connector` (and the other Fission KEDA connector images) do not yet sign their `/fission-function/...` invocations, so KEDA-driven message-queue triggers will receive `401` from the new router internal listener.

If your installation uses KEDA-backed `MessageQueueTrigger` resources, **set `internalAuth.enabled=false` at upgrade time** until signing-aware KEDA connector images ship:

```sh
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all \
  --set internalAuth.enabled=false
```

With `enabled=false`, every signer/verifier short-circuits to pass-through and the cluster falls back to `NetworkPolicy` + namespace isolation alone — matching pre-1.23 in-cluster behaviour.

See [Internal Service Authentication]({{% ref "internal-auth.md" %}}) for the full toggle matrix, secret rotation, and longer-term mitigation.

## Upgrade to 1.15.x release from 1.14.x release

With 1.15.x release, following changes are made:

- `fission-core` chart is removed
- `fission-all` chart is made similar `fission-core` chart
- In the `fission-all` chart, the following components are disabled which were enabled by default earlier. If you want to enable them, please use `--set` flag.

  - nats - Set `nats.enabled=true` to enable Fission Nats integration
  - influxdb - Set `influxdb.enabled=true` to enable Fission InfluxDB and logger component
  - prometheus - Set `prometheus.enabled=true` to install Prometheus with Fission
  - canaryDeployment - Set `canaryDeployment.enabled=true` to enable Canary Deployment

_See [configuration](#configuration) below._

### Migrating from `fission-core` chart to `fission-all` chart

`Fission-all` chart is now exactly similar to `fission-core` chart and can be used to migrate from `fission-core`.

If you are upgrading from the fission-core chart, you can use the following command to migrate with required changes.

```console
helm upgrade [RELEASE_NAME] fission-charts/fission-all --namespace fission
```

## Configuration

See [Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing). To see all configurable options with detailed comments:

```console
helm show values fission-charts/fission-all
```

You may also `helm show values` on chart's dependencies for additional options.
