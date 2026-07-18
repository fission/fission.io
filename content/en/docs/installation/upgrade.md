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

**Every upgrade needs three steps, in order: replace the CRDs, update the CLI, then upgrade the chart.**
Check the version-specific sections below for anything extra your target release requires.

### Upgrade/Replace the CRDs

Apply the CRD manifest for the version you're upgrading to:

```sh
kubectl replace -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
```

### Install the latest Fission CLI

Make sure you have the latest CLI installed.
Refer to [Fission CLI Installation]({{< ref "_index.en.md#install-fission-cli">}}).

### Upgrade Fission chart

Update the Helm repo, then upgrade by specifying the namespace Fission is installed in:

```sh
export FISSION_NAMESPACE="fission"
helm repo update
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

_See [configuration](#configuration) below._

## Upgrade to 1.27.x release

v1.27.0 adds opt-in multi-namespace tenancy and a function-developer observability toolkit (invocation correlation, `fission function describe`, and local `run-local` development).
Tenancy is off by default — `tenancy.mode: static` renders byte-identical RBAC and keeps the existing auth model — so a single-namespace or `additionalFissionNamespaces` install upgrades with just the routine CRD/CLI/chart steps above, and the minimum Kubernetes version is unchanged at **1.32**.
To onboard namespaces at runtime with `fission tenant enable` instead of editing `additionalFissionNamespaces`, see [Multi-namespace tenancy](/docs/usage/multi-namespace-tenancy/).

Two runtime defaults change visibly and are worth reviewing first:

- The router now returns a structured JSON error body for attributed failures (status codes are unchanged). A client that parses the literal old plain-text body should read the JSON instead, or set `ROUTER_STRUCTURED_ERRORS=false` to restore it.
- Trace sampling now honors `OTEL_TRACES_SAMPLER`, so if you export traces over OTLP, successful-trace volume drops to the documented `0.1` ratio (all error traces are still kept). Set `OTEL_TRACES_SAMPLER=parentbased_always_on` to keep 100% export.

See the [v1.27.0 release notes](/docs/releases/v1.27.0/#upgrade-notes) for the full list of behavioral changes and the action each one requires.

## Upgrade to 1.26.x release

v1.26.0 is a large feature release: OCI-native package delivery, the Kubernetes Gateway API route provider, streaming responses, functions as MCP tools, and an EndpointSlice-native router data plane.
There are no Kubernetes-version or admission changes from v1.25.0, so the routine CRD/CLI/chart steps above are all most installs need.

Two behavioral defaults are worth reviewing before you upgrade:

- The router now serves warm traffic directly from EndpointSlices and accounts request concurrency **per router replica** by default. Functions that depend on global concurrency enforcement should set the `fission.io/concurrency-enforcement: strict` annotation.
- When a package registry is configured (`packageRegistry.enabled`), builds publish their deployment archive as a digest-pinned OCI image and functions cold-start from it. Leave `packageRegistry.enabled` unset to keep today's tarball behavior unchanged.

See the [v1.26.0 release notes](/docs/releases/v1.26.0/#upgrade-notes) for the full list of behavioral changes and the action each one requires.

## Upgrade to 1.25.x release

v1.25.0 raises the minimum supported Kubernetes version to **1.32** and continues the security-hardening line.
Before upgrading, confirm your cluster is on Kubernetes 1.32 or newer — the Helm chart now refuses to install on anything older.

Three breaking changes need attention:

1. **Kubernetes 1.32 minimum.** Clusters below 1.32 are rejected by the chart's `kubeVersion` constraint and fail the runtime `fission check` floor. The fluentbit `PodSecurityPolicy` manifest and the `logger.podSecurityPolicy` Helm value are removed (PSP no longer exists in Kubernetes 1.32); use Pod Security Admission instead.
2. **HTTPTrigger path validation at admission.** Empty paths, `..` traversal, root-only `/`, and paths that collide with router-owned routes (`/router-healthz`, `/readyz`, `/_version`, `/auth/login`) or shadow `/fission-function/<ns>/<name>` are now rejected. The `fission` CLI already enforced these; raw `kubectl apply` no longer bypasses them. Fix offending trigger paths before upgrading.
3. **PodSpec capabilities are an allowlist.** `Environment` and `Function` PodSpecs may only add `NET_BIND_SERVICE`; every container is forced to `drop: ["ALL"]`. Specs that added other capabilities are rejected, and workloads that silently relied on the OCI default cap set will see those caps stripped.

The HTTPTrigger / TimeTrigger / CanaryConfig admission webhooks are also removed in favor of API-server CEL validation.
A side effect: a raw `kubectl apply` of an invalid cron schedule, CORS origin, or ingress path is now **admitted and flagged with a `…=False` status condition** (for example `Scheduled=False`, `RouteAdmitted=False`) rather than rejected at creation.
The `fission` CLI still rejects these client-side, so the common path is unchanged.

See the [v1.25.0 release notes](/docs/releases/v1.25.0/#upgrade-notes) for the full list of breaking changes and the action each one requires.

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
Upstream `ghcr.io/fission/keda-kafka-http-connector` (and the other `keda-*-http-connector` images) do not yet sign their `/fission-function/...` invocations, so KEDA-driven message-queue triggers will receive `401` from the new router internal listener.

If your installation uses KEDA-backed `MessageQueueTrigger` resources, **set `internalAuth.enabled=false` at upgrade time** until signing-aware KEDA connector images ship:

```sh
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all \
  --set internalAuth.enabled=false
```

With `enabled=false`, every signer/verifier short-circuits to pass-through and the cluster falls back to `NetworkPolicy` + namespace isolation alone — matching pre-1.23 in-cluster behaviour.

See [Internal Service Authentication]({{% ref "internal-auth.md" %}}) for the full toggle matrix, secret rotation, and longer-term mitigation.

## Upgrade to 1.15.x release from 1.14.x release

**v1.15.0 merges the `fission-core` chart into `fission-all` and disables four previously-default components.**

- The `fission-core` chart is removed.
- The `fission-all` chart now covers what `fission-core` did.
- In the `fission-all` chart, the components below are disabled by default (they were enabled before); re-enable any of them with the matching `--set` flag.

| Component | Flag to re-enable | Effect |
|---|---|---|
| nats | `nats.enabled=true` | Fission NATS integration |
| influxdb | `influxdb.enabled=true` | Fission InfluxDB and logger component |
| prometheus | `prometheus.enabled=true` | Installs Prometheus with Fission |
| canaryDeployment | `canaryDeployment.enabled=true` | Canary Deployment |

_See [configuration](#configuration) below._

### Migrating from `fission-core` chart to `fission-all` chart

The `fission-all` chart is now chart-for-chart identical to `fission-core`, so it can replace it directly.

If you're upgrading from the `fission-core` chart, migrate with:

```console
helm upgrade [RELEASE_NAME] fission-charts/fission-all --namespace fission
```

## Configuration

See [Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing).
To see all configurable options with detailed comments:

```console
helm show values fission-charts/fission-all
```

You may also run `helm show values` on the chart's dependencies for additional options.
