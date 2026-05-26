---
title: "Upgrade Guide"
weight: 60
description: >
  Upgrade guidance 1.13 onwards
---

{{< notice warning >}}
Note: Fission upgrades cause a downtime as of now, however we try to minimize it. Please upvote the [issue#1856](https://github.com/fission/fission/issues/1856) so we can priortize fixing it.
{{< /notice >}}

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

## Upgrade to 1.24.x release

v1.24.0 is a security-hardening release.
The admission webhooks (with controller-side guards as defence in depth) now reject several primitives that earlier versions silently accepted.
Functions, packages, environments, and triggers that depend on them will be **rejected at admission** after upgrade, so audit your specs before rolling out.

### Cross-namespace references are rejected

A `Function`, `Package`, or `KubernetesWatchTrigger` that points at a resource in a *different* namespace is now refused:

- `Function.spec.environment.namespace` and `Function.spec.package.packageref.namespace` must equal the function's own namespace (or be empty).
- `Package.spec.environment.namespace` must equal the package's own namespace (or be empty).
- `KubernetesWatchTrigger.spec.namespace` must equal the trigger's own namespace (or be empty).

Empty values are unchanged — controllers continue to default them to the object's own namespace.
This closes a set of confused-deputy advisories where a low-privilege subject could make a cluster-wide controller act against another tenant's namespace.

### `KubernetesWatchTrigger` empty namespace now means "own namespace"

Previously an empty `spec.namespace` meant *watch all namespaces* (client-go's `""` semantics), which was itself a cross-tenant leak.
It now coerces to the trigger's own namespace.
If you relied on cluster-wide watch, create one `KubernetesWatchTrigger` per target namespace with `spec.namespace` set explicitly (each must equal the trigger's own namespace).

### Dangerous PodSpec fields are rejected

`Environment` and `Function` now reject a denylist of node-escape primitives in their PodSpec: `hostNetwork`, `hostPID`, `hostIPC`, hostPath volumes, container `privileged` / `allowPrivilegeEscalation`, dangerous Linux capabilities (`SYS_ADMIN`, `NET_ADMIN`, `SYS_PTRACE`, …), and `serviceAccountName` override.
The `Environment` runtime/builder container `securityContext` is validated the same way.
Benign customization — `image`, `command`, `args`, `env`, `volumes`, `resources`, `nodeSelector`, and capabilities like `NET_BIND_SERVICE` — flows through unchanged.

`MessageQueueTrigger` goes further: its `spec.podspec` is now reduced to an allowlist of `nodeSelector`, `tolerations`, `affinity`, `runtimeClassName`, and per-container `resources`.
All other fields are dropped (or rejected by the webhook).
MQT-referenced Secret values are no longer copied into the connector pod template; they resolve via `secretKeyRef` at pod start instead.

If any of your specs set these fields, remove them (or move the privileged workload out of Fission's tenant-facing CRDs) before upgrading.

### Cross-origin browser requests are denied by default

All Fission HTTP listeners now emit `X-Content-Type-Options: nosniff` and deny cross-origin browser preflights on internal listeners.
User `HTTPTrigger` traffic is unchanged by default.
If a single-page app legitimately calls a trigger cross-origin, opt in per trigger with the new `HTTPTrigger.spec.corsConfig` allowlist rather than handling CORS inside the function.

### fission-builder ServiceAccount token no longer mounted

Following the fission-fetcher change in v1.23.0, the `fission-builder` ServiceAccount token is no longer mounted into user builder containers.
No action is required unless your build commands depended on that token being present.

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

See [Internal Service Authentication](/docs/installation/internal-auth/) for the full toggle matrix, secret rotation, and longer-term mitigation.

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
