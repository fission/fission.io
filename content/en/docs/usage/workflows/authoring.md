---
title: "Authoring Workflows"
weight: 10
description: >
  The full YAML reference for a Workflow — every state type, JSONPath I/O shaping, retries and backoff, and the built-in error model.
---

**A `Workflow` is a YAML state machine: a `startAt` state and a map of named states, each of which invokes a function, branches on data, waits, or terminates.**

This page is the field reference.
For the concepts, see [Workflows]({{% ref "/docs/concepts/workflows.md" %}}); to run and inspect what you author, see [Run and inspect]({{% ref "run-and-inspect.md" %}}).

## Manifest skeleton

```yaml
apiVersion: fission.io/v1
kind: Workflow
metadata:
  name: order-pipeline
spec:
  startAt: validate          # the first state
  timeout: 1h                # hard ceiling on total run time (default 24h)
  defaultRetry:              # optional; applied to Task states with no retry of their own
    maxAttempts: 3
    backoffBase: 1s
    backoffCap: 10s
  historyRetention:          # bound how many finished runs are kept
    maxCount: 20
    maxAge: 24h
  states:
    validate:
      type: Task
      function: { name: wf-validate-order }
      next: screening
    # ... more states ...
```

Every state has a `type` and, unless it is terminal, either `next: <state>` or `end: true`.
The functions a workflow references are ordinary Fission functions in the same namespace.

## Task

Invoke a function.
This is the only state that runs your code.

```yaml
charge:
  type: Task
  function: { name: wf-charge-card }
  timeout: 30s                              # per-step timeout
  retry: { maxAttempts: 3, backoffBase: 1s, backoffCap: 10s }
  catch:
    - errorType: PaymentDeclined            # a typed business error
      next: reject
      resultPath: $.error
  resultPath: $.charge                      # where the function result lands in the document
  next: fulfil
```

| Field | Meaning |
| --- | --- |
| `function.name` | The function to invoke. |
| `timeout` | Per-step timeout (e.g. `30s`). |
| `retry` | Retry policy for this Task (overrides `spec.defaultRetry`). |
| `catch` | Ordered error routes (see [Error model](#error-model)). |
| `inputPath` / `resultPath` / `outputPath` | JSONPath I/O shaping (see [Shaping step I/O](#shaping-step-io)). |
| `next` / `end` | The next state, or terminate the run. |

### Retry policy

`retry` (and `spec.defaultRetry`) is a bounded exponential backoff:

| Field | Meaning |
| --- | --- |
| `maxAttempts` | Total attempts before the failure is final. |
| `backoffBase` | Delay before the first retry; doubles each attempt. |
| `backoffCap` | Upper bound on the per-attempt delay. |

Retries apply to **retryable** (transient, 5xx) failures.
A permanent (4xx typed) error is not retried — route it with `catch` instead.

## Shaping step I/O

A run carries a single JSON document.
Three optional JSONPath fields shape how a state reads from and writes to it:

- **`inputPath`** selects the sub-document the state receives (default: the whole document).
- **`resultPath`** selects where the state's output is merged back (default: replace the document).
- **`outputPath`** selects what is passed on to the next state.

`resultPath` is the one to be deliberate about.
Setting `resultPath: $.charge` merges the function's result under `$.charge`, **keeping** the rest of the document; omitting it **replaces** the whole document with the result.
The same applies to a caught error — merge it so the recovery step still sees the original input:

```yaml
catch:
  - errorType: InvalidOrder
    next: reject
    resultPath: $.error     # merge the error at $.error, keep the order document
```

## Choice

Route to the next state based on the document, with no function call.
Rules are evaluated in order; the first match wins, and `default` is taken if none match.

```yaml
decision:
  type: Choice
  choices:
    - variable: $.screening[0].riskScore
      numericGreaterThan: 70
      next: reject
    - variable: $.screening[1].status
      stringEquals: OUT_OF_STOCK
      next: reject
  default: charge
```

Each rule names a `variable` (a JSONPath into the document), a comparator (for example `numericGreaterThan`, `stringEquals`), and the `next` state.

## Parallel

Run several branches concurrently and join their results into an **ordered array** — element *i* of the join is branch *i*'s result.

```yaml
screening:
  type: Parallel
  branches:
    - startAt: fraud
      states:
        fraud: { type: Task, function: { name: wf-fraud-score }, end: true }
    - startAt: stock
      states:
        stock: { type: Task, function: { name: wf-inventory-check }, end: true }
  resultPath: $.screening      # the ordered [fraud, stock] array merges here
  next: decision
```

Each branch is its own small state machine with a `startAt` and `states`.
If a branch fails terminally the Parallel state fails fast with `Fission.BranchFailed`, which a `catch` on the state can route.

## Map

Run one branch per element of an array, bounded by `maxConcurrency`.
The join is again an ordered array aligned with the input.

```yaml
enrich:
  type: Map
  itemsPath: $.leads          # the array to iterate
  maxConcurrency: 3           # at most 3 branch executions in flight
  branches:
    - startAt: score
      states:
        score: { type: Task, function: { name: wf-enrich-lead }, end: true }
  next: summarize
```

A Map has exactly one branch — the template applied to every item.

## Wait

Pause the run durably for a `duration`.
The run consumes no resources while waiting, survives controller restarts, and fires exactly once.

```yaml
grace-period:
  type: Wait
  duration: 72h               # days are fine — it is a durable timer, not a sleep
  next: second-attempt
```

## Succeed and Fail

Terminal states.
`Succeed` ends the run successfully; `Fail` ends it as failed.
A Task with `end: true` also terminates the run.

```yaml
done:
  type: Succeed
```

## Error model

Fission classifies every step failure into a built-in error class that `catch.errorType` (and retries) key off:

| Error class | Meaning | Retried? |
| --- | --- | --- |
| `Fission.FunctionError` | The function returned a 5xx — a transient/infrastructure failure. | Yes (per the retry policy). |
| `Fission.PermanentError` | The function returned a 4xx — a permanent failure retrying cannot fix. | No. |
| `Fission.Timeout` | The step exceeded its `timeout`. | Per policy. |
| `Fission.BranchFailed` | A `Parallel`/`Map` branch failed terminally. | — (route with `catch`). |
| `Fission.All` | Matches any error class in a `catch` route. | — |

A function can also return its own **typed** business error by responding with a `{"errorType": "PaymentDeclined", ...}` body; `catch` routes on that name directly, so business recovery is separate from infrastructure retries.

## Validate before applying

`fission workflow validate` checks a manifest — unreachable states, dangling `next` targets, a missing `startAt` — without creating anything:

```bash
fission workflow validate -f workflow.yaml
```

## Related

- [Run and inspect]({{% ref "run-and-inspect.md" %}}) — create, run, and trace what you author here.
- [Examples]({{% ref "examples.md" %}}) — these fields assembled into three complete workflows.
- [Workflow CLI reference]({{% ref "/docs/reference/fission-cli/fission_workflow.md" %}}) — every command and flag.
