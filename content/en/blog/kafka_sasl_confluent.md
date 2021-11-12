---
title: "Kafka connector with Confluent cloud"
date: 2021-11-10T11:21:01+05:30
author: Ankit Chawla
categories: ["kafka","keda","confluent"]
draft: true
---

Confluent cloud is a popular kafka service which can be used to stream data to any cloud.
In this blog post, we will cover using kafka connector with sasl on [confluent cloud](https://www.confluent.io/).

## Prerequisites

- A Kubernetes cluster with the latest version of Fission
- The latest version of Fission-CLI on the local machine

## Setup

### Setup KEDA

We will be deploying KEDA using Helm 3. For more installation options, checkout [deploying KEDA](https://keda.sh/docs/1.5/deploy/).

1. Add Helm repo
```
$ helm repo add kedacore https://kedacore.github.io/charts
```
2. Update Helm repo
```
$ helm repo update
```
3. Install KEDA Helm chart
```
$ kubectl create namespace keda
$ helm install keda kedacore/keda --namespace keda
```

### Setup Apache Kafka on Confluent cloud

To setup Kafka on Confluent cloud, refer this [article](https://docs.confluent.io/cloud/current/get-started/index.html) till step 2.


## Setup Kafka Connect

### Creating Kafka Topics

You have to add the following topics in confluent cloud.

- request-topic
- response-topic
- error-topic

To add, edit or delete kafka topics on the Confluent cloud, refer this [article](https://docs.confluent.io/cloud/current/client-apps/topics/manage.html).

### Configuring kafka connect

Here we create a Secret object(for SASL) and ConfigMap to configure kafka keda connector to use confluent.

Update username and password in Secret object with the api_key and value you get when you create an api key. Update brokers in ConfigMap object. You would get this from Confluent Cloud cluster setting(Bootstrap Servers).

Save the following file as kafka-config.yaml.

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

Now we will create this config in the default namespace.

```shell
$ kubectl apply -f kafka-config.yaml
```

### YAML spec

Specs are used when you have to handle lots of functions. Instead of invoking each function using cli, it would be better to specify all functions in a set of yaml files. This is the recommended way to use your application in production. You can read more about specs [here](https://fission.io/docs/usage/spec/).

First we'll create a main folder and then three separate folders for specs, producer and consumer function.

```shell 
$ mkdir kafkatest && cd kafkatest
$ mkdir producer consumer
$ fission spec init
```

## Creating functions

### Creating producer function

The producer function will send 10 messages to the `request-topic` which will trigger autoscaling and run the consumer function to consume the messages.

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

Now we will create an environment, package this code and create a function.

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

The consumer function runs on the pods which consumes the messages from `request-topic` and sends the response to `response-topic`. If any error is incurred, then the message is sent to `error-topic`. This function will print the message received in the logs and send the message back in upper case.

Save the following file as consumer.go.

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
We already created the environment when we created the producer function. So now we will package this code and create a function.

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

Now we will create a trigger which will run the consumer function whenever there are messages in the `request-topic`.

Update the value of bootstrapServer with your value.

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
$ fission spec apply
```

You have to wail till the package build is successful.
```shell
$ fission package list
NAME           BUILD_STATUS ENV LASTUPDATEDAT
kafka-producer succeeded    go  08 Nov 21 14:45 IST
kafka-consumer succeeded    go  08 Nov 21 14:45 IST
```

Open another terminal and run the following command to watch for new pods that are being created.

```shell
$ kubectl pods -w
```

Now invoke the producer function.
```shell
$ fission fn test --name kafka-producer
```

Now you will be able to see new pods being created in the second terminal. If you check the logs of the created pod, you will see all the messages that were created by the producer function.










