---
title: "Statestore"
weight: 16
description: >
  A durable state substrate — key/value, an append-only event log, and a visibility-timeout queue — behind one interface with pluggable drivers.
---

**The statestore is the durable substrate the control plane writes to when a feature needs state that outlives a single request or a single pod.**

It exposes three capabilities behind one interface — a **key/value** store, an append-only **event log**, and a visibility-timeout **queue** — served by a pluggable driver.
Fission itself never deploys a database product: you either use the bundled embedded driver for development, or point the external driver at a database you already run.

The statestore is what makes Fission's newer durable features possible.
Starting with Fission {{< release-version >}}, three subsystems build on it:

- **[Durable Workflows]({{% ref "/docs/usage/workflows/_index.md" %}})** record every step of a run in the event log, so a run survives a controller restart and resumes exactly where it stopped.
- **[Asynchronous invocation]({{% ref "/docs/usage/function/async-invocation.md" %}})** enqueues each fire-and-forget call on the queue and delivers it in the background with retries and a dead-letter queue.
- **Eventing** uses the event log and queue as its zero-broker transport.

The statestore is off by default; a feature that needs it will tell you to enable it.

```mermaid
flowchart TB
  wf["Workflow Engine"]:::fission
  async["Async Router / Worker"]:::fission
  evt["Eventing"]:::fission
  subgraph ss["Statestore"]
    kv["Key/Value"]:::store
    log["Event Log (append-only, CAS)"]:::store
    queue["Queue (visibility timeout)"]:::store
  end
  driver["Driver"]:::fission
  embedded["SQLite on a PVC<br/>(embedded)"]:::pod
  external["Postgres via DSN Secret<br/>(external)"]:::pod

  wf --> log
  async --> queue
  evt --> log
  evt --> queue
  kv --> driver
  log --> driver
  queue --> driver
  driver -->|"embedded"| embedded
  driver -->|"external"| external

  classDef fission fill:#e8f0fe,stroke:#2d70de,color:#1f2a43
  classDef pod fill:#e6f7f1,stroke:#11a37f,color:#1f2a43,stroke-dasharray:5 3
  classDef store fill:#fff7e0,stroke:#dba514,color:#1f2a43,stroke-dasharray:5 3
```

## Embedded vs external

The driver is chosen with `statestore.mode`.
The two modes differ only in where the state lives; the interface the features use is identical.

| Mode | Driver | Where state lives | Use it for |
| --- | --- | --- | --- |
| `embedded` | SQLite | A bundled SQLite file on a `PersistentVolumeClaim` | Development, single-node, and evaluation. Simple to run; not highly available. |
| `external` | Postgres | A database **you** run and manage | Production, high availability, and anything that needs KEDA autoscaling. |

{{% notice warning %}}
KEDA autoscaling for asynchronous invocation requires `statestore.mode=external`.
The KEDA PostgreSQL scaler reads the backlog directly from the database and cannot reach the embedded SQLite file inside the pod.
{{% /notice %}}

## Enable the statestore

The statestore is **off by default**.
Enable it and pick a mode with Helm values.

Embedded (SQLite on a PVC — development):

```bash
helm upgrade --install fission fission-charts/fission-all \
  --namespace fission \
  --set statestore.enabled=true \
  --set statestore.mode=embedded \
  --set statestore.embedded.size=1Gi
```

External (Postgres — production): create a Secret holding the DSN, then point the chart at it:

```bash
kubectl create secret generic statestore-postgres \
  --namespace fission \
  --from-literal=dsn='postgres://user:password@postgres.db.svc:5432/fission?sslmode=require'

helm upgrade --install fission fission-charts/fission-all \
  --namespace fission \
  --set statestore.enabled=true \
  --set statestore.mode=external
```

| Helm value | Default | Meaning |
| --- | --- | --- |
| `statestore.enabled` | `false` | Provision the statestore. Required by workflows, async invocation, and eventing. |
| `statestore.mode` | `embedded` | `embedded` (SQLite on a PVC) or `external` (a Postgres DSN Secret). |
| `statestore.embedded.size` | `1Gi` | Size of the PVC backing the embedded SQLite file. |
| `statestore.external` | — | Name of the DSN Secret for external mode (defaults to `statestore-postgres`, key `dsn`). |

Fission runs no database of its own in either mode: embedded is a file on a volume, and external is a database you already operate.

## Related

- [Durable Workflows]({{% ref "/docs/usage/workflows/_index.md" %}}) — multi-step orchestration recorded in the event log.
- [Asynchronous Invocation]({{% ref "/docs/usage/function/async-invocation.md" %}}) — fire-and-forget calls delivered from the queue.
- [Architecture overview]({{% ref "/docs/architecture/_index.md" %}}) — how the statestore sits alongside the other components.
