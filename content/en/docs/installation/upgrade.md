---
title: "Upgrade Guide"
weight: 60
description: >
  Upgrade Fission with Helm: the routine steps, what happens to in-flight traffic and warm pods during the roll, and how to tune the drain windows.
---

{{% notice info %}}
Zero-downtime upgrades are the goal of Fission's upgrade design ([issue #1856](https://github.com/fission/fission/issues/1856)).
Recent releases ship rollout defaults that keep warm function traffic serving while the control plane rolls.
Fission does not yet test or guarantee zero downtime for every request, so schedule upgrades in a low-traffic window when that matters.
{{% /notice %}}

## Upgrade to the latest Fission version

**Every upgrade needs two steps, in order: update the CLI, then upgrade the chart.**
Starting with Fission {{< release-version >}}, `helm upgrade` applies the matching CRDs itself through a pre-upgrade hook.
You need a separate CRD step only when you opt out.
Check the version-specific sections below for anything extra your target release requires.

### Install the latest Fission CLI

Make sure you have the latest CLI installed.
Refer to [Fission CLI Installation](/docs/installation/#install-fission-cli).

### Upgrade Fission chart

Update the Helm repo, then upgrade by specifying the namespace Fission is installed in:

```sh
export FISSION_NAMESPACE="fission"
helm repo update
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

With the default `crds.mode=hook`, the chart's [pre-upgrade checks](#pre-upgrade-checks) Job applies the target version's CRDs before any component rolls.

If you set `crds.mode=none` because your organization does not grant CRD write to a chart, apply the CRD manifest yourself **before** the `helm upgrade`:

```sh
kubectl replace -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
```

Releases before v1.28.0 always need this manual CRD step.

_See [configuration](#configuration) below._

### Verify the upgrade

Confirm the client and server versions match, and run the cluster diagnostics:

```sh
fission version
fission check
```

## What happens during an upgrade

`helm upgrade` replaces the Fission control-plane pods, not your function pods.

### Pre-upgrade checks

A Helm hook Job runs before any manifest changes (`preUpgradeChecks.enabled`, default `true`).
The Job:

- applies the target version's CRD bundle (`crds.mode=hook`, the default), so controllers never run against stale schemas;
- confirms the latest CRD schema is live on the cluster;
- checks that every function references secrets, configmaps, and packages in its own namespace.

If a check fails, the upgrade stops before any component rolls, and the existing installation keeps running unchanged.

### Router

The router runs two replicas by default and rolls surge-first (`maxSurge: 1`, `maxUnavailable: 0`), so the serving replica count never dips.
A new router pod reports Ready only after it builds its route table and syncs its endpoint index.
A terminating router pod first sleeps for `router.preStopSleep` (default 5 seconds), so its removal from the Service propagates.
It then drains in-flight requests for up to `router.gracefulShutdownTimeout` (default `75s`).
A PodDisruptionBudget (`minAvailable: 1`) protects the router during node drains.
The chart renders the budget only when the router can satisfy it: two or more replicas, or an autoscaler with a floor of two.

### Warm function pods

Warm pods keep serving through the upgrade:

- The restarted executor **adopts** existing function Deployments and pods (`executor.adoptExistingResources`, default `true`) instead of recreating them.
- **Specialized** poolmgr pods survive executor-side template changes, such as a new fetcher image.
  The pool controller recycles them only when their environment changes.
- **Generic** (not yet specialized) pool pods roll and pick up the new images.
- Warm traffic does not need a live executor: the router serves warm requests directly from EndpointSlices.

### Executor

The executor is a single-writer control plane, so it rolls overlap-free (`maxSurge: 0`, `maxUnavailable: 1`).
The old pod stops before the new one starts.
This gives a bounded executor-down window per roll.
Warm traffic keeps serving throughout.
Only cold starts wait for the new executor pod.
To shorten failover, run `executor.replicas: 2` with `executor.leaderElection.enabled: true` (active-passive HA).

### Webhook

The validating webhook runs two replicas by default with a surge rollout and a PodDisruptionBudget, so Fission CR writes stay available while it rolls.
One caveat remains on the default certificate path: the chart mints a new serving certificate on every `helm upgrade`.
A short window can then reject CR writes while old pods still serve the old certificate.
Set `webhook.certManager.enabled=true` to let cert-manager manage a stable certificate and close that window.
Function invocations are not affected.
The webhook sits only on the CR write path.

### Embedded statestore

This applies only when `statestore.enabled=true` with `mode: embedded`.
The embedded statestore is a single-replica Deployment with `strategy: Recreate`, because two pods must never hold the SQLite file at once.
Its pod is therefore down for a short window during the upgrade.
Invocations already enqueued are durable on the persistent volume, and delivery resumes when the pod returns.
New [asynchronous enqueues](/docs/usage/function/async-invocation/) during that window fail, and the caller must retry.
`statestore.mode=external` (Postgres) has no such window; see [Statestore](/docs/architecture/statestore/).

## Tune the drain windows

### Function pods: `terminationGracePeriod`

Each environment sets how long its function pods drain before Kubernetes removes them: `spec.terminationGracePeriod`, default **90 seconds**.
A terminating function pod keeps serving for the whole window.
The preStop hook sleeps through it, then the kubelet kills the pod.
Set the window above your longest function timeout, or the slowest in-flight requests end with a connection reset:

```sh
fission env update --name node --graceperiod 180
```

The same window applies to every pod teardown: idle reap, environment update, upgrade, node drain.
A larger value makes each teardown take longer per pod.
An explicit `0` disables draining and removes pods instantly.
See the [`terminationGracePeriod` field reference](/docs/reference/crd-reference/#environmentspec).

### Router: grace period and shutdown timeout

Two chart values control the router drain, and they must move together:

```sh
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all \
  --set router.terminationGracePeriodSeconds=150 \
  --set router.gracefulShutdownTimeout=120s
```

Keep `terminationGracePeriodSeconds` greater than `gracefulShutdownTimeout`, and `gracefulShutdownTimeout` greater than your longest function timeout.
Raising the grace period alone does nothing: the drain still stops at `gracefulShutdownTimeout`.

## Upgrade to 1.28.x release

v1.28.0 flips the chart's rollout-posture defaults so that upgrades keep warm traffic serving:

- The **router** and the **webhook** default to two replicas each, with surge rollouts and PodDisruptionBudgets.
- The chart applies **CRDs** itself through the pre-upgrade hook (`crds.mode: hook`), so the manual `kubectl` CRD step is no longer part of the routine upgrade.

Small-footprint installs (kind, single node) can set `router.replicas=1` and `webhook.replicas=1` to keep the previous footprint; the PodDisruptionBudgets drop automatically at one replica.
Set `crds.mode=none` to keep delivering CRDs yourself.

See the [v1.28.0 release notes](/docs/releases/v1.28.0/#upgrade-notes) for the full list of changes.

## Upgrade to 1.27.x release

v1.27.0 adds opt-in multi-namespace tenancy and a function-developer observability toolkit (invocation correlation, `fission function describe`, and local `run-local` development).
Tenancy is off by default.
`tenancy.mode: static` renders byte-identical RBAC and keeps the existing auth model, so a single-namespace or `additionalFissionNamespaces` install upgrades with just the routine CRD/CLI/chart steps above.
The minimum Kubernetes version is unchanged at **1.32**.
To onboard namespaces at runtime with `fission tenant enable` instead of editing `additionalFissionNamespaces`, see [Multi-namespace tenancy](/docs/usage/multi-namespace-tenancy/).

Two runtime defaults change visibly and are worth reviewing first:

- The router now returns a structured JSON error body for attributed failures (status codes are unchanged).
  A client that parses the literal old plain-text body should read the JSON instead, or set `ROUTER_STRUCTURED_ERRORS=false` to restore it.
- Trace sampling now honors `OTEL_TRACES_SAMPLER`.
  If you export traces over OTLP, successful-trace volume drops to the documented `0.1` ratio (all error traces are still kept).
  Set `OTEL_TRACES_SAMPLER=parentbased_always_on` to keep 100% export.

See the [v1.27.0 release notes](/docs/releases/v1.27.0/#upgrade-notes) for the full list of behavioral changes and the action each one requires.

## Upgrade to 1.26.x release

v1.26.0 is a large feature release: OCI-native package delivery, the Kubernetes Gateway API route provider, streaming responses, functions as MCP tools, and an EndpointSlice-native router data plane.
There are no Kubernetes-version or admission changes from v1.25.0, so the routine CRD/CLI/chart steps above are all most installs need.

Two behavioral defaults are worth reviewing before you upgrade:

- The router now serves warm traffic directly from EndpointSlices and accounts request concurrency **per router replica** by default.
  Functions that depend on global concurrency enforcement should set the `fission.io/concurrency-enforcement: strict` annotation.
- When a package registry is configured (`packageRegistry.enabled`), builds publish their deployment archive as a digest-pinned OCI image and functions cold-start from it.
  Leave `packageRegistry.enabled` unset to keep today's tarball behavior unchanged.

See the [v1.26.0 release notes](/docs/releases/v1.26.0/#upgrade-notes) for the full list of behavioral changes and the action each one requires.

## Upgrade to 1.25.x release

v1.25.0 raises the minimum supported Kubernetes version to **1.32** and continues the security-hardening line.
Before upgrading, confirm your cluster is on Kubernetes 1.32 or newer — the Helm chart now refuses to install on anything older.

Three breaking changes need attention:

1. **Kubernetes 1.32 minimum.**
   Clusters below 1.32 are rejected by the chart's `kubeVersion` constraint and fail the runtime `fission check` floor.
   The fluentbit `PodSecurityPolicy` manifest and the `logger.podSecurityPolicy` Helm value are removed (PSP no longer exists in Kubernetes 1.32).
   Use Pod Security Admission instead.
2. **HTTPTrigger path validation at admission.**
   Empty paths, `..` traversal, root-only `/`, and paths that collide with router-owned routes (`/router-healthz`, `/readyz`, `/_version`, `/auth/login`) or shadow `/fission-function/<ns>/<name>` are now rejected.
   The `fission` CLI already enforced these.
   Raw `kubectl apply` no longer bypasses them.
   Fix offending trigger paths before upgrading.
3. **PodSpec capabilities are an allowlist.**
   `Environment` and `Function` PodSpecs may only add `NET_BIND_SERVICE`.
   Every container is forced to `drop: ["ALL"]`.
   Specs that added other capabilities are rejected, and workloads that silently relied on the OCI default cap set will see those caps stripped.

The HTTPTrigger / TimeTrigger / CanaryConfig admission webhooks are also removed in favor of API-server CEL validation.
A side effect: a raw `kubectl apply` of an invalid cron schedule, CORS origin, or ingress path is now admitted rather than rejected at creation.
It is instead **flagged with a `…=False` status condition** (for example `Scheduled=False`, `RouteAdmitted=False`).
The `fission` CLI still rejects these client-side, so the common path is unchanged.

See the [v1.25.0 release notes](/docs/releases/v1.25.0/#upgrade-notes) for the full list of breaking changes and the action each one requires.

## Upgrade to 1.24.x release

v1.24.0 is a security-hardening release.
The admission webhooks now reject cross-namespace references and dangerous PodSpec fields, and deny cross-origin browser requests by default.
They also stop mounting the `fission-builder` ServiceAccount token into user builder containers.
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
Upstream `ghcr.io/fission/keda-kafka-http-connector` (and the other `keda-*-http-connector` images) do not yet sign their `/fission-function/...` invocations.
KEDA-driven message-queue triggers therefore receive `401` from the new router internal listener.

If your installation uses KEDA-backed `MessageQueueTrigger` resources, **set `internalAuth.enabled=false` at upgrade time** until signing-aware KEDA connector images ship:

```sh
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all \
  --set internalAuth.enabled=false
```

With `enabled=false`, every signer/verifier short-circuits to pass-through and the cluster falls back to `NetworkPolicy` + namespace isolation alone — matching pre-1.23 in-cluster behavior.

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
