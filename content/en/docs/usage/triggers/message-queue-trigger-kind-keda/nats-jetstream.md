---
title: "NATS Jetstream"
draft: false
description: "Keda based Message Queue Trigger for NATS Jetstream"
weight: 5
---

{{< notice info >}}
NATS Jetstream connector is available in Fission 1.17 or higher.
{{< /notice >}}

This tutorial will demonstrate how to use a NATS Jetstream trigger to invoke a function.
We'll assume you have Fission and Kubernetes installed.
If not, please head over to the [install guide]({{% ref "../../../installation/_index.en.md" %}}).

You will also need NATS server setup which is reachable from the Fission Kubernetes cluster.

## Installation

If you want to set up NATS Jetstream server on the Kubernetes cluster, you can use the [information here](https://github.com/nats-io/k8s) or you can check the documentation for nats jetstream [docs](https://docs.nats.io/running-a-nats-service/nats-kubernetes).
You can also set up NATS jetstream server with this [yaml](https://github.com/fission/keda-connectors/blob/master/nats-jetstream-http-connector/test/jetstream/jetstream-server.yaml) file.(Monitoring is already configured)

{{% notice info %}}
NATS jetstream keda connector uses NATS monitoring to scale the deployment, to enable monitoring in nats we need to pass flags as below, you can get more [information here](https://docs.nats.io/nats-server/configuration/monitoring)

```bash
-m, --http_port PORT             HTTP PORT for monitoring
-ms,--https_port PORT            Use HTTPS PORT for monitoring
```

{{% /notice %}}

```sh
$ kubectl apply -f jetstream-server.yaml
$ kubectl apply -f jetstream-server.yaml
  deployment.apps/nats-jetstream-deployment created
  service/nats-jetstream created

$ kubectl get po
NAME                                       READY   STATUS    RESTARTS   AGE
nats-jetstream-deployment-9b588f5d-vb2fv   1/1     Running   1          5h40m
```

You can find the above file [here](https://github.com/fission/keda-connectors/blob/master/nats-jetstream-http-connector/test/jetstream/jetstream-server.yaml).

Verify if monitoring endpoint is reachable by exec into any container

```sh
$ kubectl create deployment test --image=nginx
$ kubectl exec -it test-844b65666c-8kppc /bin/bash
$ curl nats-jetstream.default.svc.cluster.local:8222
```

the response should be a success response code.

## Overview

Before we dive into details, let's walk through overall flow of event and functions involved.

1. A Go producer function (producer) which acts as a producer creates a stream named `input` and stream subject named `input.created`. It then pushes some message to the created stream.
2. Fission NATS Jetstream trigger activates and invokes another function (consumer) with message received from producer. In our example we have named the function - `helloworld`.
3. The consumer function (helloworld) gets body of message and returns a response.
4. Fission NATS jetstream trigger takes the response of consumer function (helloworld) and drops the message in a response stream's subject named `output.response-topic`. If there is an error, the message is dropped in error stream's subject named `erroutput.error-topic`.

## Building the app

### Producer Function

The producer function is a go program which creates a message and drops into a NATS jetstream stream `input`.
For brevity all values have been hard coded in the code itself.
There are different ways of loading this function into cluster. We have created fission function here.
All the files required are present [here](https://github.com/fission/examples/tree/jetstream-example/miscellaneous/message-queue-trigger/nats-jetstream/producer).

Steps for deploying producer function:

```sh
fission environment create --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16
fission fn create --name producer --env go --src "producer/*" --entrypoint Handler 
```

the above step creates an environment `go` and creates a `producer` function in it.

[Go file](https://github.com/fission/examples/blob/jetstream-example/miscellaneous/message-queue-trigger/nats-jetstream/producer/main.go)

The go file mentioned above-

- creates a NATS connection and gets the Jetstream context
- creates the input stream, response and error response stream which are later required by the consumer
- publishes some data to the input stream

### Consumer function

The consumer function is golang function which takes the body of the request, appends a "Hello" and returns the resulting string. The file is present [here](https://github.com/fission/examples/blob/jetstream-example/miscellaneous/message-queue-trigger/nats-jetstream/consumer/main.go).

Let's create function:

```bash
fission fn create --name helloworld --env go --src hello.go --entrypoint Handler
```

### Connecting via trigger

We have both the functions ready but the connection between them is the missing glue.
Let's create a message queue trigger which will invoke the consumer func every time there is a message in `input` stream.
The response will be sent to `output` stream and in case of consumerfunc invocation fails, the error is written to `erroutput` stream.

```bash
fission mqt create --name jetstreamtest --function helloworld --mqtype nats-jetstream --mqtkind keda --topic input.created --resptopic output.response-topic --errortopic erroutput.error-topic --maxretries 3 --metadata stream=input --metadata natsServerMonitoringEndpoint=nats-jetstream.default.svc.cluster.local:8222 --metadata natsServer=nats://nats-jetstream.default.svc.cluster.local:4222 --metadata consumer=fission_consumer --metadata account=\$G
```

Parameter list:

- topic - Subject from which messages are read. It is generally of form - `streamname.subjectname`
- resptopic - Subject to write responses on success response. It is generally of form - `response_stream_name.response_subject_name` where streamname should be different than input stream.
- errortopic - Subject to write errors on failure. It is generally of form - `err_response_stream_name.error_subject_name`
- maxretries - Maximum number of times an http endpoint will be retried upon failure.
- stream - stream from which connector will read messages.
- natsServerMonitoringEndpoint - Location of the Nats Jetstream Monitoring
- natsServer- Location of the Nats Jetstream
- consumer - consumer is through which our system keeps monitoring the request. And creates resources(like pods) accordingly
- account - Name of the NATS account. `$G` is default when no account is configured.

### Testing it out

Let's invoke the producer function to insert some messages in `input` stream.

```bash
$ fission fn test --name=producer

```

sample output-

```bash

Order with OrderID:1 has been published
Order with OrderID:2 has been published
Order with OrderID:3 has been published
Successfully sent to request-topic
```

There are multiple ways to verify that the consumer function received the messages from input stream. Two are mentioned below-

- check for logs in the fission `helloworld` function's pod

```sh
$ fission fn pod --name=helloworld
NAME                                         NAMESPACE         READY  STATUS   IP            EXECUTORTYPE  MANAGED  
poolmgr-go-default-6312601-6d6b85ff4f-b8m7g  default  2/2    Running  10.244.0.188  poolmgr       false 
```

or

```sh
$ kubectl get pod -l functionName=helloworld
NAME                                          READY   STATUS        RESTARTS   AGE
poolmgr-go-default-6312601-6d6b85ff4f-b8m7g   2/2     Terminating   0          30m
```

Sample output:

```text
$ kubectl logs -f -c go poolmgr-go-default-6312601-6d6b85ff4f-b8m7g 
2022/08/24 06:16:17 listening on 8888 ...
2022/08/24 06:42:23 specializing ...
2022/08/24 06:42:23 loading plugin from /userfunc/deployarchive/helloworld-eb3f240a-d6bb-4728-b806-f426ce0e255a-vyh8tf-oa1sgs
2022/08/24 06:42:23 done
Hello: Test1
Hello: Test2
Hello: Test3
```

- check jetstream pods logs-

```bash
$ kubectl logs deploy/jetstreamtest
{"level":"info","ts":1661322333.8198879,"caller":"app/main.go:90","msg":"Done processing message","messsage":"Hello Test1"}
{"level":"info","ts":1661322333.8208282,"caller":"app/main.go:90","msg":"Done processing message","messsage":"Hello Test2"}
{"level":"info","ts":1661322333.8217056,"caller":"app/main.go:90","msg":"Done processing message","messsage":"Hello Test3"}
```

### Note

- Jetstream connector creates a push based subscriber to get the data. Make sure the `consumer` provided in `mqt` is of type pull. Also, if the consumer is not present connector will itself create the it.
- The connector needs all the stream mentioned(topic,respTopic,errTopic streams) to be present otherwise it will fail. For this example we have created all these streams in producer function. So before pusblisher publishes the messages it also creates the required stream if not present.
  