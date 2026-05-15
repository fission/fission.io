---
title: "Internal Service Authentication"
weight: 45
description: >
  HMAC-signed authentication for Fission's internal control-plane RPCs
---

Starting with [v1.23.0](/docs/releases/v1.23.0/), Fission ships **application-layer HMAC authentication** for the internal HTTP channels between its control-plane services.
This is distinct from the end-user [function-invocation authentication](/docs/installation/authentication/) (JWT, opt-in): internal auth protects in-cluster RPCs and is **enabled by default**.

## What it protects

Five internal channels now require signed requests when `internalAuth.enabled=true`:

| Service | Server endpoint(s) | Callers |
|---|---|---|
| `storagesvc` | `/v1/archive` | controllers uploading function archives |
| `fetcher` (per-pod sidecar) | `/fetch`, `/upload`, `/clean`, `/specialize` | buildermgr, executor |
| `builder` (per-pod) | `/build` | buildermgr |
| `executor` | `/v2/getServiceForFunction`, `/v2/tap`, `/v2/error`, … | router, kubewatcher, timer, mqt-fission-kafka, canaryconfig |
| `router-internal` (port `8889`) | `/fission-function/<ns>/<name>` | executor, kubewatcher, timer, mqt-fission-kafka |

Each pair derives a per-service key via HKDF from a single chart-managed master secret, so one toggle gates all five channels atomically.

## Key behavioral change in v1.23.0

The router now binds **two listeners**:

- **Public listener** (port `8888`) — serves user `HTTPTrigger` paths, `/router-healthz`, `/_version`, and (when enabled) the JWT-based [function-invocation auth](/docs/installation/authentication/).
- **Internal listener** (port `8889`) — serves `/fission-function/<ns>/<name>` only, gated by `NetworkPolicy` plus HMAC verification.

**`/fission-function/<ns>/<name>` no longer exists on the public listener.** This closes [GHSA-3g33-6vg6-27m8](https://github.com/fission/fission/security/advisories/GHSA-3g33-6vg6-27m8) — previously anyone reachable to the public router URL (e.g. via Ingress) could invoke any function by guessing its name, bypassing all `HTTPTrigger` host/path/method gates.

Any external tooling that today curls `/fission-function/...` against the public router URL will receive **404** after upgrading.
The public listener is unchanged for user `HTTPTrigger` traffic.

## Default install

`internalAuth.enabled` defaults to `true` from v1.23.0 onwards:

```bash
helm install fission fission-charts/fission-all -n fission --create-namespace
```

The chart materialises a `Secret/fission-internal-auth` with an auto-generated 32-byte master key.
The same value is preserved across `helm upgrade` runs.
Every controller, executor, router, and dynamically-created builder/function pod mounts the master via environment variable; each signer/verifier pair derives its own per-service key.

## Bring your own master secret

```bash
helm install fission fission-charts/fission-all -n fission \
  --set internalAuth.secret="$(openssl rand -base64 32)"
```

If `internalAuth.secret` is set, the chart honours it instead of auto-generating one.

## Disable everywhere

```bash
helm install fission fission-charts/fission-all -n fission \
  --set internalAuth.enabled=false
```

With `enabled=false` the chart skips the `Secret` and the env mounts.
Every signer/verifier short-circuits to pass-through — no signing, no verification — so the cluster falls back to `NetworkPolicy` + namespace isolation alone for in-cluster trust.

This is the **recommended setting if you rely on stock upstream KEDA connector images** (`fission/kafka-http-connector` and friends) — see [Caveats](#caveats) below.

The router's two-listener split is independent of this toggle: `/fission-function/<ns>/<name>` remains on the internal listener regardless.
With `internalAuth.enabled=false` the internal listener still accepts unsigned requests; with `internalAuth.enabled=true` it requires signatures.

## Master-secret rotation

The master secret can be rotated without downtime using the `oldSecret` overlap field:

```bash
# Step 1 — pin the live secret as `oldSecret` so verifiers accept both.
LIVE=$(kubectl -n fission get secret fission-internal-auth -o jsonpath='{.data.secret}' | base64 -d)
helm upgrade fission fission-charts/fission-all -n fission \
  --set internalAuth.oldSecret="$LIVE"

# Step 2 — roll in the new master.
helm upgrade fission fission-charts/fission-all -n fission \
  --set internalAuth.secret="$(openssl rand -base64 32)"

# Step 3 — wait for every Fission deployment to finish rolling.

# Step 4 — drop the old secret.
helm upgrade fission fission-charts/fission-all -n fission \
  --set internalAuth.oldSecret=""
```

Because every per-service key is derived from the master via HKDF, this single sequence rotates the key for all five channels atomically.

## Toggle interaction matrix

| Server (verifier) | Client (signer) | Outcome |
|---|---|---|
| OFF | OFF | All requests pass through unsigned — identical to pre-v1.23 in-cluster behaviour |
| ON | ON | All signed and verified per-service (default) |
| ON | OFF | Client request returns **401** |
| OFF | ON | Client sends signed headers; server pass-through ignores them — works |

The chart applies the toggle wholesale, so the "ON / OFF" failure mode only surfaces during hand-edited deployments, in-flight `helm upgrade` rollouts where some pods haven't rolled yet, or external tooling that signed against an unconfigured CLI.

## Caveats

### KEDA connector signing gap

Upstream `fission/kafka-http-connector` (and the other Fission KEDA connector images) **do not yet sign their `/fission-function/...` invocations**.
With `internalAuth.enabled=true` (the default), KEDA-driven message-queue triggers will receive `401` from the router internal listener.

Operators have two options until signing-aware KEDA images ship:

1. **Build signing-aware connector images** (recommended long-term). The signer primitive lives in `pkg/auth/hmac` in the Fission repo.
2. **Set `internalAuth.enabled=false`** and rely on `NetworkPolicy` alone for the KEDA traffic. The internal listener still hosts `/fission-function/<ns>/<name>` but does not enforce signatures.

### `ROUTER_INTERNAL_URL`

Services that publish to the router internal listener (`kubewatcher`, `timer`, `mqt-fission-kafka`, `mqt-keda`) now read `ROUTER_INTERNAL_URL`.
The chart sets it to `http://router.fission.svc:8889` by default.
If you customise the router `Service` name, namespace, or `router.internalPort`, set this env override accordingly.

## Reference

- [GHSA-3g33-6vg6-27m8](https://github.com/fission/fission/security/advisories/GHSA-3g33-6vg6-27m8) — router public-listener function-invocation exposure (fixed by the two-listener split)
- [PR #3368](https://github.com/fission/fission/pull/3368) — initial HMAC wiring on `storagesvc`
- [PR #3369](https://github.com/fission/fission/pull/3369) — extension to `fetcher`, `builder`, `executor`, `router-internal`
