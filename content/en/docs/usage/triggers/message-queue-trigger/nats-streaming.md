---
title: "Fission NATS Streaming"
weight: 2
draft: true
description: >
  Legacy reference for the removed Fission-kind NATS Streaming message queue trigger; use the KEDA-based NATS Streaming trigger instead.
---

{{% notice warning %}}
This page covers the legacy Fission-kind NATS Streaming trigger, which was removed in the 1.20 release.
Use the [KEDA-based NATS Streaming trigger]({{% ref "../message-queue-trigger-kind-keda/nats-streaming.md" %}}) instead.
{{% /notice %}}

{{% notice info %}}
Fission uses [**NATS Streaming**](https://github.com/nats-io/nats-streaming-server) instead of pure [NATS](https://nats.io/) as the default message queue service.</br>
Use the correct client library to connect to the NATS Streaming service.
{{% /notice %}}

## Installation

Fission installs the NATS streaming service by default when the `fission-all` helm chart is used for installation.
You can change the default setting in [values.yaml](https://github.com/fission/fission/blob/38f96c7e46e3be8d91014dd6f0aac9965d627459/charts/fission-all/values.yaml#L120-L125) before installation or upgrade.

Confirm the service is running by checking for a pod with the `nats-streaming` prefix.

```bash
kubectl -n fission get pod -l svc=nats-streaming
```

If NATS Streaming is enabled, a Kubernetes deployment called `mqtrigger-nats-streaming` is also created.

```bash
kubectl -n fission get deploy|grep mqtrigger-nats-streaming
```

The message queue trigger talks to NATS Streaming through a Kubernetes service; get the service information with this command.

```bash
$ kubectl -n fission get svc -l svc=nats-streaming
NAME             TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
nats-streaming   ClusterIP   10.97.32.55   <none>        4222/TCP   6d
```

{{% notice info %}}
For further nats-streaming configuration/operation, visit the [NATS docs](https://docs.nats.io/).
{{% /notice %}}

## Connection Information

These are the default connection values from the Helm installation.
(To change them, see the nats section of [values.yaml](https://github.com/fission/fission/blob/master/charts/fission-all/values.yaml).)

- **Authentication Token**: `defaultFissionAuthToken`
- **NATS Streaming ClusterID**: `fissionMQTrigger`

The FQDN of the nats-streaming server is `nats-streaming:4222` by default, or `nats-streaming.fission:4222` if the producer is in a different namespace.
So the full connection information for the NATS client is

```bash
nats://defaultFissionAuthToken@nats-streaming:4222
```

If the connection information changes, update the environment variable of the mqtrigger-nats-streaming deployment as well.

```bash
kubectl -n fission edit deployment mqtrigger-nats-streaming
```

## Local Test

Create a message queue trigger that invokes any function you created before.

```bash
fission mqt create --name hello --function hello1 --topic foobar --mqtkind fission
```

To test the setup locally, forward local port traffic to the nats-streaming server in the Kubernetes cluster.

```bash
export NATS_POD=$(kubectl -n fission get pod -l svc=nats-streaming -o name)
kubectl -n fission port-forward ${NATS_POD} 4222:4222
```

This lets you connect to the nats-streaming server locally at `127.0.0.1:4222`.
(**NOTICE**: for local test only)

```bash
cd ${GOPATH}/src/github.com/fission/fission/test/tests/mqtrigger/nats
go run stan-pub.go -s nats://defaultFissionAuthToken@127.0.0.1:4222 -c fissionMQTrigger -id clientPub foobar ""
```

Then, you should see the function invocation logs.

```bash
$ fission fn logs --name hello1
[2018-12-17 07:57:44.383563857 +0000 UTC] 2018/12/17 07:57:44 fetcher received fetch request and started downloading: {1 {hello-js-60kj  default    0 0001-01-01 00:00:00 +0000 UTC <nil> <nil> map[] map[] [] nil [] }   user [] [] false}
[2018-12-17 07:57:44.563666772 +0000 UTC] 2018/12/17 07:57:44 Successfully placed at /userfunc/user
[2018-12-17 07:57:44.563726739 +0000 UTC] 2018/12/17 07:57:44 Checking secrets/cfgmaps
[2018-12-17 07:57:44.563734156 +0000 UTC] 2018/12/17 07:57:44 Completed fetch request
[2018-12-17 07:57:44.563739212 +0000 UTC] 2018/12/17 07:57:44 elapsed time in fetch request = 299.120419ms
[2018-12-17 07:57:44.648270717 +0000 UTC] user code loaded in 0sec 0.240217ms
[2018-12-17 07:57:44.659143091 +0000 UTC] ::ffff:172.17.0.28 - - [17/Dec/2018:07:57:44 +0000] "POST /specialize HTTP/1.1" 202 - "-" "Go-http-client/1.1"
[2018-12-17 07:57:44.675180546 +0000 UTC] ::ffff:172.17.0.10 - - [17/Dec/2018:07:57:44 +0000] "POST / HTTP/1.1" 200 14 "-" "Go-http-client/1.1"
```

## Example

The diagram below shows a working example: a function publishes messages, and the message queue trigger invokes another function in response.

{{< img "../assets/nats-example.png" "" "40em" "1" >}}

The function `publisher` publishes a message to the target topic `foobar`.
When the message queue trigger receives the message, it sends a POST request to the function `hello`.

You can find the fully workable example source code [here](https://github.com/fission/examples/tree/main/miscellaneous/message-queue-trigger/nats-streaming).
