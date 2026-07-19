---
title: "Workflows"
weight: 22
description: >
  Orchestrate several functions as one durable, resumable state machine — with parallel branches, data-driven routing, retries, durable waits, and typed-error handling.
---

**A workflow orchestrates several functions as one durable state machine: it survives controller restarts, resumes exactly where it stopped, retries transient failures, and routes typed business errors — all recorded step by step in the statestore.**

Starting with Fission {{< release-version >}}, you define a `Workflow` as a state machine over your functions and start a `WorkflowRun` each time you want it to execute.
For the mental model behind the two resources and the durability guarantees, read the [Workflows concept]({{% ref "/docs/concepts/workflows.md" %}}); this guide is how to enable, author, run, and inspect them.

## Prerequisites

Workflows are **off by default** and require the [statestore]({{% ref "/docs/architecture/statestore.md" %}}), which holds each run's event log:

```bash
helm upgrade --install fission fission-charts/fission-all \
  --namespace fission \
  --set statestore.enabled=true \
  --set workflows.enabled=true
```

Embedded statestore mode is enough to run workflows.

## State types

A workflow is a map of named states; each has a `type`:

| State | Purpose |
| --- | --- |
| `Task` | Invoke a function, with per-step timeout, retry, and error catching. |
| `Choice` | Route to the next state based on the run's data — no function call. |
| `Parallel` | Run several branches concurrently and join their results in order. |
| `Map` | Run one branch per element of an array, bounded by `maxConcurrency`. |
| `Wait` | Pause the run durably for a `duration`. |
| `Succeed` / `Fail` | Terminate the run. |

A run walks from `startAt` along each state's `next` until a state with `end: true` or a `Succeed`/`Fail` state.
The order-pipeline example below has this shape:

```mermaid
stateDiagram-v2
  [*] --> validate
  validate --> screening
  validate --> reject: InvalidOrder
  screening --> decision
  decision --> reject: high risk / out of stock
  decision --> charge
  charge --> fulfil
  charge --> reject: PaymentDeclined
  fulfil --> [*]
  reject --> [*]
```

`fission workflow graph --name <workflow>` renders exactly this diagram from a workflow's definition, and `--open` serves it in a local day/night viewer.

## In this section

- [Authoring workflows]({{% ref "authoring.md" %}}) — the full YAML reference for every state type, path shaping, retries, and the error model.
- [Run and inspect]({{% ref "run-and-inspect.md" %}}) — create, run, and manage workflows, and see where a run stopped with the `runs` commands and the graph viewer.
- [Examples]({{% ref "examples.md" %}}) — three worked workflows covering the full palette.

## Related

- [Workflows concept]({{% ref "/docs/concepts/workflows.md" %}}) — Workflow vs WorkflowRun and the durability model.
- [Statestore]({{% ref "/docs/architecture/statestore.md" %}}) — the durable event log workflows are recorded in.
- [Asynchronous invocation]({{% ref "/docs/usage/function/async-invocation.md" %}}) — the simpler durable primitive for single-function work.
