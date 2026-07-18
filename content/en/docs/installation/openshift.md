---
title: "OpenShift"
weight: 30
description: >
  OpenShift specific setup 
---

**This page covers OpenShift-specific setup: installing Fission, running the Logger as a privileged container, and enabling Prometheus metrics.**

## Installing Fission

See [Fission installation]({{%ref "_index.en.md" %}}) to learn how to install Fission.

## Run Logger as privileged container

Logger pods must run as a privileged container because Fission mounts a `hostPath` volume into FluentBit to read container log files and persist data.

The persistence is for FluentBit's [tail plugin](https://github.com/fluent/fluent-bit-docs/blob/master/pipeline/inputs/tail.md) to read/write its own sqlite database.
Fission itself doesn't persist anything.

```text
Optionally a database file can be used so the plugin can have a history of tracked files and a state of offsets, this is very useful to resume a state if the service is restarted.
```

Once the logger restarts, it ensures no duplicate logs are sent to the log database.

You may need to add `privileged` permission to the logger's service account `fission-fluentbit`.

```bash
oc adm policy add-scc-to-user privileged -z fission-fluentbit -n fission
```

* Reference: https://github.com/fluent/fluentd-kubernetes-daemonset#running-on-openshift

## Prometheus

* Follow [this guide](https://docs.openshift.com/container-platform/4.2/monitoring/cluster-monitoring/configuring-the-monitoring-stack.html#creating-cluster-monitoring-configmap_configuring-monitoring) to deploy Prometheus to OpenShift cluster.

* Get Prometheus server URL by following [Accessing Prometheus, Alertmanager, and Grafana](https://docs.openshift.com/container-platform/4.2/monitoring/cluster-monitoring/prometheus-alertmanager-and-grafana.html#monitoring-accessing-prometheus-alertmanager-grafana-directly_accessing-prometheus).

For example, if we have `https://prometheus-k8s-openshift-monitoring.apps._url_.openshift.com` as Prometheus server URL, encode following config with base64

```sh
$ base64 <<EOF
canary:
  enabled: true
  prometheusSvc: "https://prometheus-k8s-openshift-monitoring.apps._url_.openshift.com"
EOF
```

Patch configmap `feature-config` in `fission` namespace with output from previous step

```sh
$ kubectl -n fission patch configmap feature-config \
    -p '{"data":{"config.yaml":"Y2FuYXJ5OgogIGVuYWJsZWQ6IHRydWUKICBwcm9tZXRoZXVzU3ZjOiAiaHR0cHM6Ly9wcm9tZXRoZXVzLWs4cy1vcGVuc2hpZnQtbW9uaXRvcmluZy5hcHBzLl91cmxfLm9wZW5zaGlmdC5jb20iCg"}}'
```

Restart the canaryconfig pod so it reloads the updated config.

```sh
$ kubectl -n fission delete pod -l svc=canaryconfig
```
