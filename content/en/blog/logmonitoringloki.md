---
title: "Monitoring Fission logs with Grafana Loki"
date: 2020-09-14T16:19:12+05:30
author: "Sahil Lakhwani"
categories: ["Tutorials"]
description: "Enabling event driven autoscaling with KEDA integration"
type: "blog"
---

# Importance of Logs

Proper logging in a software is a quick and systematic way to inform the state of the software. Although the definition of 'logs' remains the same along years in software engineering, the scope of what logs are used is has always been increasing. Apart from helping developers and operators, logs can be used by complimenting software for security, metrics, triggers, cost estimation and other different operations.

# Logs in Fission

Fission works in a systematic way where there are different services (containers) providing functionalities for running applications (Functions) in a serverless way. Logs in Fission thus comprise of log statements from these services as well as from the applications.

A good log monitoring solution can be useful to make full use of these logs.

# Grafana Loki

Grafana Loki is a set of components which provides fully featured logging stack. This comprises of a client to fetch the logs, an aggregator and a visualizing tool. 

The stack supports multiple clients, for the case here we will use Promtail which is the recommended client when using the stack in Kubernetes.
The components are briefed below.

- **Loki** - Loki is a horizontally scalable, highly available, multi-tenant log aggregation system inspired by Prometheus.
- **Promtail** - Promtail is the client which fetches and forwards the logs to Loki. It is a good fit for Kubernetes as it automatically fetches metadata such as pod labels.
- **Grafana** - A visualizing tool which supports Loki as a data source.

The stack is depicted briefly in the below image

![loki_grafana_stack](/images/loki-grafana/stack.png)


# Setting up

There are different ways and configurations to [install the complete stack](https://grafana.com/docs/loki/latest/installation/). For this case, we'll use Helm.

## Prerequisite

- Kubernetes cluster
- Fission [installed in the cluster](/docs/installation/)
- [Helm](https://helm.sh/) (This post assumes helm 3 in use)
- kubectl and kubeconfig configured


## Install Loki and Promtail

From a terminal, run the following commands to add the Loki repo and then install Loki

```
helm repo add loki https://grafana.github.io/loki/charts
helm repo update
helm upgrade --install loki loki/loki-stack
```

This will install Loki in the default namespace. Check if there're pods running for Loki and Promtail. This also creates a Service. Note the ClusterIP of this service which will be needed further.


## Install Grafana

Similarly, to install Grafana, run the following commands from a terminal.

```
helm repo add stable https://kubernetes-charts.storage.googleapis.com
helm repo update
helm upgrade --install grafana stable/grafana -n grafana
```

This will install Grafana in the `grafana` namespace


## Accessing Grafana UI

The installation above creates a Service in `grafana` namespace. To access this, you can
- Create an [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) for this service
- Use Kubernetes port forwarding
    ```
    export POD_NAME=$(kubectl get pods --namespace grafana -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
    kubectl --namespace grafana port-forward $POD_NAME 3000
    ```
  
## Adding Loki as a data source in Grafana

Clicking on the Settings icon in the left pane will bring up a menu, click on `Data Sources`. Clicking on `Add Data Source` and select Loki.
Under HTTP, in the URL field, put the ClusterIP noted in the pereceding section followed by 3100 which is the default port of Loki. For example, if the ClusterIP is `http://10.108.230.242` the value to put is `http://10.108.230.242:3100`. Click on `Save and Test` and there should be a notification of the data source added successfully.

# Running Log Queries

From the options in left pane, navigate to `Explore`. Here you can run log queries using [LogQL](https://grafana.com/docs/loki/latest/logql/). Since Loki auto scrapes labels, there will be example log queries presented. There also will be list of log labels that you can select from.

You can run queries for Fission components such as:
- All logs from Fission Router
    `{svc="router"}`
- All logs from Fission Router that have "error" in the statement.
    `{svc="router"} |= "error"`

Loki is great for performing metrics over the logs, for example:
- Count of all logs in Fission Router with "error" over span of 5 mins 
    `count_over_time({svc="router"} |= "error" [5m])`


# Fission Logs Dashboard

Grafana provides a great way to build visual dashboards by aggregating queries.
These dashboards are a set of individual panels each showing visuals of some queries.
Metrics over this logs can be seen in real time. The dashboards are also easily shareable.

Multiple panel with queries over Fission can be put together to get overall view of Fission components as well the Functions running within.
An exported JSON of one such dashboard can be found [here](/misc/loki-grafana-dashboard.json). This dashboard shows log metrics from all the major components of Fission.

Once imported, the dashboard will look similar to below image.

![loki_grafana_dashboard](/images/loki-grafana/loki-grafana-dashboard.png)


**_Authors:_**

* [Sahil Lakhwani](https://twitter.com/lakhwani_sahil)  Software Engineer - [InfraCloud Technologies](http://infracloud.io/)
