---
title: "Observability"
weight: 40
description: >
  Collect metrics, traces, and logs from Fission and your functions
---

**Observability is how you understand what Fission and your functions are doing in production** — through metrics, traces, and logs.

Fission emits all three signals from its core components and from your function pods, in formats that standard cloud-native tooling already understands.
This section shows you how to wire each signal into a backend and visualize it in Grafana.

## The observability stack

Fission's components and your function pods are the sources.
Each source emits one or more signals, which a collector ingests and stores, and which Grafana then queries for dashboards and ad-hoc exploration.

```mermaid
flowchart LR
  subgraph sources["Fission Sources"]
    components["Core components (router, executor, ...)"]
    fnPods["Function pods"]
  end

  subgraph collect["Collectors / Stores"]
    prometheus["Prometheus"]
    otel["OTel Collector"]
    loki["Loki"]
  end

  jaeger["Jaeger"]
  grafana["Grafana"]

  components -->|"metrics"| prometheus
  fnPods -->|"metrics"| prometheus
  components -->|"traces"| otel
  fnPods -->|"traces"| otel
  components -->|"logs"| loki
  fnPods -->|"logs"| loki

  otel -->|"exports traces"| jaeger
  prometheus -->|"datasource"| grafana
  loki -->|"datasource"| grafana
  jaeger -->|"datasource"| grafana
```

## Signals and guides

- **Metrics** — Fission exposes Prometheus-format metrics from every component and function. See [Metrics with Prometheus]({{% ref "prometheus.md" %}}).
- **Traces** — Fission instruments request flows with OpenTelemetry and can export to any OTLP backend such as Jaeger. See [Tracing with OpenTelemetry]({{% ref "opentelemetry.md" %}}).
- **Logs** — function and component logs can be aggregated with Loki and queried in Grafana. See [Logs with Loki]({{% ref "loki.md" %}}).
- **Service mesh** — Linkerd can mesh function and Fission pods to add request-level metrics. See [Observability with Linkerd]({{% ref "linkerd.md" %}}).
