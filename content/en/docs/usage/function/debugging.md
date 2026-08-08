---
title: "Debugging and diagnosing functions"
draft: false
weight: 9
description: >
  Diagnose a failing Fission function with fission function describe, failure attribution from fission function test, and per-invocation request-id tracing.
---

**Diagnose a failing function down to the component and the exact invocation, without reading server logs.**
When a function misbehaves, the question is usually *where* it broke — the function code, the build, the executor, or a timeout — and *which* call it was.
Fission answers both: `fission function describe` shows a function's health in one view, `fission function test` attributes a failure to a component and hands you a request id, and `fission function logs --request-id` pulls that one invocation's logs.

#### See a function's health at a glance

`fission function describe` consolidates what you would otherwise gather from `function getmeta`, `function pods`, and `package info` into a single view:

```bash
$ fission function describe --name hello
Name:         hello
Namespace:    default
Environment:  nodejs
Executor:     poolmgr
Package:      hello-pkg
Invocable:    Yes (1 of 2 warm pod(s) serving)
Created:      5m

CONDITIONS:
  TYPE   STATUS  REASON       MESSAGE
  Ready  True    PodsReady    ...

PACKAGE:
  Name:          hello-pkg
  Build Status:  succeeded

PODS:
  NAME              READY  STATUS   AGE
  poolmgr-...-abcd  2/2    Running  5m

VERSIONING:
  Versioning: disabled
```

For a function with [versioning]({{% ref "versions-aliases.md" %}}) enabled, the `VERSIONING` section lists the mode, the version count, and the aliases.

The **`Invocable`** line answers "can I call this right now?":

| `Invocable` value | Meaning |
| --- | --- |
| `Yes (N of M warm pod(s) serving)` | Warm pods are published and serving traffic. |
| `Yes (N warm pod(s))` | Warm, ready pods exist. |
| `Yes (cold start on first call)` | Ready, but the first call pays a cold start. |
| `No - function not Ready (see CONDITIONS)` | Not invocable; the `CONDITIONS` table says why. |

Each section is sourced independently, so an unavailable source degrades to `<none>` rather than failing the whole view.
On a **failed build**, the `PACKAGE` section additionally prints the build log inline — the one place you most need it:

```bash
$ fission function describe --name broken
...
PACKAGE:
  Name:          broken-pkg
  Build Status:  failed
  Build Logs:
  npm ERR! ... cannot find module 'left-pad'
```

#### Read the failure attribution

`fission function test` invokes a function and, on failure, tells you which component failed and why instead of just printing a status code.
Every run echoes the invocation's request id; a failure renders the structured attribution:

```bash
$ fission function test --name broken
Request ID: 6f1c2a9e-1c2b-4f0a-9d2e-7b3c2a1d4e5f
✗ function "broken" failed in executor (specialization_failed) — status 500, request 6f1c2a9e-...
```

Now you know it failed during **specialization** in the **executor** (not in your code, not a timeout), and you have the request id to find its logs.
Against an older cluster that does not send structured errors, `test` falls back to printing the raw response body.

#### The failure-attribution contract

Every response — success or failure — carries the request id, and failures add the component, so callers and tooling can attribute a failure without reading server logs:

| Header | Meaning |
| --- | --- |
| `X-Fission-Request-ID` | Stable id for the invocation; honored if you send one, otherwise minted by the router. |
| `X-Fission-Component` | On a failure, the component that failed. |

Failures also return a structured JSON body:

```json
{
  "component": "executor",
  "reason": "specialization_failed",
  "requestId": "6f1c2a9e-1c2b-4f0a-9d2e-7b3c2a1d4e5f",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

The **component** is one of `router`, `executor`, `fetcher`, `function`, or `timeout`.
The **reason** is a stable value you can match on:

| Reason | Typically means |
| --- | --- |
| `function_error` | Your code returned an error or a 5xx. |
| `function_timeout` | The function exceeded its time budget. |
| `specialization_failed` | The code failed to load into the environment (bad entry point, import error). |
| `connection_refused` / `dial_error` | The function pod was not reachable. |
| `capacity_exceeded` / `executor_unavailable` | The executor could not provide a pod in time. |
| `client_disconnect` | The caller went away before the response finished. |
| `stream_idle` / `stream_max_duration` | A [streaming]({{% ref "streaming.md" %}}) response hit its idle or max-duration limit. |

The body never includes raw internal error text by default.
To get verbose detail for a single call, send `X-Fission-Debug: true`; the router fills in a `message` field only when it is running in debug mode.

{{% notice info %}}
**Operators:** structured error bodies are on by default and can be turned off with `ROUTER_STRUCTURED_ERRORS=false` on the router, which restores the legacy plain-text error body.
Status codes are unchanged either way.
{{% /notice %}}

#### Trace one invocation through the logs

With the request id from `test` (or from a caller's `X-Fission-Request-ID` response header), pull just that invocation's logs — when logs are aggregated with Loki:

```bash
$ fission function logs --name hello --dbtype loki --request-id 6f1c2a9e-1c2b-4f0a-9d2e-7b3c2a1d4e5f
```

`--request-id`, `--trace-id`, and `--level` are applied by the `loki` log database and are ignored by the default `kubernetes` driver.
See [Logs with Loki]({{% ref "/docs/usage/observability/loki.md" %}}) for setup and the full query workflow, and [Local development with run-local]({{% ref "run-local.md" %}}) to reproduce and fix the failure locally without a redeploy.
