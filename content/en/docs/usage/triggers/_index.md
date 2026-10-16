---
title: "Triggers"
weight: 20
description: >
  Bind events to function invocations
---

A **trigger binds an event source to a function**, so that the function runs whenever the event occurs.
Fission ultimately invokes every function over HTTP.
The router exposes functions internally.
Each trigger type turns its event into an HTTP request to that function.

Fission ships several trigger types, one per kind of event source.
Pick the trigger that matches where your events come from.

## Trigger types

| Trigger | Event source | Created with | Page |
| --- | --- | --- | --- |
| HTTP trigger | An incoming HTTP request to a URL path | `fission httptrigger create` (alias `route`) | {{% ref "http-trigger.md" %}} |
| Time trigger | A cron schedule | `fission timetrigger create` (alias `timer`) | {{% ref "timer.md" %}} |
| Message queue trigger | A message published to a queue or stream | `fission mqtrigger create` (alias `mqt`) | {{% ref "message-queue-trigger-kind-keda/_index.md" %}} |
| Statestore eventing | An event published to a built-in statestore topic | `fission mqtrigger create --mqtkind fission --mqtype statestore` | {{% ref "statestore-eventing.md" %}} |
| Kubernetes watch trigger | A change to a Kubernetes object | `fission watch create` | {{% ref "kubewatcher.md" %}} |

{{% notice info %}}
For message queues, the **KEDA-based** message queue trigger is the recommended path.
It autoscales the connector that consumes from your event source, scaling to zero when idle.
See [Message Queue Trigger: KEDA]({{% ref "message-queue-trigger-kind-keda/_index.md" %}}).
{{% /notice %}}

## How triggers reach a function

All trigger types converge on the same internal path: each one issues an HTTP request to the router, which routes it to a function pod.
The router serves HTTP triggers directly.
The other trigger types run a dedicated component; it watches the event source and calls the router on your behalf.

```mermaid
flowchart LR
  client["HTTP Client"]:::user
  timer["Timer"]:::fission
  mqt["MQ Trigger"]:::fission
  watch["KubeWatcher"]:::fission

  subgraph k8s["Kubernetes Cluster"]
    router["Router"]:::fission
    fnPod["Function Pod"]:::pod
  end

  client -->|"HTTP request"| router
  timer -->|"on schedule"| router
  mqt -->|"on message"| router
  watch -->|"on object change"| router
  router -->|"forwards request"| fnPod
  fnPod -->|"response"| router
  classDef user fill:#ffffff,stroke:#94a3b8,color:#1f2a43
  classDef fission fill:#e8f0fe,stroke:#2d70de,color:#1f2a43
  classDef pod fill:#e6f7f1,stroke:#11a37f,color:#1f2a43,stroke-dasharray:5 3
```

The router resolves the request to a function and forwards it to a running pod (starting one if needed), then returns the function's response.
This is why understanding HTTP triggers and the router helps when debugging any trigger type.

## Related

- [HTTP Trigger]({{% ref "http-trigger.md" %}})
- [Time Trigger]({{% ref "timer.md" %}})
- [Message Queue Trigger: KEDA]({{% ref "message-queue-trigger-kind-keda/_index.md" %}})
- [Statestore Eventing]({{% ref "statestore-eventing.md" %}})
- [Kubernetes Watch Trigger]({{% ref "kubewatcher.md" %}})
- [Router architecture]({{% ref "/docs/architecture/router.md" %}})
