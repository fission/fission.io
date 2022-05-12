+++
title = "Autoscaling on Custom Metrics in New Deploy Functions"
date = "2022-05-11T14:43:46+05:30"
author = "Ankit Chawla"
description = "Implementing custom metrics for HPA scaling"
categories = ["Fission"]
type = "blog"
+++


Autoscaling is one of the key features of kubernetes because of its capability to scale up or down according to the load. This is pretty useful as optimizes cost and no human interference is required for scaling. It is intelligent enough to make its own decisions on scaling matters.

The default metric for new deploy functions to depend on is `targetCPU` which is provided by the kubernetes metrics server. But what if you want the functions to scale based on some third party software's metrics?

In our latest release of fission(`fission 1.16.0-rc2`), we have upgraded our autoscaling dependencies to `v2beta2` and fission now supports adding custom metrics to the new deploy functions.

So in this blog post we will cover scraping and exposing kafka metrics and then providing the metrics to our function.

## Prerequisites

- A Kubernetes cluster with the latest version of helm.
- The latest version of Fission-CLI on the local machine

## Steps to set up autoscaling on custom metrics

- First we will set up a strimzi kafka exporter which is going to provide the metrics that we feed to the newdeploy HPA.
- Next we will use a pod monitor to scrape the metrics from the kafka pods.
- Finally we will set up a prometheus adapter which will expose the metrics to our HPA.
The HPA will then scale up and down according to that metric value.

## Installing fission

We'll be using [kafka mqtrigger type fission](https://fission.io/docs/usage/triggers/message-queue-trigger/kafka/) which requires some configuration to be specified while installing with helm.

Create a file `kafka-fission-config.yaml` and paste the following configuration with the appropriate broker url.

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
Create the kafka namespace. Then we'll install strimzi in the namespace.

```bash
kubectl create ns kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
```

Wait until the `strimzi-cluster-operator` starts running.

Save the following file as `kafka-config.yaml`.

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
spec:
  kafka:
    replicas: 1
    listeners:
      - name: plain2
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
        authentication:
          type: tls
      - name: external
        port: 9094
        type: nodeport
        tls: false
    storage:
      type: jbod
      volumes:
        - id: 0
          type: persistent-claim
          size: 20Gi
          deleteClaim: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: kafka-metrics-config.yml
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 20Gi
      deleteClaim: false
    metricsConfig:
      type: jmxPrometheusExporter
      valueFrom:
        configMapKeyRef:
          name: kafka-metrics
          key: zookeeper-metrics-config.yml
  entityOperator:
    topicOperator: {}
    userOperator: {}
  kafkaExporter:
    groupRegex: ".*"
    topicRegex: ".*"
    logging: debug
    enableSaramaLogging: true
    readinessProbe:
      initialDelaySeconds: 15
      timeoutSeconds: 5
    livenessProbe:
      initialDelaySeconds: 15
      timeoutSeconds: 5
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: kafka-metrics
  namespace: kafka
  labels:
    app: strimzi
