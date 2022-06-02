---
title: "Metrics with Prometheus"
weight: 10
---

## Metrics in Fission

Fission exposes metrics in the Prometheus standard, which can be readily scraped and used using a Prometheus server and visualized using Grafana.
The metrics help monitor the state of the Functions as well as the Fission components.

### Prometheus

Prometheus is a monitoring and alerting tool.
It uses a multi-dimensional data model with time series data identified by metric name and key/value pairs.

Fission exposes metrics which are pulled and operated by Prometheus at regular intervals.

### Grafana

Grafana is a visualization tool which can query, visualize, alert on and understand metrics.
It supports Prometheus as it's data source.

## Setting up

There are different ways to install Prometheus.
It can be installed and run in and outside containers.
Since Fission itself runs in Kubernetes, we'll use the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator) which is a way of installing Prometheus as Kubernetes Custom Resource.

### Prerequisite

- Kubernetes cluster
- Fission [installed in the cluster](/docs/installation/)
- [Helm](https://helm.sh/) (This post assumes helm 3 in use)
- kubectl and kubeconfig configured

### Install Prometheus and Grafana

We'll install Prometheus and Grafana in a namespace named `monitoring`.

To create the namespace, run the following command in a terminal:

```bash
expose METRICS_NAMESPACE=monitoring
kubectl create namespace $METRICS_NAMESPACE
```

Install Prometheus and Grafana with the release name `fission-metrics`.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false,prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

This will install Prometheus and Grafana in the `monitoring` namespace.
Along with the Prometheus server, it'll also install other components viz. `node-exporter`, `kube-state-metrics` and `alertmanager`.

### Enabling Service Monitors in Fission

You'll need to enable service monitors which will scrape metrics from fission components.

```bash
helm upgrade fission fission-charts/fission-all --namespace fission --set serviceMonitor.enabled=true --set serviceMonitor.namespace=monitoring
```

### Accessing Grafana UI

The installation creates a Service named `prometheus-grafana`. To access this, you can use Kubernetes port forwarding

```bash
kubectl --namespace monitoring port-forward svc/prometheus-grafana 3000:80
```

The Grafana can be now accessed on <http://localhost:3000>.

To log in to the Grafana dashboard, enter `admin` in the `username` field.

For password, you'll need to run the following command:

```bash
kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
  
This installation also adds Prometheus as a data source for Grafana automatically.
You can verify and update this in the `Data Sources` section of the UI.

## Metrics Queries

Once Prometheus is configured, we can now run queries in Grafana over Fission metrics.
Individual queries can be run under `Explore` section.

Fission exposes a set of metrics. For example to query the total number of function calls, run

```text
fission_function_calls_total
```

Calls for a specific function can be queried using

```text
fission_function_calls_total{name="foo"}
```

To track the duration of a specific function

```text
fission_function_duration_seconds{name="hello"}
```

There are a few more Fission metrics available which are listed [here](/docs/reference/metrics-reference)

## Fission Dashboard

With Grafana, visuals dashboards can be created to monitor multiple metrics in an organized way.

You can refer to [Fission functions dashboard](https://github.com/fission/examples/blob/main/miscellaneous/dashboards/prometheus-fission-functions.json) that shows log metrics from all the major components of Fission.

Once imported, the dashboard will look similar to below image.

![Prometheus Fission Functions dashboard](../assets/prometheus-grafana.png)

View the list of all [Fission dashboards](https://github.com/fission/examples/tree/main/miscellaneous/dashboards) posted over time.
