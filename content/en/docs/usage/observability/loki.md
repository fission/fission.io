---
title: "Logs with Loki"
weight: 20
description: >
  Aggregate Fission component and function pod logs with the Grafana Loki, Promtail, and Grafana stack installed via Helm.
---

## Logs in Fission

**Both Fission's core services and your function pods emit logs**, and aggregating them makes debugging far easier.

Fission runs several core components that route, build, and execute your functions.
The logs from the components and from the function pods together tell the full story of a request, so a good log-aggregation backend is worth setting up.

## Grafana Loki

Loki is a horizontally-scalable, highly-available, multi-tenant log aggregation system inspired by Prometheus.
The main components are a client to fetch the logs, an aggregator, and a visualizing tool (Grafana).

The stack supports multiple clients; this guide uses Promtail, the recommended client for Kubernetes because it automatically picks up pod labels as metadata.

| Component | Role |
|-----------|------|
| **Loki** | Aggregates and stores the logs. |
| **Promtail** | Fetches logs from each pod and forwards them to Loki. |
| **Grafana** | Visualizes Loki data through dashboards and queries. |

The diagram below shows how the three connect: Promtail ships pod logs to Loki, and Grafana queries Loki to visualize them.

![Loki-Grafana stack](../assets/stack.png)

## Setting up

