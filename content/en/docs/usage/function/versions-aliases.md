---
title: "Function Versions and Aliases"
draft: false
weight: 49
description: >
  Publish immutable versions of a function, route traffic through movable aliases like prod and staging, split traffic between two versions, and roll back instantly — without touching triggers or paying a cold start.
---

**Publish a function as immutable versions, point named aliases like `prod` and `staging` at them, and roll back a bad deploy in seconds — without editing a single trigger and without a cold start.**

A plain `fission fn update` changes the live function in place: every trigger that names the function immediately serves the new code, and the only way back is another update.
Starting with Fission {{< release-version >}}, a function can also have **versions** and **aliases**:

- A **version** (`FunctionVersion`, `kubectl get fnver`) is an immutable snapshot of the function's spec and package content at publish time, named `<function>-v<sequence>` (for example `orders-v3`).
  It is never mutated after creation, only garbage collected once nothing references it.
- An **alias** (`FunctionAlias`, `kubectl get fnalias`) is a movable, named pointer at one version — or at two versions during a weighted traffic split.
  Triggers reference the alias; moving the alias is how a rollout or a rollback happens.

```mermaid
flowchart LR
  api["/api route"]:::user --> prod["alias: prod"]:::fission
  beta["/beta route"]:::user --> staging["alias: staging"]:::fission
  prod --> v3["orders-v3"]:::pod
  staging --> v4["orders-v4"]:::pod

  classDef user fill:#ffffff,stroke:#94a3b8,color:#1f2a43
  classDef fission fill:#e8f0fe,stroke:#2d70de,color:#1f2a43
  classDef pod fill:#e6f7f1,stroke:#11a37f,color:#1f2a43,stroke-dasharray:5 3
```

This is fully backward compatible.
A trigger that references a bare function name keeps meaning "the live function", exactly as before — nothing changes until you publish a version and point something at it.

## Publish a version

`fission fn publish` snapshots the function's current spec and package content as the next version:

```bash
$ fission fn update --name orders --code orders-v2.js
function 'orders' updated

$ fission fn publish --name orders --description "checkout rounding fix"
created orders-v3
```

Publishing is idempotent: if nothing runtime-affecting changed since the last publish, the existing newest version is returned instead of minting a duplicate:

```bash
$ fission fn publish --name orders
unchanged orders-v3
```

| Flag | Meaning |
| --- | --- |
| `--description` | Human-readable note recorded on the version. |
| `--wait` | Wait for the function's package build to finish before publishing (see `--timeout`); without it, publishing against a still-building package fails fast. |
| `-o name` | Print only the version name, for scripting. |
| `-o json` / `-o yaml` | Print the full version object. |

Versions can also be minted automatically on every runtime-affecting update — see [automatic publishing]({{% ref "versions-lifecycle.md#automatic-publishing" %}}).

## List versions

```bash
$ fission fn versions --name orders
NAME      SEQUENCE DIGEST              PUBLISHED            AGE
orders-v1 1        sha256:1f8ac10f23c5 2026-07-10T09:14:02Z 14d
orders-v2 2        sha256:60303ae22b99 2026-07-17T16:41:55Z 7d
orders-v3 3        sha256:fd61a03af4f7 2026-07-24T08:03:11Z 2m
```

The `DIGEST` column pins the exact package content of each version.
The table truncates it; `-o wide` prints full digests and adds an `ENVDRIFT` column showing whether the version was published under an older generation of its environment (see [environment updates and drift]({{% ref "versions-lifecycle.md#environment-updates-and-drift" %}})).
`-o json` / `-o yaml` print the full objects.

## Point an alias at a version

```bash
$ fission alias create --name prod --function orders --version orders-v3
function alias 'prod' created

$ fission alias list
NAME    FUNCTION VERSION   PACKAGE-DIGEST WEIGHT SECONDARY-VERSION RESOLVED-VERSION
prod    orders   orders-v3                <none>                   orders-v3
staging orders   orders-v4                <none>                   orders-v4
```

`fission alias get --name prod` shows the same row plus the alias's status conditions, and `fission alias delete --name prod` removes it.
An alias lives in the same namespace as its function, and one function can have any number of aliases.

## Route triggers through the alias

A trigger targets an alias through the optional `alias` field on its function reference.
The router resolves the alias **at request time**, so repointing the alias redirects traffic without touching the trigger.

The `fission` CLI has no dedicated flag for this yet, so set the field declaratively.
Either write the trigger with `--spec` and edit the generated file, or apply YAML directly:

```yaml
apiVersion: fission.io/v1
kind: HTTPTrigger
metadata:
  name: orders-api
  namespace: default
spec:
  relativeurl: /api/orders
  methods:
    - POST
  functionref:
    type: name
    name: orders
    alias: prod
```

Different routes can target different aliases of the **same** function:

```yaml
# /api/orders -> alias prod (stable), /beta/orders -> alias staging (next)
functionref:
  type: name
  name: orders
  alias: prod
---
functionref:
  type: name
  name: orders
  alias: staging
```

