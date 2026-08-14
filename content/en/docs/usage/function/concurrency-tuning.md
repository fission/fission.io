---
title: "Tuning Function Concurrency"
draft: false
weight: 46
description: >
  Size a poolmgr function's warm pool for long-running, concurrency-heavy request workloads — LLM backends, chat agents, and other slow-turn services.
---

**Four knobs shape how a poolmgr function handles concurrent load: requests per pod, concurrency, provisioned concurrency, and idle timeout.
This page shows how they compose for workloads where each request is slow and heavy — an LLM chat backend, an agent runtime, a report generator — rather than the fast, light requests classic serverless assumes.**

For what each executor type is and how to pick one,
read [Controlling Function Execution]({{% ref "executor.en.md" %}}).
This page assumes `poolmgr` (the default executor).

## The mental model: a pod is a request slot

With the default `--requestsperpod 1`,
one specialized pod serves one request at a time.
That makes capacity planning simple:

> **Warm capacity = number of specialized pods.
> Peak capacity = `--concurrency`.**

For CPU- or IO-heavy request turns
(an LLM call that runs for seconds, a data transform, a build step)
this default is the right one:
packing a second slow request onto a busy pod doubles its latency,
so you scale by adding pods, not by sharing them.

Raise `--requestsperpod` only when requests are cheap and mostly waiting —
for example a thin proxy that spends its time blocked on a downstream service.

## The four knobs

| Knob | Flag | Default | What it shapes |
|------|------|---------|----------------|
| Requests per pod | `--requestsperpod` (`--rpp`) | `1` | How many concurrent requests one pod serves — the "slot width" |
| Concurrency | `--concurrency` (`--con`) | `500` | Maximum specialized pods — the burst ceiling |
| Provisioned concurrency | `--provisioned-concurrency` | `0` | Warm specialized pods kept ready — the latency floor |
| Idle timeout | `--idletimeout` | `120` | Seconds a pod stays specialized after its last request — the pool decay rate |

They compose like this:

* **`--concurrency` is the ceiling.**
  It caps how many pods the function may specialize at once.
  When every pod is busy and the ceiling is reached,
  further requests wait briefly and then fail with `429 Too Many Requests`.
  Set it to the most parallel turns you are willing to pay for.
* **`--provisioned-concurrency` is the floor.**
  Fission keeps this many pods specialized and ready even when the function is idle,
  so the first N concurrent requests never pay a cold start.
  Set it to your steady-state parallelism.
* **`--idletimeout` shapes everything between floor and ceiling.**
  After a burst, pods above the provisioned floor stay warm this many seconds and then get recycled.
  A longer timeout keeps burst capacity warm between bursty sessions;
  a shorter one returns resources to the cluster faster.

## Worked example: a chat backend

Suppose a chat function where each turn calls an LLM and runs for 2–10 seconds,
you expect around 20 concurrent turns in steady state,
and you want headroom for spikes of 100:

```bash
fission fn create --name chat-turn --env python --code chat.py \
  --requestsperpod 1 \
  --concurrency 100 \
  --provisioned-concurrency 20 \
  --idletimeout 600
```

Reading it back:

* Each turn gets its own pod (`--rpp 1`), so one slow LLM call never queues behind another.
* Up to 100 turns can run in parallel; the 101st gets a `429` and the client retries.
* 20 pods are always warm, so steady-state turns skip the cold start entirely.
* After a spike, the extra pods linger for 10 minutes —
  long enough that an active conversation returning after a pause still finds a warm pod.

Watch the spike behavior before raising `--provisioned-concurrency`:
warm pods hold their environment's resource requests permanently,
so the floor is a standing cost.

## Session affinity is an optimization, not a guarantee

If your function keeps a per-session cache
(a loaded model context, a memoized lookup),
sticky routing can keep a session's requests landing on the same warm pod:

```bash
fission fn create --name chat-turn --env python --code chat.py \
  --state --state-sticky-source header --state-sticky-name X-Session-Id ...
```

(The sticky flags are part of the function's state configuration,
so they take effect only together with `--state`.)

Stickiness is **best-effort by contract**:
any pod being added or removed can move a session to a different pod,
and a saturated sticky target overflows to another pod rather than queueing.
Treat the pod-local cache as exactly that — a cache.
Durable session state belongs outside the pod
(in Fission's keyed state API or your own store),
so a moved session rehydrates and continues correctly.

## When requests must not share a pod at all

For jobs where each request should get a completely fresh pod
(untrusted input, leaky native libraries),
add `--onceonly` (alias `--yolo`):
the pod serves exactly one request and is recycled.
Pair it with a `--concurrency` sized to your parallelism,
and expect every request to pay the specialization cost.

## Related

* [Controlling Function Execution]({{% ref "executor.en.md" %}}) — executor types and the per-knob reference.
* [Streaming Responses]({{% ref "streaming.md" %}}) — stream slow responses instead of raising timeouts.
* [Functions]({{% ref "/docs/concepts/functions.md" %}}) — the `Function` resource.
