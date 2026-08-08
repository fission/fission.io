---
title: "Internal Service Authentication"
weight: 45
description: >
  HMAC-signed authentication for Fission's internal control-plane RPCs
---

**Fission signs internal control-plane RPCs with application-layer HMAC authentication, enabled by default since [v1.23.0]({{% ref "../releases/v1.23.0.md" %}}).**
This is distinct from the end-user [function-invocation authentication]({{% ref "authentication.md" %}}) (JWT, opt-in), which protects function invocations rather than in-cluster RPCs.

## What it protects

Five internal channels now require signed requests when `internalAuth.enabled=true`:

| Service | Server endpoint(s) | Callers |
|---|---|---|
| `storagesvc` | `/v1/archive` | buildermgr and fetcher uploading function archives |
| `fetcher` (per-pod sidecar) | `/fetch`, `/specialize`, `/upload` | buildermgr, executor |
| `builder` (per-pod) | `/build` | buildermgr |
| `executor` | `/v2/getServiceForFunction`, `/v2/tapService`, `/v2/unTapService`, … | router |
| `router-internal` (port `8889`) | `/fission-function/<ns>/<name>` | executor, kubewatcher, timer, mqt-fission-kafka |

Each pair derives a per-service key via HKDF from a single chart-managed master secret, so one toggle gates all five channels atomically.

## Key behavioral change in v1.23.0

The router now binds **two listeners**:

- **Public listener** (port `8888`) — serves user `HTTPTrigger` paths, `/router-healthz`, `/_version`, and (when enabled) the JWT-based [function-invocation auth]({{% ref "authentication.md" %}}).
- **Internal listener** (port `8889`) — serves `/fission-function/<ns>/<name>` only, gated by `NetworkPolicy` plus HMAC verification.

