---
title: "Workflow Examples"
weight: 30
description: >
  Three worked workflows — an order pipeline, a Map fan-out, and a durable Wait timer — that together exercise every state type.
---

**Three runnable workflows in the [examples repository](https://github.com/fission/examples/tree/main/miscellaneous/workflows) cover the full state-type palette.**

Each directory has the `workflow.yaml`, the functions it calls, and sample inputs, plus a README with the deploy steps.
Read them alongside the [authoring reference]({{% ref "authoring.md" %}}).

## Order pipeline — Parallel, Choice, retry, catch

An e-commerce checkout: validate an order, then screen it for fraud and stock **in parallel**.
A `Choice` routes on the results.
Charging the card includes **retry and a catch for declines**.
Every failure converges onto one rejection path.
It is the flagship example — the one the [`stateDiagram`]({{% ref "_index.md" %}}#state-types) on the overview page is drawn from.

- **Shows:** `Parallel` with an ordered join, data-driven `Choice`, `Task` `retry` for transient gateway errors, and `catch` on a typed `PaymentDeclined` error.
- **Inputs:** `happy`, `invalid`, `high-fraud`, `out-of-stock`, `declined-card`, `flaky-gateway` — one per route through the machine.
- [order-pipeline →](https://github.com/fission/examples/tree/main/miscellaneous/workflows/order-pipeline)

## Batch enrichment — Map fan-out

Enrich a batch of CRM leads: a `Map` state invokes a single-record scoring function once per element of `$.leads`, at most three concurrently.
The ordered join array feeds a summary step.
The function stays simple.
The workflow owns the fan-out, throttling, retries, and ordering.

- **Shows:** `Map` with `itemsPath` and `maxConcurrency`, and an ordered join feeding the next `Task`.
- **Inputs:** `leads` — the array the Map iterates.
- [batch-enrichment →](https://github.com/fission/examples/tree/main/miscellaneous/workflows/batch-enrichment)

## Payment dunning — durable Wait timers

Subscription renewal with a grace period: if a charge is declined, the run **waits out a grace period on a durable timer**.
It tries once more before canceling.
The run consumes no pod, memory, or connection while waiting — the timer lives in the statestore and survives controller restarts.

- **Shows:** `Wait` as a durable delay, and a `catch` route that changes behavior on the second attempt.
- **Inputs:** `valid`, `past-due` — one that charges cleanly, one that exercises the grace-period retry.
- [payment-dunning →](https://github.com/fission/examples/tree/main/miscellaneous/workflows/payment-dunning)

## Related

- [Authoring workflows]({{% ref "authoring.md" %}}) — the fields these examples use.
- [Run and inspect]({{% ref "run-and-inspect.md" %}}) — run them and trace where each input lands.