There are different ways and configurations to [install the complete stack](https://grafana.com/docs/loki/latest/installation/).
For this case, we'll use Helm.

### Prerequisite

- Kubernetes cluster
- Fission [installed in the cluster](/docs/installation/)
- [Helm](https://helm.sh/) (This post assumes helm 3 in use)
- kubectl and kubeconfig configured


#### Install Grafana and Loki

Create a values.yaml file.
We are installing [monolithic Loki](https://grafana.com/docs/loki/latest/setup/install/helm/install-monolithic/).
Check Loki's [deployment modes](https://grafana.com/docs/loki/latest/get-started/deployment-modes/) for other options.

```bash
cat > loki-config.yaml <<EOF
deploymentMode: SingleBinary
loki:
  auth_enabled: false
  commonConfig:
    replication_factor: 1
  storage:
    type: 'filesystem'
  schemaConfig:
    configs:
    - from: "2024-01-01"
      store: tsdb
      index:
        prefix: loki_index_
        period: 24h
      object_store: filesystem # we're storing on filesystem, so there's no real persistence here.
      schema: v13
singleBinary:
  replicas: 1
read:
  replicas: 0
backend:
  replicas: 0
write:
  replicas: 0
EOF
```

From a terminal, run the following commands to add the Loki repo and then install Loki.

```bash
$ helm repo add grafana https://grafana.github.io/helm-charts
$ helm repo update
$ helm upgrade -n monitoring --create-namespace --install loki grafana/loki -f loki-config.yaml
```

This will install Loki in the monitoring namespace.
Check if there are pods running for Loki.


#### Install Promtail

You'll notice that the Promtail installation is disabled above.
This is because custom configuration is required to effectively tail logs.
The default Promtail configuration follows the [kubernetes recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) and filters out everything that doesn't conform to those rules.

Create a values.yaml file that lets Promtail tail and forward all labels — this is necessary because Fission adds extra labels when a pod is specialized.
```bash
cat > promtail-config.yaml <<EOF
config:
  clients:
    - url: http://loki-gateway.monitoring.svc.cluster.local/loki/api/v1/push
  extraRelabelConfigs: 
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
  snippets:
    common:
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_node_name
        target_label: node_name
      - action: replace
        source_labels:
          - __meta_kubernetes_namespace
        target_label: namespace
      - action: replace
        replacement: \$1
        separator: /
        source_labels:
          - namespace
          - app
        target_label: job
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_name
        target_label: pod
      - action: replace
        source_labels:
          - __meta_kubernetes_pod_container_name
        target_label: container
      - action: replace
        replacement: /var/log/pods/*\$1/*.log
        separator: /
        source_labels:
          - __meta_kubernetes_pod_uid
          - __meta_kubernetes_pod_container_name
        target_label: __path__
      - action: replace
        replacement: /var/log/pods/*\$1/*.log
        regex: true/(.*)
        separator: /
        source_labels:
          - __meta_kubernetes_pod_annotationpresent_kubernetes_io_config_hash
          - __meta_kubernetes_pod_annotation_kubernetes_io_config_hash
          - __meta_kubernetes_pod_container_name
        target_label: __path__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
EOF
```

Install Promtail with this configuration:

```bash
$ helm upgrade -n monitoring --install promtail grafana/promtail -f promtail-config.yaml
```

This will install Promtail in the `monitoring` namespace.
Check that a Promtail pod is running.

The Promtail UI at `localhost:3101` shows all of the pods' logs being tailed, along with the labels assigned to them.
```bash
$ kubectl --namespace monitoring port-forward $(kubectl  --namespace monitoring get daemonset -l app.kubernetes.io/instance=promtail -o name) 3101:3101
```

## Install Grafana

Similarly, to install Grafana, run the following commands from a terminal.

```
helm repo add grafana https://grafana.github.io/helm-charts/
helm repo update
helm upgrade --install grafana grafana/grafana --create-namespace -n grafana
```

This will install Grafana in the `grafana` namespace.


## Accessing Grafana UI

The installation above creates a Service in the `grafana` namespace.
To access this, you can:
- Create an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) for this service
- Use Kubernetes port forwarding
    ```
    kubectl port-forward svc/grafana -n grafana 3000:80
    ```
## Fetching Credentials of Grafana

The default user is `admin`.
Fetch the password with:
```
kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

#### Adding Loki as a data source in Grafana

Clicking on the Settings icon in the left pane will bring up a menu, click on `Data Sources`.
Clicking on `Add Data Source` and select Loki.
Under HTTP, in the URL field put `http://loki-gateway.monitoring.svc.cluster.local`

Click on `Save and Test` and there should be a notification of the data source added successfully.

### Running Log Queries

From the options in the left pane, navigate to `Explore`.
Here you can run log queries using [LogQL](https://grafana.com/docs/loki/latest/logql/).
Since Loki auto-scrapes labels, example log queries are presented, along with a list of log labels you can select from.

You can run queries for Fission components such as:

- All logs from Fission Router
    `{svc="router"}`
- All logs from Fission Router that have "error" in the statement.
    `{svc="router"} |= "error"`

Loki is great for performing metrics over the logs, for example:

- Count of all logs in Fission Router with "error" over span of 5 mins `count_over_time({svc="router"} |= "error" [5m])`.

### Querying logs from the Fission CLI

You do not have to open Grafana to read function logs.
With Loki configured, `fission function logs --dbtype loki` queries it directly, and a few filters make it easy to follow a single function or a single invocation:

```bash
# Stream a function's logs as they arrive
$ fission function logs --name hello --dbtype loki --follow

# Just the logs for one invocation, by its X-Fission-Request-ID
$ fission function logs --name hello --dbtype loki --request-id 6f1c2a9e-1c2b-4f0a-9d2e-7b3c2a1d4e5f

# Filter by trace id or level
$ fission function logs --name hello --dbtype loki --trace-id 4bf92f3577b34da6a3ce929d0e0e4736
$ fission function logs --name hello --dbtype loki --level error
```

`--request-id`, `--trace-id`, and `--level` are applied by the `loki` driver only; the default `kubernetes` driver ignores them.
The request id comes from the `X-Fission-Request-ID` response header or from `fission function test` — see [Debugging and diagnosing functions]({{% ref "/docs/usage/function/debugging.md" %}}) for how to get it and attribute a failure to a component.

## Fission Logs Dashboard

Grafana dashboards aggregate queries into panels, each visualizing a metric over your logs in real time.
Dashboards are easily shareable.

Multiple panels with queries over Fission can be combined for an overall view of Fission's components and the functions running within them.
An exported JSON of one such dashboard can be found [here](https://github.com/fission/examples/blob/main/miscellaneous/dashboards/loki-grafana-summary.json).
This dashboard shows log metrics from all the major components of Fission.

Once imported, the dashboard looks like this:

![Loki-Grafana dashboard](../assets/loki-grafana-dashboard.png)

Watch the same [location](https://github.com/fission/examples/tree/main/miscellaneous/dashboards) for more dashboards, which will be added over time.
