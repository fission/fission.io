+++
title = "Autoscaling Serverless Functions with Custom Metrics"
date = "2022-05-11T14:43:46+05:30"
author = "Ankit Chawla"
description = "Let us see how to enable autoscaling for serverless functions with custom metrics"
categories = ["Tutorials"]
type = "blog"
+++


Autoscaling is one of the key features of Kubernetes because of its capability to scale up or down according to the load.
This is pretty useful as optimizes cost with minimum human intervention.
Autoscaling adjusts your applications and resources based on the rise and fall in the demand.

In the earlier versions of Fission, new deploy functions depended only on `targetCPU` metric for scaling.
But what if you want the functions to scale based on some third party software's metrics?

In our latest [Fission release 1.16.0-rc2](/docs/releases/v1.16.0-rc2/) , we have upgraded our autoscaling dependencies to [HPA v2beta2](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#horizontalpodautoscaler-v2beta2-autoscaling) from [HPA v1](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#horizontalpodautoscaler-v1-autoscaling) since HPA v1 doesn't support custom metrics.
This allows fission to scale function based on newdeploy or container executor via custom metrics.

In this blog post we will cover scraping and exposing kafka metrics and then providing the metrics to our function.

## Prerequisites

- A Kubernetes cluster with the latest version of helm.
- The latest version of Fission-CLI on the local machine

## Steps to set up autoscaling on custom metrics

- First we will set up a strimzi kafka exporter which is going to provide the metrics that we feed to the newdeploy HPA.
- Next we will use a pod monitor to scrape the metrics from the kafka pods.
- Finally we will set up a prometheus adapter which will expose the metrics to our HPA.

The HPA will then scale up and down according to that metric value.

## Installing fission

We'll be using [kafka mqtrigger type fission](/docs/usage/triggers/message-queue-trigger/kafka/) which requires some configuration to be specified while installing with helm.

Create a file [`kafka-fission-config.yaml`](https://github.com/fission/examples/blob/main/miscellaneous/newdeploy-custommetrics/kafka-config/kafka-fission-config.yaml) and paste the following configuration with the appropriate broker url.

```yaml
kafka:
  enabled: true
  # Please use the brokers link for your kafka here.
  brokers: 'my-cluster-kafka-bootstrap.kafka.svc:9092'
```

Now we can install fission.

```bash
kubectl create ns fission
helm install fission fission-charts/fission-all --namespace fission -f kafka-fission-config.yaml --version 1.16.0-rc2
```

## Setting up Apache Kafka

We'll be using [Strimzi](https://strimzi.io/) to run the Kafka cluster.
Create kafka namespace and install strimzi in it.

```bash
kubectl create ns kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
```

Wait until the `strimzi-cluster-operator` starts running.

Save the file as [`kafka-config.yaml`](https://github.com/fission/examples/blob/main/miscellaneous/newdeploy-custommetrics/kafka-config/kafka-config.yaml).
This file contains the configuration to set up the `kafka cluster` and the `kafka-exporter`.
It also defines all the kafka metrics which will be made accessible by the `kafka-exporter`.

```bash
kubectl apply -f kafka-config.yaml
```

## Creating kafka topics

We'll create the following kafka topics

- request-topic
- response-topic
- error-topic

Paste the following contents in a new yaml file. Name it [`kafka-topic.yaml`](https://github.com/fission/examples/blob/main/miscellaneous/newdeploy-custommetrics/kafka-config/kafka-topic.yaml) and apply it.

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
    name: request-topic
    labels:
        strimzi.io/cluster: "my-cluster"
spec:
    partitions: 3
    replicas: 1
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
    name: response-topic
    labels:
        strimzi.io/cluster: "my-cluster"
spec:
    partitions: 3
    replicas: 1
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
    name: error-topic
    labels:
        strimzi.io/cluster: "my-cluster"
spec:
    partitions: 3
    replicas: 1
```

```bash
kubectl apply -f kafka-topic.yaml -n kafka
```

## Setting up Prometheus monitoring

We will set up Prometheus in the `monitoring` namespace which will monitor the kafka metrics and also expose the metrics when we create the adapter.
We'll be using [kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack) to set up Prometheus on the cluster.

```bash
kubectl create ns monitoring
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false,prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

Next we have to create [`strimzi-pod-monitor.yaml`](https://github.com/fission/examples/blob/main/miscellaneous/newdeploy-custommetrics/prometheus/strimzi-pod-monitor.yaml) which will scrape the metrics from the kafka pods.

```bash
kubectl apply -f strimzi-pod-monitor.yaml -n monitoring
```

## Setting up the fission function

We'll be using the [specs](/docs/usage/spec/) feature of fission since we'll need to add the HPA to the function spec file.

```bash
fission spec init
fission env create --name nodeenv --image fission/node-env --spec
fission fn create --name consumer --env nodejs --code consumer.js --executortype newdeploy --minscale 1 --maxscale 3 --mincpu 100 --maxcpu 200 --minmemory 128 --maxmemory 256 --targetcpu 0 --spec
fission mqt create --name kafkatest --function consumer --mqtkind fission --mqtype kafka --topic request-topic  --resptopic response-topic  --errortopic error-topic --spec
```

You need to add the `hpaMetrics` field under `ExecutionStrategy` as shown below.

```yaml
apiVersion: fission.io/v1
kind: Function
metadata:
  creationTimestamp: null
  name: consumer
  namespace: default
spec:
  InvokeStrategy:
    ExecutionStrategy:
      ExecutorType: newdeploy
      MaxScale: 5
      MinScale: 1
      SpecializationTimeout: 120
      TargetCPUPercent: 0
      hpaMetrics:
      - type: Object
        object:
          metric:
            name: kafka_consumergroup_lag
          describedObject:
            apiVersion: v1
            kind: Pod
            #Change the name of the pod here
            name: my-cluster-kafka-exporter-55867498c9-pnqhz
          target:
            type: AverageValue
            averageValue: 500
    StrategyType: execution
  concurrency: 500
  environment:
    name: nodejs
    namespace: default
  functionTimeout: 60
  idletimeout: 120
  package:
    packageref:
      name: consumer-5b1d1136-c6fb-4991-aaa6-1973f9e35a7f
      namespace: default
  requestsPerPod: 1
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
```

You will need to change the pod name of the `kafka-exporter` in the spec file.

To do that run the command `kubectl get pods -n kafka` and copy the pod name of the kafka-exporter.
Replace the default value in the `name` field under `describedObject` with the copied value.

Run the `fission spec apply` command to apply the specs.
It will create an environment, a package, a newdeploy function and a kafka mqtrigger.

We need to get the uid of the mqtrigger which is also the name of the `consumergroup`.

Run the command `kubectl get messagequeuetriggers.fission.io -oyaml` and copy the `uid` field value which is under `metadata`.

## Setting up Prometheus adapter

We have kafka and prometheus both up and running, but we need an adapter to expose the custom metrics to the HPA in our newdeploy function.
So we'll install the [prometheus adapter](https://artifacthub.io/packages/helm/prometheus-community/prometheus-adapter) using helm with the provided configuration file.

We'll be using the `kafka_consumergroup_lag` metric to determine if the HPA should scale or not.

Save the file as [prometheus-adapter.yaml](https://github.com/fission/examples/blob/main/miscellaneous/newdeploy-custommetrics/prometheus_adapter/prometheus-adapter.yaml).

```yaml
prometheus:
  port: 9090
  url: http://prometheus-operated.monitoring.svc.cluster.local

rules:
  default: false
  resource: {}
  custom:
  - seriesQuery: 'kafka_consumergroup_lag'
    resources:
      overrides:
        kubernetes_namespace: {resource: "namespace"}
        kubernetes_pod_name: {resource: "pod"}
    name:
      matches: "kafka_consumergroup_lag"
      as: "kafka_consumergroup_lag"
    #Change consumergroup value
    metricsQuery: 'avg_over_time(kafka_consumergroup_lag{topic="request-topic",consumergroup="3f665dc7-6187-4593-8b81-7e4bb08f7f11"}[1m])'
```

Before installing, you'll need to change the `consumergroup` file with the uid you copied earlier.
You'll find the filter in the `metricsQuery` field.

```bash
helm install my-release prometheus-community/prometheus-adapter -f prometheus-adapter.yaml --namespace monitoring
```

If this installed correctly, you should see the metric and its value.

```bash
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1/namespaces/kafka/pods/*/kafka_consumergroup_lag
{"kind":"MetricValueList","apiVersion":"custom.metrics.k8s.io/v1beta1","metadata":{"selfLink":"/apis/custom.metrics.k8s.io/v1beta1/namespaces/kafka/pods/%2A/kafka_consumergroup_lag"},"items":[{"describedObject":{"kind":"Pod","namespace":"kafka","name":"my-cluster-kafka-exporter-55867498c9-pnqhz","apiVersion":"/v1"},"metricName":"kafka_consumergroup_lag","timestamp":"2022-05-09T12:35:58Z","value":"0","selector":null}]}
```

**NOTE**: If you are using a shell different from bash(e.g. zsh), then this might not work. Try using the following command in that scenario.

```bash
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1/namespaces/kafka/pods/%2A/kafka_consumergroup_lag
```

**Note**: If you are not getting any value, it maybe because the metric has not been defined yet. So you'll have to send some messages to the queue.

## Testing

Run a producer function to send 10000 messages to the topic `request-topic` and check the namespace `default` where the new deploy pods will be created or destroyed according to the metric value.

## Conclusion

By now you would have understood how to provide custom metrics to the HPA.
You can try exposing other kafka metrics through the prometheus adapter.
In the latest version of fission, we have added quite a few new metrics.
You can try using those metrics with the new deploy functions.

If you have any doubts, feel free to reach us at [fission slack](/slack)

## Want More?

More examples can be found in our [Examples repository on GitHub](https://github.com/fission/examples/).
Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!