**`/fission-function/<ns>/<name>` no longer exists on the public listener.** This closes [GHSA-3g33-6vg6-27m8](https://github.com/fission/fission/security/advisories/GHSA-3g33-6vg6-27m8) — previously anyone reachable to the public router URL (e.g. via Ingress) could invoke any function by guessing its name, bypassing all `HTTPTrigger` host/path/method gates.

Any external tooling that today curls `/fission-function/...` against the public router URL will receive **404** after upgrading.
The public listener is unchanged for user `HTTPTrigger` traffic.

## Default install

`internalAuth.enabled` defaults to `true` from v1.23.0 onwards:

```bash
helm install fission fission-charts/fission-all -n fission --create-namespace
```

The chart materializes a `Secret/fission-internal-auth` with an auto-generated 32-byte master key.
The same value is preserved across `helm upgrade` runs.
Under static tenancy the chart replicates the Secret into `defaultNamespace` and each `additionalFissionNamespaces` entry, so dynamically created builder and function pods can mount it too.
Every Fission control-plane component (storagesvc, executor, router, buildermgr, and the rest) and every dynamically-created builder/function pod mounts the master via environment variable; each signer/verifier pair derives its own per-service key.

### Fail-closed startup check

Every binary — fission-bundle, fetcher, builder, and the CLI — validates the internal-auth environment at startup.
An absent `FISSION_INTERNAL_AUTH_SECRET` means internal auth is off; signers and verifiers pass through.
A present but blank value is refused: the process exits with an error that names the variable.
This closes the one misconfiguration that previously failed open — a Secret with an empty `secret` key silently disabled HMAC verification.
The same check covers the rotation variable `FISSION_INTERNAL_AUTH_SECRET_OLD`.

## Bring your own master secret

Pass an explicit master secret at install time to skip the auto-generated key:

```bash
helm install fission fission-charts/fission-all -n fission \
  --set internalAuth.secret="$(openssl rand -base64 32)"
```

If `internalAuth.secret` is set, the chart honors it instead of auto-generating one.

## Use a pre-created Secret (`existingSecret`)

Point the chart at a Secret you create and manage yourself:

```bash
kubectl create secret generic fission-auth-master -n fission \
  --from-literal=secret="$(openssl rand -base64 32)"

helm install fission fission-charts/fission-all -n fission \
  --set internalAuth.existingSecret=fission-auth-master
```

The Secret must hold the key `secret`, and during rotation the optional key `oldSecret`.
With `internalAuth.existingSecret` set, the chart renders no master Secret; every component reads yours.

Create the Secret in every namespace where Fission runs pods: the release namespace, `defaultNamespace`, and each `additionalFissionNamespaces` entry.
kubelet cannot resolve a cross-namespace `secretKeyRef`, so a single copy in the release namespace leaves builder and function pods starting but returning 401 on every archive fetch and builder upload.
Under dynamic or cluster tenancy, only the release namespace needs the Secret.

This is the recommended path for GitOps renderers (Argo CD, Flux).
Those run `helm template`, where the chart cannot preserve a generated value across syncs — each sync would mint a new master and break every running pod.
Switching an existing install to `existingSecret` is safe: a pre-upgrade hook marks the chart-generated Secret with `helm.sh/resource-policy=keep`, so Helm does not prune it.

As an alternative for GitOps, `internalAuth.autoGenerate=true` (default `false`) moves generation into a pre-install/pre-upgrade hook that creates the master Secret in-cluster only if it is absent, so no renderer re-mints it.
The hook is admission-fenced by a `ValidatingAdmissionPolicy`: it can create only the master Secret, and only as a plain `Opaque` object.

The CLI discovers the Secret name from the cluster it talks to.
The precedence is: an explicit `FISSION_INTERNAL_AUTH_SECRET_NAME` environment variable, then the name stamped on the executor Deployment, then the default `fission-internal-auth`.
If your CLI user cannot read Deployments and the install uses a non-default name, set `FISSION_INTERNAL_AUTH_SECRET_NAME` explicitly.

## Disable everywhere

Turn off signing across all five channels at install time:

```bash
helm install fission fission-charts/fission-all -n fission \
  --set internalAuth.enabled=false
```

With `enabled=false` the chart skips the `Secret` and the env mounts.
Every signer/verifier short-circuits to pass-through — no signing, no verification — so the cluster falls back to `NetworkPolicy` + namespace isolation alone for in-cluster trust.

This is the **recommended setting if you rely on stock upstream KEDA connector images** (`ghcr.io/fission/keda-kafka-http-connector` and the other `keda-*-http-connector` images) — see [Caveats](#caveats) below.

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

`helm uninstall` no longer removes the master Secret: the chart marks it `helm.sh/resource-policy=keep`, and a reinstall reuses the surviving value.
To force a rotation after a suspected compromise, delete `Secret/fission-internal-auth` in every namespace it was replicated into, or set new values for `internalAuth.secret`.

## Toggle interaction matrix

The verifier (server) and signer (client) toggles are set independently per rollout, so mixed states are possible; this table shows the outcome of each combination:

| Server (verifier) | Client (signer) | Outcome |
|---|---|---|
| OFF | OFF | All requests pass through unsigned — identical to pre-v1.23 in-cluster behavior |
| ON | ON | All signed and verified per-service (default) |
| ON | OFF | Client request returns **401** |
| OFF | ON | Client sends signed headers; server pass-through ignores them — works |

The chart applies the toggle wholesale, so the "ON / OFF" failure mode only surfaces during hand-edited deployments, in-flight `helm upgrade` rollouts where some pods haven't rolled yet, or external tooling that signed against an unconfigured CLI.

## Caveats

### KEDA connector signing gap

Upstream `ghcr.io/fission/keda-kafka-http-connector` (and the other `keda-*-http-connector` images) **do not yet sign their `/fission-function/...` invocations**.
With `internalAuth.enabled=true` (the default), KEDA-driven message-queue triggers will receive `401` from the router internal listener.

Operators have two options until signing-aware KEDA images ship:

1. **Build signing-aware connector images** (recommended long-term). The signer primitive lives in `pkg/auth/hmac` in the Fission repo.
2. **Set `internalAuth.enabled=false`** and rely on `NetworkPolicy` alone for the KEDA traffic. The internal listener still hosts `/fission-function/<ns>/<name>` but does not enforce signatures.

### `ROUTER_INTERNAL_URL`

Services that publish to the router internal listener (`kubewatcher`, `timer`, `mqt-fission-kafka`, `mqt-keda`) now read `ROUTER_INTERNAL_URL`.
The chart sets it to `http://router-internal.<namespace>:<router.internalPort>` (port `8889` by default) using the dedicated `router-internal` Service.
If you customize the router `Service` name, namespace, or `router.internalPort`, set this env override accordingly.

## Reference

- [GHSA-3g33-6vg6-27m8](https://github.com/fission/fission/security/advisories/GHSA-3g33-6vg6-27m8) — router public-listener function-invocation exposure (fixed by the two-listener split)
- [PR #3368](https://github.com/fission/fission/pull/3368) — initial HMAC wiring on `storagesvc`
- [PR #3369](https://github.com/fission/fission/pull/3369) — extension to `fetcher`, `builder`, `executor`, `router-internal`
