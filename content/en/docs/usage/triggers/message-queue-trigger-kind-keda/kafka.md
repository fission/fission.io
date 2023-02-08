---
title: "Apache Kafka"
description: "Keda based Message Queue Trigger for Apache Kafka"	

date: 2021-10-05T15:39:35+05:30
weight: 1
---

You can use the Kafka message queue trigger to receive messages from Apache Kafka and process them via Fission Function.
Kafka can be onpremise, hosted on Kubernetes with [Strimzi](https://strimzi.io/) or cloud based such as [Confluent Cloud](https://www.confluent.io/confluent-cloud/).

We demonstrate how to use a Kafka trigger to invoke a Fission function.
We'll assume you have Fission and Kubernetes installed.
If not, please head over to the [install guide]({{% ref "../../../installation/_index.en.md" %}}).
Please install the [Keda Helm Chart](https://keda.sh/docs/latest/deploy/#helm) in your cluster for Fission Keda Kafka trigger to work.

You will also need Kafka setup which is reachable from the Fission Kubernetes cluster.

## Installation

If you want to setup Apache Kafka on the Kubernetes cluster, you can use the [information here](https://strimzi.io/docs/operators/latest/quickstart.html#proc-product-downloads-str).

You can also use service like [Confluent Cloud](https://www.confluent.io/confluent-cloud/) to quickly setup Kafka and create required topics.

## Overview

Before we dive into details, let's walk through overall flow of event and functions involved.

1. A Go producer function (producer) which acts as a producer and drops a message in a Kafka queue named `request-topic`.
2. Fission Kafka trigger activates and invokes another function (consumer) with message received from producer.
3. The consumer function (consumer) gets body of message and returns a response.
4. Fission Kafka trigger takes the response of consumer function (consumer) and drops the message in a response queue named `response-topic`.
   If there is an error, the message is dropped in error queue named `error-topic`.

### Sample Apps

We have two samples if you want to quickly try out the trigger.

- [Keda Kafka Trigger Sample with Strimzi Kafka](https://github.com/fission/examples/tree/main/miscellaneous/message-queue-trigger/kafka-keda)
- [Keda Kafka Trigger Sample with SASL plain text authentication and Confluent Cloud](https://github.com/fission/examples/tree/main/miscellaneous/message-queue-trigger/kafka-keda-sasl)

## Building the app

### Kafka Topics

If you are using Strimzi Kafka, you need to create the following topics in Kafka.
Please replace namespace and cluster accordingly.

1. Kafka `request-topic` for function invocation

    ```shell
    cat << EOF | kubectl create -n kafka -f -
    apiVersion: kafka.strimzi.io/v1beta2
    kind: KafkaTopic
    metadata:
    name: request-topic
    labels:
        strimzi.io/cluster: "my-cluster"
    spec:
    partitions: 3
    replicas: 1
    EOF
    ```

2. Kafta `response-topic` for function response

    ```shell
    cat << EOF | kubectl create -n kafka -f -
    apiVersion: kafka.strimzi.io/v1beta2
    kind: KafkaTopic
    metadata:
    name: response-topic
    labels:
        strimzi.io/cluster: "my-cluster"
    spec:
    partitions: 3
    replicas: 1
    EOF
    ```

3. Kafta topic for error response

    ```shell
    cat << EOF | kubectl create -n kafka -f -
    apiVersion: kafka.strimzi.io/v1beta2
    kind: KafkaTopic
    metadata:
    name: error-topic
    labels:
        strimzi.io/cluster: "my-cluster"
    spec:
    partitions: 3
    replicas: 1
    EOF
    ```

4. Please ensure your topics are created in Kafka and show ready status.

### Producer Function

The producer function is a go program which creates a message with timestamp and drops into a queue `request-topic`.
For brevity all values have been hard coded in the code itself.

```go
package main

import (
    "crypto/tls"
    "fmt"
    "net/http"
    "time"

    sarama "github.com/Shopify/sarama"
)

func Handler(w http.ResponseWriter, r *http.Request) {
    brokers := []string{"my-cluster-kafka-bootstrap.kafka.svc:9092"}
    producerConfig := sarama.NewConfig()
    producerConfig.Producer.RequiredAcks = sarama.WaitForAll
    producerConfig.Producer.Retry.Max = 100
    producerConfig.Producer.Retry.Backoff = 100
    producerConfig.Producer.Return.Successes = true
    producerConfig.Version = sarama.V1_0_0_0
    
    // This code is required if you use kafka with sasl
    /*
    producerConfig.Net.SASL.User = "xxxxxxxxx"
    producerConfig.Net.SASL.Password = "xxxxxxxxxxxxxxxx"
    producerConfig.Net.SASL.Handshake = true
    producerConfig.Net.SASL.Enable = true
    producerConfig.Net.TLS.Enable = true
    tlsConfig := &tls.Config{
        InsecureSkipVerify: true,
        ClientAuth:         0,
    }
    producerConfig.Net.TLS.Config = tlsConfig
    */

    producer, err := sarama.NewSyncProducer(brokers, producerConfig)
    fmt.Println("Created a new producer ", producer)
    if err != nil {
        panic(err)
    }
    for msg := 1; msg <= 10; msg++ {
        ts := time.Now().Format(time.RFC3339)
        message := fmt.Sprintf("{\"message_number\": %d, \"time_stamp\": \"%s\"}", msg, ts)
        _, _, err = producer.SendMessage(&sarama.ProducerMessage{
            Topic: "request-topic",
            Value: sarama.StringEncoder(message),
        })

        if err != nil {
            w.Write([]byte(fmt.Sprintf("Failed to publish message to topic %s: %v", "request-topic", err)))
            return
        }
    }
    w.Write([]byte("Successfully sent to request-topic"))
}
```

{{% notice info %}}
The above example is recommended for development purposes only. For production purposes, you can checkout [YAML specs](https://fission.io/docs/usage/spec/).
If you want to use spec with SASL, you can check out this [example](https://github.com/fission/examples/tree/main/miscellaneous/message-queue-trigger/kafka-keda-sasl).
{{% /notice %}}

We are now ready to package this code and create a function so that we can execute it later.
Following commands will create a environment, package and function.
Verify that build for package succeeded before proceeding.

```shell
$ mkdir kafka_test && cd kafka_test
$ go mod init

# create a producer.go file with above code replacing the placeholder values with actual ones
$ go mod tidy
$ zip -qr kafka.zip *

$ fission env create --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16
$ fission package create --env go --src kafka.zip
$ fission fn create --name producer --env go --pkg kafka-zip-s2pj --entrypoint Handler
$ fission package info --name kafka-zip-s2pj
Name:        kafka-pkg
Environment: go
Status:      succeeded
Build Logs:
Building in directory /usr/src/kafka-zip-s2pj-wbk3yr
```

### Consumer function

The consumer function is nodejs function which takes the body of the request, appends a "Hello" and returns the resulting string.

```js
module.exports = async function (context) {
  console.log(context.request.body);
  let obj = context.request.body;
  return {
    status: 200,
    body: "Consumer Response " + JSON.stringify(obj),
  };
};
```

Let's create the environment and function:

```shell
fission env create --name nodeenv --image fission/node-env
fission fn create --name consumer --env nodeenv --code consumer.js
```

### Connecting via trigger

We have both the functions ready but the connection between them is the missing glue.
Let's create a message queue trigger which will invoke the consumer function every time there is a message in `request-topic` queue.
The response will be sent to `response-topic` queue and in case of consumer function invocation fails, the error is written to `error-topic` queue.

```bash
fission mqt create --name kafkatest --function consumer --mqtype kafka --mqtkind keda --topic request-topic --resptopic response-topic --errortopic error-topic --maxretries 3 --metadata bootstrapServers=my-cluster-kafka-bootstrap.kafka.svc:9092 --metadata consumerGroup=my-group --metadata topic=request-topic  --cooldownperiod=30 --pollinginterval=5 --secret keda-kafka-secrets
```

Parameter list:

- bootstrapServers - Kafka brokers “hostname:port” to connect to for bootstrap.
- consumerGroup - Name of the consumer group used for checking the offset on the topic and processing the related lag.
- topic - Name of the topic on which processing the offset lag.

{{% notice info %}}

If you are using kafka with sasl you need to provide the secret. Below is the example to create a secret.

```shell
kubectl apply -f secret.yaml
```

secret.yaml file should contain the secret object whose values should correspond with `parameter` name in `TriggerAuthentication.spec.secretTargetRef`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: keda-kafka-secrets
  namespace: default
stringData:
  sasl: "plaintext"
  username: "xxxxxx"
  password: "xxxxxxxxxxxxxxx"
  tls: "enable"
```

{{% /notice %}}

### Testing it out

Let's invoke the producer function so that the queue `request-topic` gets some messages and we can see the consumer function in action.

```shell
$ fission fn test --name producer
Successfully sent to request-topic
```

>> To add authentication to your function calls, refer to our [Fission Authentication](/docs/installation/authentication) guide.

There are a couple of ways you can verify that the consumer is called:

- Check the logs of `mqtrigger-kafka` pods:

```text
{"level":"info","ts":1630296782.86601,"caller":"app/main.go:58","msg":"Message sending to response successful"}
{"level":"info","ts":1630296782.8708184,"caller":"app/main.go:58","msg":"Message sending to response successful"}
```

- Connect to your kafka cluster and check if messages are coming in the `response-topic` queue or `error-topic` in case of error.

## Debugging

For debugging, you can check the logs of the pods created in the `fission` and `default` namespace.

Typically, all function pods would be created in the `default` namespace.
Based on the environment name, the pods would be created in the `default` namespace.
You can check consumer and producer function logs.

## Introducing an error

Let's introduce an error scenario - instead of consumer function returning a 200, you can return 400 which will cause an error:

```js
module.exports = async function (context) {
  console.log(context.request.body);
  let obj = context.request.body;
  return {
    status: 400,
    body: "Hello " + JSON.stringify(obj),
  };
};
```

Update the function with new code and invoke the producer function:

```bash
$ fission fn update --name consumer --code consumer.js

$ fission fn test --name producer
Successfully sent to input
```

We can verify the message in error queue as we did earlier:

- Connect to your kafka cluster and check if messages are coming in `error-topic` queue.

Do checkout [Sample apps](#sample-apps) mentioned above for end to end working example.
