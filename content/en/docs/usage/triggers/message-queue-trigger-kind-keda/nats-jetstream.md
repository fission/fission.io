---
title: "NATS Jetstream"
draft: false
description: "Keda based Message Queue Trigger for NATS Jetstream"
weight: 5
---

{{< notice info >}}
NATS Jetstream connector is available in Fission 1.17 or higher.
{{< /notice >}}

**Connect a NATS Jetstream trigger to a Fission function so the function runs automatically whenever a message arrives on a stream.**
This tutorial assumes Fission and Kubernetes are already installed.
If not, see the [install guide]({{% ref "../../../installation/_index.en.md" %}}).
You'll also need a NATS server reachable from the Fission Kubernetes cluster.

## Installation

To set up a NATS Jetstream server on the Kubernetes cluster, use the [information here](https://github.com/nats-io/k8s) or the [NATS Jetstream docs](https://docs.nats.io/running-a-nats-service/nats-kubernetes).
You can also set up a NATS Jetstream server with this [yaml](https://github.com/fission/keda-connectors/blob/master/nats-jetstream-http-connector/test/jetstream/jetstream-server.yaml) file (monitoring is already configured).

{{% notice info %}}
The NATS Jetstream KEDA connector uses NATS monitoring to scale the deployment.
To enable monitoring in NATS, pass the flags below — see [more information here](https://docs.nats.io/nats-server/configuration/monitoring) for details.

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

The response should be a success response code.

## Overview

The example wires together a producer, a consumer, and a trigger as follows:

1. A Go producer function (producer) which acts as a producer creates a stream named `input` and stream subject named `input.created`. It then pushes some message to the created stream.
2. Fission NATS Jetstream trigger activates and invokes another function (consumer) with message received from producer. In our example we have named the function - `helloworld`.
3. The consumer function (helloworld) gets body of message and returns a response.
4. Fission NATS jetstream trigger takes the response of consumer function (helloworld) and drops the message in a response stream's subject named `output.response-topic`. If there is an error, the message is dropped in error stream's subject named `erroutput.error-topic`.

## Building the app

### Producer Function

The producer function is a Go program that creates a message and drops it into the NATS Jetstream stream `input`.
For brevity all values have been hard coded in the code itself.
There are different ways to load this function into the cluster.
A reference producer implementation (standalone variant of the same logic) lives in the [keda-connectors repository](https://github.com/fission/keda-connectors/tree/main/nats-jetstream-http-connector/test/producer).

Steps for deploying producer function:

```sh
fission environment create --name go --image ghcr.io/fission/go-env-1.26 --builder ghcr.io/fission/go-builder-1.26
fission fn create --name producer --env go --src "producer/*" --entrypoint Handler 
```

The above step creates an environment `go` and creates a `producer` function in it.

The producer's Go file-

- creates a NATS connection and gets the Jetstream context
- creates the input stream, response and error response stream which are later required by the consumer
- publishes some data to the input stream

### Consumer function

The consumer function is a Go function that takes the body of the request, appends a "Hello" and returns the resulting string.

Let's create the function:

```bash
fission fn create --name helloworld --env go --src hello.go --entrypoint Handler
```

### Connecting via trigger

We have both the functions ready but the connection between them is the missing glue.
Let's create a message queue trigger which will invoke the consumer func every time there is a message in `input` stream.
The response is sent to the `output` stream.
If the consumer function invocation fails, the error is written to the `erroutput` stream.

```bash
fission mqt create --name jetstreamtest --function helloworld --mqtype nats-jetstream --mqtkind keda --topic input.created --resptopic output.response-topic --errortopic erroutput.error-topic --maxretries 3 --metadata stream=input --metadata natsServerMonitoringEndpoint=nats-jetstream.default.svc.cluster.local:8222 --metadata natsServer=nats://nats-jetstream.default.svc.cluster.local:4222 --metadata consumer=fission_consumer --metadata account=\$G
```

Each `--metadata`/flag value above maps to one of the following parameters:

| Parameter | Description |
|---|---|
| `topic` | Subject from which messages are read, generally of the form `streamname.subjectname`. |
| `resptopic` | Subject to write responses to on success, generally of the form `response_stream_name.response_subject_name`; the stream name should differ from the input stream. |
| `errortopic` | Subject to write errors to on failure, generally of the form `err_response_stream_name.error_subject_name`. |
| `maxretries` | Maximum number of times an HTTP endpoint is retried on failure. |
| `stream` | Stream the connector reads messages from. |
| `natsServerMonitoringEndpoint` | Location of the NATS Jetstream monitoring endpoint. |
| `natsServer` | Location of the NATS Jetstream server. |
| `consumer` | Consumer through which the system monitors requests and creates resources (like pods) accordingly. |
| `account` | Name of the NATS account. `$G` is the default when no account is configured. |

### Testing it out

Let's invoke the producer function to insert some messages in `input` stream.

```bash
$ fission fn test --name=producer

```

Sample output:

```bash

Order with OrderID:1 has been published
Order with OrderID:2 has been published
Order with OrderID:3 has been published
Successfully sent to request-topic
```

Two ways to verify the consumer function received the messages from the `input` stream:

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

### Notes

- The Jetstream connector creates a push-based subscriber to get the data.
Make sure the `consumer` provided in `mqt` is of type pull.
If the consumer isn't present, the connector creates it.
- The connector requires all referenced streams (`topic`, `respTopic`, `errTopic`) to already exist, or it fails.
This example creates those streams in the producer function, so the producer creates any missing stream before it publishes messages.
  