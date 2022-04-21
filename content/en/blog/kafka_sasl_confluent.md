---
title: "Serverless Kafka Consumer for Confluent Cloud"
date: 2021-11-10T11:21:01+05:30
author: Ankit Chawla
categories: ["Tutorials"]
draft: false
---

Confluent Cloud is a fully managed, cloud-native service for Apache Kafka.
Managed Kafka offering helps you focus on connecting and processing data, anywhere you need it.
You avoid hassle of infrastructure management.

In this blog post, we will connect with Kafka cluster hosted in [Confluent Cloud](https://www.confluent.io/) using Fission Keda Kafka Connector with SASL SSL.
Using Kafka Connector, we receive the latest messages on our desired Kafka topics and process them with Fission functions.

## Prerequisites

- A Kubernetes cluster with the latest version of Fission
- The latest version of Fission-CLI on the local machine

## Setup

### Setup KEDA

We will be deploying KEDA using Helm 3. For more installation options, checkout [deploying KEDA](https://keda.sh/docs/latest/deploy/).

1. Add Helm Repo

    ```shell
    helm repo add kedacore https://kedacore.github.io/charts
    ```

2. Update Helm Repo

    ```shell
    helm repo update
    ```

3. Install KEDA Helm chart

    ```shell
    kubectl create namespace keda
    helm install keda kedacore/keda --namespace keda
    ```

### Setup Apache Kafka on Confluent Cloud

To setup Kafka on Confluent cloud, refer [Quick Start for Apache Kafka using Confluent Cloud](https://docs.confluent.io/cloud/current/get-started/index.html) till Step 2.

## Setup Kafka Topics and Connection

### Creating Kafka Topics

You have to create the following topics in Confluent Cloud Kafka Cluster.

- `request-topic`
- `response-topic`
- `error-topic`

Refer [Managing Topics in Confluent Cloud](https://docs.confluent.io/cloud/current/client-apps/topics/manage.html) to add, edit or delete topics.

### Configuring Kafka Connection Details

The connector requires API key and secret to connect to Confluent Cloud.
In the Kafka Cluster Credentials section, click Generate Kafka API key & secret.
You would receive the API key and secret.

Here, we create a Kubernetes Secret `keda-kafka-secrets` (for SASL authentication info) and a ConfigMap `keda-kafka-configmap` to configure the Kafka Keda Connector to use with Confluent.

Update `username` and `password` in the Secret with the `api_key` and `secret` received from Confluent Cloud.
Update `brokers` in ConfigMap object with info from Confluent Cloud Cluster Setting(Bootstrap Servers).

Save the following file as `kafka-config.yaml`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: keda-kafka-secrets
  namespace: default
stringData:
  sasl: "plaintext"
  username: "<api_key>"
  password: "<value>"
  tls: "enable"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: keda-kafka-configmap
  namespace: default
data:
  brokers: "<bootstrap_server>"
  request-topic: "request-topic"
  response-topic: "response-topic"
  error-topic: "error-topic"
```

Now, we will create apply `kafka-config.yaml` manifest in the default namespace.

```console
kubectl apply -f kafka-config.yaml
```

### YAML specs

Specs are used when your want to manage multiple Fission functions in your project.
Specs are set of YAML files that describe the functions and their dependencies and make your deployment easier.
[YAML Specs](https://fission.io/docs/usage/spec/) can give you more details about the specs.

First, we'll create a main folder and then three child folders for specs, producer and consumer function.

```console
mkdir kafkatest && cd kafkatest
mkdir producer consumer
fission spec init
```

## Creating functions

### Creating producer function

Whenever the producer function is triggered, it will send 10 messages to the `request-topic` in Kafka Cluster.
This function is used to test thhe consumer function via the Kafka Connector.
Once the messages are sent, the Keda Connector will receive the messages and trigger the consumer function with received messages via HTTP request.

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
    "time"

    sarama "github.com/Shopify/sarama"
)

const (
    kafkaAuthModeNone            string = ""
    kafkaAuthModeSaslPlaintext   string = "plaintext"
    kafkaAuthModeSaslScramSha256 string = "scram_sha256"
    kafkaAuthModeSaslScramSha512 string = "scram_sha512"
    kedaSecret                          = "keda-kafka-secrets"
    kedaSecretNs                        = "default"
    kedaConfig                          = "keda-kafka-configmap"
    kedaConfigNs                        = "default"
    SaslKey                             = "sasl"
    UsernameKey                         = "username"
    PasswordKey                         = "password"
    TlsKey                              = "tls"
    BrokersKey                          = "brokers"
    RequestTopicKey                     = "request-topic"
)

func getConfigMapValue(name string, namespace string, key string) ([]byte, error) {
    return os.ReadFile(fmt.Sprintf("/configs/%s/%s/%s", namespace, name, key))
}

func getSecretValue(name string, namespace string, key string) ([]byte, error) {
    return os.ReadFile(fmt.Sprintf("/secrets/%s/%s/%s", namespace, name, key))
}

func getKafkaConfig() (*sarama.Config, error) {
    config := sarama.NewConfig()
    config.Producer.RequiredAcks = sarama.WaitForAll
    config.Producer.Retry.Max = 100
    config.Producer.Retry.Backoff = 100
    config.Producer.Return.Successes = true
    config.Version = sarama.V2_0_0_0

    sasl, err := getSecretValue(kedaSecret, kedaSecretNs, SaslKey)
    if err != nil {
        return nil, err
    }
    saslConfig := string(sasl)
    if saslConfig == kafkaAuthModeSaslPlaintext {
        config.Net.SASL.Enable = true
        user, err := getSecretValue(kedaSecret, kedaSecretNs, UsernameKey)
        if err != nil {
            return nil, err
        }
        config.Net.SASL.User = string(user)
        password, err := getSecretValue(kedaSecret, kedaSecretNs, PasswordKey)
        if err != nil {
            return nil, err
        }
        config.Net.SASL.Password = string(password)
        config.Net.SASL.Handshake = true
    } else if saslConfig == kafkaAuthModeSaslScramSha256 || saslConfig == kafkaAuthModeSaslScramSha512 {
        return nil, fmt.Errorf("scram authentication is not supported yet")
    } else if saslConfig == kafkaAuthModeNone {
        fmt.Println("Kafka authentication is disabled")
    } else {
        return nil, fmt.Errorf("unknown authentication mode: %s", saslConfig)
    }
    tls, err := getSecretValue(kedaSecret, kedaSecretNs, TlsKey)
    if err != nil {
        return nil, err
    }
    tlsConfig := string(tls)
    if tlsConfig == "enable" {
        config.Net.TLS.Enable = true
    }
    return config, nil
}

func Handler(w http.ResponseWriter, r *http.Request) {
    saramaConfig, err := getKafkaConfig()
    if err != nil {
        w.Write([]byte(fmt.Sprintf("Error getting kafka config: %s", err)))
        return
    }
    brokers, err := getConfigMapValue(kedaConfig, kedaConfigNs, BrokersKey)
    if err != nil {
        w.Write([]byte(fmt.Sprintf("Error getting kafka brokers: %s", err)))
        return
    }
    requestTopic, err := getConfigMapValue(kedaConfig, kedaConfigNs, RequestTopicKey)
    if err != nil {
        w.Write([]byte(fmt.Sprintf("Error getting kafka request topic: %s", err)))
        return
    }
    producer, err := sarama.NewSyncProducer([]string{string(brokers)}, saramaConfig)
    log.Println("Created a new producer ", producer)
    if err != nil {
        w.Write([]byte(fmt.Sprintf("Error creating kafka producer: %s", err)))
        return
    }
    count := 10
    for msg := 1; msg <= count; msg++ {
        ts := time.Now().Format(time.RFC3339)
        message := fmt.Sprintf("{\"message_number\": %d, \"time_stamp\": \"%s\"}", msg, ts)
        _, _, err = producer.SendMessage(&sarama.ProducerMessage{
            Topic: string(requestTopic),
            Value: sarama.StringEncoder(message),
        })
        if err != nil {
            w.Write([]byte(fmt.Sprintf("Failed to publish message to topic %s: %v", requestTopic, err)))
            return
        }
    }
    w.Write([]byte(fmt.Sprintf("Published %d messages to topic %s", count, requestTopic)))
}
```

Now, we will create an environment, package this code and create a function.

```shell
$ cd producer
$ go mod init github.com/kafkatest/producer

# Copy the above code and save it as producer.go

$ go mod tidy
$ cd .. && zip -j producer.zip producer/*
$ fission env create --spec --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16
$ fission package create --spec --src producer.zip --env go --name kafka-producer
$ fission fn create --spec --name kafka-producer --env go --pkg kafka-producer \
    --entrypoint Handler --secret keda-kafka-secrets --configmap keda-kafka-configmap
```

### Creating Consumer function

The consumer function runs on the pods which consumes the messages from `request-topic` and sends the response to `response-topic`.
If any error is incurred, then the message is sent to `error-topic`.
This function will print the message received in the logs and send the message back in upper case.

Save the following file as `consumer.go`.

```go
package main

import (
    "io"
    "log"
    "net/http"
    "strings"
)

func Handler(w http.ResponseWriter, r *http.Request) {
    b, _ := io.ReadAll(r.Body)
    log.Println(string(b))
    defer r.Body.Close()

    log.Println(string(b))
    s := string(b)

    w.Write([]byte(strings.ToUpper(s)))
}
```

We already created the environment, when we created the producer function.
So now we will package this code and create a function.

```shell
$ cd consumer
$ go mod init github.com/kafkatest/consumer

# Copy the code and save it as consumer.go.

$ go mod tidy
$ cd .. && zip -j consumer.zip consumer/*
$ fission package create --spec --src consumer.zip --env go --name kafka-consumer
$ fission fn create --spec --name kafka-consumer --env go --pkg kafka-consumer --entrypoint Handler
```

## Creating Message Queue Trigger

Now, we will create a trigger which will run the consumer function whenever there are messages in the `request-topic`.

Update the value of `bootstrapServer` with your value.

```shell
$ fission mqt create --spec --name kafkatest --function kafka-consumer --mqtype kafka --mqtkind keda \
    --topic request-topic --resptopic response-topic --errortopic error-topic --maxretries 3 \
    --metadata bootstrapServers=<boostrap_server> \
    --metadata consumerGroup=my-group --metadata topic=request-topic  --cooldownperiod=30 \
    --pollinginterval=5 --secret keda-kafka-secrets
```

## Testing it out

We will apply the specs first and then test the function.

```shell
fission spec apply
```

Please wail till the package build is successful.

```shell
$ fission package list
NAME           BUILD_STATUS ENV LASTUPDATEDAT
kafka-producer succeeded    go  08 Nov 21 14:45 IST
kafka-consumer succeeded    go  08 Nov 21 14:45 IST
```

Open another terminal and run the following command to watch for new pods that are being created.

```shell
kubectl pods -w
```

Now, invoke the producer function.

```shell
fission fn test --name kafka-producer
```

Now you will be able to see new pods being created in the second terminal.
If you check the logs of the created pod, you will see all the messages that were created by the producer function.

You can also see the source for this blog at [Keda Kafka Example](https://github.com/fission/examples/tree/main/miscellaneous/message-queue-trigger/kafka-keda-sasl)

You can also look at [Kafka Connector documentation](/docs/usage/triggers/message-queue-trigger-kind-keda/kafka/).

Keda Kafka Connector can be used to connect with Kakfa Cluster hosted anywhere and process the messages.

## Conclusion

With this really simple example, we got way to create simple and scalable approach to process Kafka messages.
Developers can use this approach to process any type of messages with focus on business logic.

----

If you would like to find out more about Fission:

- Get started in [fission.io](http://fission.io/).
- Check out the
  [Fission project in GitHub](https://github.com/fission/fission).
- Meet the maintainers on the
  [Fission Slack](/slack).
- Follow [@fissionio on Twitter](https://twitter.com/fissionio).