data:
  kafka-metrics-config.yml: |
    # See https://github.com/prometheus/jmx_exporter for more info about JMX Prometheus Exporter metrics
    lowercaseOutputName: true
    rules:
    # Special cases and very specific rules
    - pattern: kafka.server<type=(.+), name=(.+), clientId=(.+), topic=(.+), partition=(.*)><>Value
      name: kafka_server_$1_$2
      type: GAUGE
      labels:
       clientId: "$3"
       topic: "$4"
       partition: "$5"
    - pattern: kafka.server<type=(.+), name=(.+), clientId=(.+), brokerHost=(.+), brokerPort=(.+)><>Value
      name: kafka_server_$1_$2
      type: GAUGE
      labels:
       clientId: "$3"
       broker: "$4:$5"
    - pattern: kafka.server<type=(.+), cipher=(.+), protocol=(.+), listener=(.+), networkProcessor=(.+)><>connections
      name: kafka_server_$1_connections_tls_info
      type: GAUGE
      labels:
        cipher: "$2"
        protocol: "$3"
        listener: "$4"
        networkProcessor: "$5"
    - pattern: kafka.server<type=(.+), clientSoftwareName=(.+), clientSoftwareVersion=(.+), listener=(.+), networkProcessor=(.+)><>connections
      name: kafka_server_$1_connections_software
      type: GAUGE
      labels:
        clientSoftwareName: "$2"
        clientSoftwareVersion: "$3"
        listener: "$4"
        networkProcessor: "$5"
    - pattern: "kafka.server<type=(.+), listener=(.+), networkProcessor=(.+)><>(.+):"
      name: kafka_server_$1_$4
      type: GAUGE
      labels:
       listener: "$2"
       networkProcessor: "$3"
    - pattern: kafka.server<type=(.+), listener=(.+), networkProcessor=(.+)><>(.+)
      name: kafka_server_$1_$4
      type: GAUGE
      labels:
       listener: "$2"
       networkProcessor: "$3"
    # Some percent metrics use MeanRate attribute
    # Ex) kafka.server<type=(KafkaRequestHandlerPool), name=(RequestHandlerAvgIdlePercent)><>MeanRate
    - pattern: kafka.(\w+)<type=(.+), name=(.+)Percent\w*><>MeanRate
      name: kafka_$1_$2_$3_percent
      type: GAUGE
    # Generic gauges for percents
    - pattern: kafka.(\w+)<type=(.+), name=(.+)Percent\w*><>Value
      name: kafka_$1_$2_$3_percent
      type: GAUGE
    - pattern: kafka.(\w+)<type=(.+), name=(.+)Percent\w*, (.+)=(.+)><>Value
      name: kafka_$1_$2_$3_percent
      type: GAUGE
      labels:
        "$4": "$5"
    # Generic per-second counters with 0-2 key/value pairs
    - pattern: kafka.(\w+)<type=(.+), name=(.+)PerSec\w*, (.+)=(.+), (.+)=(.+)><>Count
      name: kafka_$1_$2_$3_total
      type: COUNTER
      labels:
        "$4": "$5"
        "$6": "$7"
    - pattern: kafka.(\w+)<type=(.+), name=(.+)PerSec\w*, (.+)=(.+)><>Count
      name: kafka_$1_$2_$3_total
      type: COUNTER
      labels:
        "$4": "$5"
    - pattern: kafka.(\w+)<type=(.+), name=(.+)PerSec\w*><>Count
      name: kafka_$1_$2_$3_total
      type: COUNTER
    # Generic gauges with 0-2 key/value pairs
    - pattern: kafka.(\w+)<type=(.+), name=(.+), (.+)=(.+), (.+)=(.+)><>Value
      name: kafka_$1_$2_$3
      type: GAUGE
      labels:
        "$4": "$5"
        "$6": "$7"
    - pattern: kafka.(\w+)<type=(.+), name=(.+), (.+)=(.+)><>Value
      name: kafka_$1_$2_$3
      type: GAUGE
      labels:
        "$4": "$5"
    - pattern: kafka.(\w+)<type=(.+), name=(.+)><>Value
      name: kafka_$1_$2_$3
      type: GAUGE
    # Emulate Prometheus 'Summary' metrics for the exported 'Histogram's.
    # Note that these are missing the '_sum' metric!
    - pattern: kafka.(\w+)<type=(.+), name=(.+), (.+)=(.+), (.+)=(.+)><>Count
      name: kafka_$1_$2_$3_count
      type: COUNTER
      labels:
        "$4": "$5"
        "$6": "$7"
    - pattern: kafka.(\w+)<type=(.+), name=(.+), (.+)=(.*), (.+)=(.+)><>(\d+)thPercentile
      name: kafka_$1_$2_$3
      type: GAUGE
      labels:
        "$4": "$5"
        "$6": "$7"
        quantile: "0.$8"
    - pattern: kafka.(\w+)<type=(.+), name=(.+), (.+)=(.+)><>Count
      name: kafka_$1_$2_$3_count
      type: COUNTER
      labels:
        "$4": "$5"
    - pattern: kafka.(\w+)<type=(.+), name=(.+), (.+)=(.*)><>(\d+)thPercentile
      name: kafka_$1_$2_$3
      type: GAUGE
      labels:
        "$4": "$5"
        quantile: "0.$6"
    - pattern: kafka.(\w+)<type=(.+), name=(.+)><>Count
      name: kafka_$1_$2_$3_count
      type: COUNTER
    - pattern: kafka.(\w+)<type=(.+), name=(.+)><>(\d+)thPercentile
      name: kafka_$1_$2_$3
      type: GAUGE
      labels:
        quantile: "0.$4"
  zookeeper-metrics-config.yml: |
    # See https://github.com/prometheus/jmx_exporter for more info about JMX Prometheus Exporter metrics
    lowercaseOutputName: true
    rules:
    # replicated Zookeeper
    - pattern: "org.apache.ZooKeeperService<name0=ReplicatedServer_id(\\d+)><>(\\w+)"
      name: "zookeeper_$2"
      type: GAUGE
    - pattern: "org.apache.ZooKeeperService<name0=ReplicatedServer_id(\\d+), name1=replica.(\\d+)><>(\\w+)"
      name: "zookeeper_$3"
      type: GAUGE
      labels:
        replicaId: "$2"
    - pattern: "org.apache.ZooKeeperService<name0=ReplicatedServer_id(\\d+), name1=replica.(\\d+), name2=(\\w+)><>(Packets\\w+)"
      name: "zookeeper_$4"
      type: COUNTER
      labels:
        replicaId: "$2"
        memberType: "$3"
    - pattern: "org.apache.ZooKeeperService<name0=ReplicatedServer_id(\\d+), name1=replica.(\\d+), name2=(\\w+)><>(\\w+)"
      name: "zookeeper_$4"
      type: GAUGE
      labels:
        replicaId: "$2"
        memberType: "$3"
    - pattern: "org.apache.ZooKeeperService<name0=ReplicatedServer_id(\\d+), name1=replica.(\\d+), name2=(\\w+), name3=(\\w+)><>(\\w+)"
      name: "zookeeper_$4_$5"
      type: GAUGE
      labels:
        replicaId: "$2"
        memberType: "$3"
