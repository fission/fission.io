---
title: "Version Lifecycle and Interactions"
draft: false
weight: 50
description: >
  Mint function versions automatically on every update, bound version history with retention GC, track environment drift, and understand how versions interact with async invocation, canaries, state, and other triggers.
---

**How function versions are minted automatically, how old ones are cleaned up, what an environment update means for rollback, and how every other Fission feature behaves when traffic flows through an alias.**

This page continues from [Function versions and aliases]({{% ref "versions-aliases.md" %}}), which covers publishing, aliases, routing, and rollback.

## Automatic publishing

Instead of calling `fission fn publish` after every deploy, a function can opt into minting versions automatically.
Opt in from the CLI with `--versioning`, on either `fission fn create` or `fission fn update`:

```bash
$ fission fn update --name orders --versioning auto
Function 'orders' updated

$ fission fn update --name orders --versioning auto --retain-versions 10
Function 'orders' updated
```

`--versioning` takes `auto` (the default once versioning is enabled), `manual`, or `off`.
`off` is only meaningful on `fn update` — it clears the versioning config; on `fn create` there is nothing to clear yet, so omitting `--versioning` and passing `--versioning off` are equivalent.
`--retain-versions` sets the retention floor (see below) and requires versioning to already be enabled — pass `--versioning` in the same command, or add `--retain-versions` on its own once the function already carries a `versioning` block.
`--retain-versions` is distinct from `--retainpods`, which controls how many specialized pods stay warm — not how many function versions are kept.

The same fields are also settable directly on the function's spec — in a [spec file]({{% ref "/docs/usage/spec/_index.md" %}}) or with `kubectl patch`, if you'd rather manage it that way:

```yaml
apiVersion: fission.io/v1
kind: Function
metadata:
  name: orders
spec:
  # ...
  versioning:
    mode: auto    # "auto" is the default once versioning is present
    retain: 10    # optional; see retention below
```

```bash
$ kubectl patch function orders --type merge -p '{"spec":{"versioning":{"mode":"auto","retain":10}}}'
```

In `auto` mode, Fission publishes a new version after every **runtime-affecting** update — a change to what actually runs or is observable by an invocation, such as new code, a changed entry point, or changed resources.
Cosmetic edits (labels, annotations) do not mint versions.

The version is minted only **after the referenced package build succeeds**, so a broken build never becomes a version an alias could point at.
If a build is in flight when you update, the version appears when the build completes.

Set `--versioning manual` (or `mode: manual` in the spec) to keep versioning opted in (retention GC, alias support) but mint versions only on explicit `fission fn publish`.
`fission fn publish` itself works on any function, whether or not `spec.versioning` is set.

## Retention

Version history is bounded per function so old snapshots do not accumulate forever:

- `spec.versioning.retain` bounds how many **unaliased** versions are kept (default 10, minimum 1).
- A version referenced by any alias is **never** garbage collected, no matter how old.
- The newest version is never deleted.

The sweep runs automatically for opted-in functions.
Run one on demand — for example to preview a lower retain value before committing it to the spec — with:

```bash
$ fission fn gc-versions --name orders --keep 5
deleted 3, skipped 1, retained 5
```

`skipped` counts versions that were beyond the keep floor but protected by an alias reference.

## Environment updates and drift

Versions snapshot the function's **code and configuration** — not the environment's runtime image.
An environment update (say, bumping `node` to a new image) recycles pods under **every** version of every function using it; it sits outside the version boundary entirely.
That has one operational consequence worth internalizing:

{{% notice warning %}}
Rolling back an alias restores the function's code and configuration, **not** the runtime image it originally ran on.
If an incident started with an environment update, roll the environment back too.
{{% /notice %}}

Fission surfaces this drift in three places:

**On the alias**, as an `EnvDrift` condition, set when the alias's resolved version was published under an older generation of its environment.

**On rollback**, as a non-blocking warning:

```bash
$ fission fn rollback --name orders --alias prod
WARNING: target version orders-v2 was published under env default/node generation 4; live env is generation 5 — rollback restores code/config, not the runtime image
function alias 'prod' rolled back: orders-v3 -> orders-v2
```

**Before an environment update**, as a blast-radius report.
`fission env impact` lists every function referencing the environment, each of its aliases, and whether each alias's current target already drifts:

```bash
$ fission env impact --name node
FUNCTION ALIAS   TARGET-VERSION ENV-OBSERVED-GEN LIVE-GEN DRIFT
orders   prod    orders-v2      4                5        True
orders   staging orders-v3      5                5        False
reports  <none>  <none>         <none>           5        <none>
```

`DRIFT` is `True` (published under an older environment generation), `False` (current), `OtherEnv` (the version was published when the function still used a different environment), or `<none>` (no alias or not assessable).
`fission fn versions --name orders -o wide` shows the same verdict per version in its `ENVDRIFT` column.

## How other invocation paths behave

HTTP triggers are not the only way traffic reaches a function.
Every path has a defined relationship with aliases and versions:

| Path | Behavior with an alias |
| --- | --- |
| HTTP trigger | Resolved at **request time**: repointing the alias redirects the very next request. |
| Message queue, timer, and Kubernetes watch triggers | Resolved at **delivery/firing time**: the invocation runs whatever the alias points at when the event fires, so you upgrade consumers by moving the alias — without redeploying any trigger. |
| [MCP tools]({{% ref "mcp-tools.md" %}}) | Resolved at **call time**, like HTTP: an LLM agent's tool call runs the alias's current target. |
| [Async invocation]({{% ref "async-invocation.md" %}}) retries | Pinned at **enqueue time**: an async invocation records the version it resolved to when accepted, and every retry re-runs that same version — retries stay deterministic even across a rollback. |
| [Keyed state]({{% ref "keyed-state.md" %}}) | **Shared across versions**: state belongs to the function, not to a version, so a rollback rolls back code, never data. |
| Sticky sessions | A session key stays on **one version** through a weighted split, so a user is not bounced between old and new behavior mid-session. |

## Canary rollouts over an alias

A weighted alias is the manual form of a canary; a [CanaryConfig]({{% ref "canary-deployments.md" %}}) automates the stepping.
When the canary's HTTP trigger references an alias, `--newfn` and `--oldfn` name two **versions** of the alias's function (see `fission fn versions`) — not two functions:

```bash
$ fission alias create --name prod --function orders --version orders-v3
function alias 'prod' created

$ fission canary create --name orders-canary --httptrigger orders-api \
    --newfn orders-v4 --oldfn orders-v3 \
    --increment-step 20 --increment-interval 2m --failure-threshold 10
```

The canary controller then steps the alias's weight toward `orders-v4`, watching the error rate.
On success it promotes: the alias is repointed fully at the new version.
On failure it rolls back: traffic returns to `orders-v3` — which is still warm, because the alias never stopped referencing it.

Prefer this over the classic two-function canary pattern (deploying `orders-v2` as a separate function next to `orders`): with versions there is nothing to duplicate, the history stays on one function, and cleanup is automatic via retention.
The classic pattern keeps working unchanged.

## Related

- [Function versions and aliases]({{% ref "versions-aliases.md" %}}) — publishing, aliases, weighted splits, rollback, and GitOps workflows.
- [Canary deployments]({{% ref "canary-deployments.md" %}}) — the full canary reference, including the metrics setup.
- [Asynchronous invocation]({{% ref "async-invocation.md" %}}) — durable fire-and-forget delivery.
- [Function state]({{% ref "keyed-state.md" %}}) — durable per-key state shared by all versions of a function.
