---
title: "Message Queue Trigger: Kind Keda"
description: "Keda based Message Queue Trigger"
date: 2020-07-20T14:30:01+05:30
weight: 3
---

_This is a new feature getting released in 1.11._

## Brief Introduction

Message queue trigger integration with KEDA has enabled autoscaling of trigger handler.
Now, there are two kinds of message queue triggers:

1. fission
2. keda

Message queue trigger kind can be specified using `mqtkind` flag.

{{% notice info %}}

Starting from fission version 1.16, the default value of the flag `--mqtkind` is keda. To create the regular [message queue trigger](/docs/usage/triggers/message-queue-trigger/) one must specify `--mqtkind=fission`.

{{% /notice %}}

## Architecture

{{< img "../assets/mqt-kind-keda.png" "" "40em" "1" >}}

1. The user creates a trigger adding all relevant parameters.
   These parameters are different for each message queue and hence are encapsulated in a metadata field and follow a key-value format.
   As soon as you create the MQ Trigger, Fission creates a ScaledObject and a consumer deployment object which is referenced by ScaledObject.
   The ScaledObject is a Keda’s way of encapsulating the consumer deployment and all relevant information for connecting to an event source!
   Keda goes ahead and creates a HPA for the deployment and scales down the deployment to zero.
2. As the message arrives in the event source - the Keda will scale the HPA and deployment from 0 - to 1 for consuming messages.
   As more messages arrive the deployment is scaled beyond 1 automatically too.
3. The deployment is like an connector which consumes messages from the source and then calls a function.
4. The function consumes the message and returns the response to deployment pods, which puts the response in response topic and errors in error topic as may be applicable.

## Usage

### Prerequisite

- KEDA [must be installed](https://keda.sh/docs/latest/deploy/#helm) on your cluster
- Message queue trigger KEDA integration should be enabled.

To enable integration set the value `mqt_keda.enabled` to `true` while installing Fission with helm chart.

When you create a message queue trigger of kind keda, it creates [a ScaledObject and a TriggerAuthentication](https://keda.sh/docs/latest/concepts/#custom-resources-crd).
The ScaledObjects represent the desired mapping between an event source (e.g. Apache Kafka) and the Kubernetes deployment.
A ScaledObject may also reference a TriggerAuthentication which contains the authentication configuration or secrets to monitor the event source.
For successful creation of these objects, user should specify the following fields while creating a message queue trigger.

1. pollinginterval: Interval to check the message source for up/down scaling operation of consumers
2. cooldownperiod: The period to wait after the last trigger reported active before scaling the consumer back to 0
3. minreplicacount: Minimum number of replicas of consumers to scale down to
4. maxreplicacount: Maximum number of replicas of consumers to scale up to
5. metadata: Metadata needed for connecting to source system in format: `--metadata key1=value1 --metadata key2=value2`
6. secret: Name of secret object (secret fields must be similarly specified as in mentioned for [particular scaler](https://keda.sh/docs/latest/scalers/))