To pin a route permanently to one immutable snapshot instead, set `functionref.version: orders-v3` — unlike an alias, a version pin never moves.
`alias` and `version` are mutually exclusive, and both are valid on every trigger kind that embeds a function reference (HTTP, message queue, timer, Kubernetes watch).

## Deploy by moving the alias

A deploy becomes: publish, then repoint.

```bash
$ fission fn update --name orders --code orders-v3.js
function 'orders' updated

$ fission fn publish --name orders --wait
created orders-v4

$ fission alias update --name prod --version orders-v4 --wait
function alias 'prod' updated
function alias 'prod' resolved
```

`--wait` blocks until the alias's `Resolved` condition reports the new target, so a CI job can gate the next step on the switch actually happening.
You can also wait separately: `fission alias wait --name prod --for condition=Resolved`.

### Weighted traffic splits

An alias can spread traffic across two versions — the primary gets `--weight` percent, the secondary gets the rest:

```bash
$ fission alias update --name prod --version orders-v3 --weight 90 --secondary-version orders-v4
function alias 'prod' updated
```

Now 90% of requests through `prod` run `orders-v3` and 10% run `orders-v4`.
Step `--weight` down as confidence grows, then finish with a full repoint:

```bash
$ fission alias update --name prod --version orders-v4 --clear-weight
function alias 'prod' updated
```

`--weight` requires `--secondary-version`, and `--clear-weight` drops the split (it wins if combined with other flags in the same call).
To have Fission step the weight for you based on error rates, drive the split with a [canary config over the alias]({{% ref "versions-lifecycle.md#canary-rollouts-over-an-alias" %}}).

## Instant rollback

`fission fn rollback` repoints one alias back at a previous version — atomically, and without recycling any pods:

```bash
$ fission fn rollback --name orders --alias prod --wait
function alias 'prod' rolled back: orders-v4 -> orders-v3
function alias 'prod' resolved
```

By default the alias returns to its **previous target**, which Fission records in the alias's history on every switch.
Pass `--to` to pick any version explicitly:

```bash
$ fission fn rollback --name orders --alias prod --to orders-v1
function alias 'prod' rolled back: orders-v3 -> orders-v1
```

Three properties make this safe to reach for during an incident:

- **No cold start.**
  A version that any alias references keeps at least one specialized pod warm, so the rollback target is already running when traffic arrives.
- **Full repoint.**
  A rollback clears any weighted split, so a rollback issued mid-canary stops the split entirely rather than rolling back only the primary side.
- **Atomic.**
  The alias flips in a single update; there is no window where triggers see a half-moved state.

### Rolling back a GitOps-managed alias

If the alias is owned by a `fission spec` directory (deployed with `fission spec apply`), a bare rollback is refused:

```bash
$ fission fn rollback --name orders --alias prod
Error: function alias 'prod' is managed by `fission spec` (Git); the next spec apply will revert this rollback. Re-run with --detach to strip spec ownership, and update your Git repo: set spec.version: orders-v3 in the FunctionAlias manifest
```

The guard exists because the next `fission spec apply` would reconcile the alias back to whatever `spec.version` says in Git — silently undoing the rollback.
You have two options:

- **Git-first (preferred):** change `spec.version` in the FunctionAlias manifest in your repository and let the pipeline apply it.
- **Emergency:** re-run with `--detach`, which strips the spec-ownership annotations in the same update as the repoint, so a later `spec apply` no longer reverts it.
  Update the manifest afterwards, then re-apply to re-adopt the alias.

## Declarative aliases and digest pinning

Aliases are ordinary objects in a [spec directory]({{% ref "/docs/usage/spec/_index.md" %}}), so a Git repository can own them:

```yaml
apiVersion: fission.io/v1
kind: FunctionAlias
metadata:
  name: prod
  namespace: default
spec:
  functionName: orders
  version: orders-v3
```

For pipelines that build content before versions exist, an alias can pin by **package digest** instead of by version name:

```yaml
spec:
  functionName: orders
  packageDigest: sha256:fd61a03af4f77d870fc21e05e7e80678095c92d808cfb3b5c279ee04c74aca13
```

The pipeline commits the content hash it built; Fission resolves the digest to the version that recorded it, asynchronously, once that version exists.
Because resolution is eventually consistent, gate on it in CI:

```bash
$ fission alias wait --name prod --for condition=Resolved --timeout 120s
```

`version` and `packageDigest` are mutually exclusive — exactly one must be set.
Promotion between environments is then just two aliases converging: point `staging` at a new version, test through the staging route, and promote by repointing `prod` at the **same** version — the identical immutable snapshot, not a rebuild.

Versions themselves are deliberately **not** spec-managed: the cluster mints them, and Git references them by name or digest.

## Related

- [Version lifecycle and interactions]({{% ref "versions-lifecycle.md" %}}) — automatic publishing, retention, environment drift, and how versions interact with async invocation, canaries, and state.
- [Canary deployments]({{% ref "canary-deployments.md" %}}) — automated, metrics-driven weight stepping.
- [Declarative specs]({{% ref "/docs/usage/spec/_index.md" %}}) — the `fission spec` workflow that can own aliases.
- [Create and run functions]({{% ref "functions.en.md" %}}) — the everyday function workflow.