```

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

Paste the following yaml to a file named `kafka-topic.yaml` and then apply it.

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

Now we will set up Prometheus in the `monitoring` namespace which will monitor the kafka metrics and also expose the metrics when we create the adapter.
We'll be using [kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack) to set up Prometheus on the cluster.

```bash
kubectl create ns monitoring
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false,prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

Next we have to create `strimzi-pod-monitor.yaml` which will scrape the metrics from the kafka pods.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: cluster-operator-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      strimzi.io/kind: cluster-operator
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
  - path: /metrics
    port: http
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: entity-operator-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: entity-operator
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
  - path: /metrics
    port: healthcheck
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: bridge-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchLabels:
      strimzi.io/kind: KafkaBridge
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
  - path: /metrics
    port: rest-api
---
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: kafka-resources-metrics
  labels:
    app: strimzi
spec:
  selector:
    matchExpressions:
      - key: "strimzi.io/kind"
        operator: In
        values: ["Kafka", "KafkaConnect", "KafkaMirrorMaker", "KafkaMirrorMaker2"]
  namespaceSelector:
    matchNames:
      - kafka
  podMetricsEndpoints:
  - path: /metrics
    port: tcp-prometheus
    relabelings:
    - separator: ;
      regex: __meta_kubernetes_pod_label_(strimzi_io_.+)
      replacement: $1
      action: labelmap
    - sourceLabels: [__meta_kubernetes_namespace]
      separator: ;
      regex: (.*)
      targetLabel: namespace
      replacement: $1
      action: replace
    - sourceLabels: [__meta_kubernetes_pod_name]
      separator: ;
      regex: (.*)
      targetLabel: kubernetes_pod_name
      replacement: $1
      action: replace
    - sourceLabels: [__meta_kubernetes_pod_node_name]
      separator: ;
      regex: (.*)
      targetLabel: node_name
      replacement: $1
      action: replace
    - sourceLabels: [__meta_kubernetes_pod_host_ip]
      separator: ;
      regex: (.*)
      targetLabel: node_ip
      replacement: $1
      action: replace
```

```bash
kubectl apply -f strimzi-pod-monitor.yaml -n monitoring
```

## Setting up the fission function

We'll be using the [specs](https://fission.io/docs/usage/spec/) feature of fission since we'll need to add the HPA to the function spec file.

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

Save the file as `prometheus-adapter.yaml`.

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

Run a producer function to send 10000 messages to the topic `request-topic` and check the namespace `fission-function` where the new deploy pods will be created or destroyed according to the metric value.
