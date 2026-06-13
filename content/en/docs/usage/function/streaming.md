---
title: "Streaming Responses"
draft: false
weight: 48
description: >
  Stream a function's response incrementally with Server-Sent Events, HTTP chunked transfer, or a WebSocket upgrade using spec.streaming and the --streaming flags — for LLM tokens, AI agents, chat, and long-running responses.
---

By default a function buffers its full response and the router cuts the request off at `functionTimeout`.
Starting with Fission {{< release-version >}} a function can instead **stream its response incrementally** — over Server-Sent Events (SSE), HTTP chunked transfer, or a WebSocket upgrade.
The response is flushed to the client as it is produced and is **not** bound by `functionTimeout`.

Streaming is **per-function and opt-in**: omit the `spec.streaming` object (or the `--streaming` flag) and the function keeps the existing buffered behavior exactly.
Typical use cases are LLM token streaming, AI agent runs, chat, SSE feeds, and other long-running or bidirectional responses.

## Enable streaming

Create the function with `--streaming`, add a route, and invoke it:

```bash
fission fn create --name chat --env nodejs --code chat.js --streaming
fission route create --name chat --function chat --url /chat --method POST
```

Toggle streaming back off on an existing function:

```bash
fission fn update --name chat --streaming=false
```

### CLI flags

| Flag | Default | Meaning |
| --- | --- | --- |
| `--streaming` | off | Enable streaming responses for the function. Disable on update with `--streaming=false`. |
| `--streamingprotocol` | `auto` | Streaming protocol: `auto`, `sse`, `chunked`, or `websocket`. `auto` covers all cases; `websocket` signals intent (the upgrade is detected from the request). |
| `--streamingidletimeout` | `60` | Abort the stream if no bytes flow from the function for this many seconds; reset on each chunk. Also bounds time-to-first-byte. |
| `--streamingmaxduration` | `0` | Hard ceiling (seconds) on total stream lifetime; `0` means no ceiling. |

## How streaming changes timeouts

{{% notice info %}}
A streaming function does **not** inherit `functionTimeout` as a wall-clock cap — that limit is exactly what streaming exists to escape.
Progress is governed by the **idle timeout** (default 60s, reset on every chunk), and `--streamingmaxduration` is the optional absolute ceiling.
A function that keeps producing output completes even if it runs far past `functionTimeout`.
See the [function timeout concept]({{% ref "/docs/concepts/functions.md" %}}) for how this relates to the buffered path.
{{% /notice %}}

## Protocols

`auto` (the default) handles every case; set a specific protocol only to signal intent.
Streaming works on both the public HTTPTrigger route and the internal `/fission-function/<ns>/<name>` invocation path.

{{< tabs >}}
{{< tab "SSE" >}}
With SSE the function writes `text/event-stream` chunks and the router flushes each one as it arrives.
Use `curl -N` to watch tokens arrive incrementally instead of all at once:

```bash
curl -N https://<router>/chat -d '{"prompt":"hello"}'
```
{{< /tab >}}
{{< tab "Chunked" >}}
With HTTP chunked transfer the function writes its body in pieces and the router forwards each chunk without buffering the whole response.
This is the default transport for a non-SSE, non-WebSocket streaming response and needs no client opt-in beyond reading the body as it streams.
{{< /tab >}}
{{< tab "WebSocket" >}}
Create the function with the `websocket` protocol and connect with any WebSocket client:

```bash
fission fn create --name ws --env nodejs --code ws.js --streaming --streamingprotocol websocket
fission route create --name ws --function ws --url /ws --method GET
wscat -c ws://<router>/ws
```
{{< /tab >}}
{{< /tabs >}}

## WebSocket

WebSocket is now first-class for **every** environment, not just the Python GEVENT environment.
The router upgrades the connection and holds the function pod for the socket's whole lifetime (a router-driven keepalive), and the `main(ws, clients)` programming model is unchanged.

{{% notice warning %}}
The legacy Python `socket_tracker.py` keepalive mechanism still works but is **deprecated in favor of the streaming approach** and is targeted for removal in a future release.
New environment images should drop calls to the fetcher `/wsevent` endpoints and rely on the streaming WebSocket path.
{{% /notice %}}

For a worked WebSocket example, see the [WebSocket sample blog post](/blog/fission-websocket-sample/).

## Declarative spec

You can enable streaming directly on the `Function` resource:

```yaml
apiVersion: fission.io/v1
kind: Function
metadata:
  name: chat
spec:
  environment:
    name: nodejs
  streaming:
    protocol: sse
    idleTimeoutSeconds: 60
    maxDurationSeconds: 0     # optional absolute ceiling; 0 = unlimited
```

## Cluster default

The optional router environment variable `ROUTER_STREAM_IDLE_TIMEOUT` sets the cluster-wide default idle window, which per-function `idleTimeoutSeconds` overrides.
It is a router (Helm) setting; see [Customizing the chart](/docs/installation/upgrade/#configuration).

## Related

* [Create and run functions]({{% ref "functions.en.md" %}}) — the everyday function workflow.
* [Controlling Function Execution]({{% ref "executor.en.md" %}}) — executors, scaling, and concurrency.
* [HTTP Triggers]({{% ref "/docs/usage/triggers/http-trigger.md" %}}) — routing requests to a function.
* [Functions]({{% ref "/docs/concepts/functions.md" %}}) — the `Function` resource and the function timeout.
* [Custom Resource Definition Specification]({{% ref "/docs/reference/crd-reference.md" %}}) — the `streaming` spec fields.
