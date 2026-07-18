---
title: "[Removed] Message Queue Trigger: Kind Fission"
date: 2019-12-17T14:38:11+08:00
weight: 4
draft: true
description: >
  Legacy reference for the removed Fission-kind message queue trigger that invoked functions from queue messages; use the KEDA trigger instead.
---

{{% notice warning %}}
This page is legacy.
The Fission-kind message queue trigger was removed in the 1.20 release — use the [KEDA-based message queue trigger]({{% ref "../message-queue-trigger-kind-keda/_index.md" %}}) instead.
{{% /notice %}}

## How Message Queue Trigger Works

**A message queue trigger invokes a function when a message arrives on a message queue.**
Since all functions are invoked over HTTP, a component called `Message Queue Trigger` sits between the message queue and the user function to support message queuing.
It subscribes to message topics and invokes the function when needed.

{{< img "../assets/message-queue-trigger.png" "Fig.1 Overview" "45em" "1" >}}

The Message Queue Trigger watches for changes to the message queue trigger CRD (`messagequeuetriggers.fission.io`).
The command below creates a trigger that subscribes to the topic `foobar` and invokes the function `node` for each message it receives:

```bash
$ fission mqtrigger create --name hello --function node --topic foobar
```

When a message queue trigger is created with the command above, the Message Queue Trigger first subscribes to the topic `foobar` and waits for messages being published to the message queue.
As long as the Message Queue Trigger receives a message on that topic, it sends a **POST** HTTP call to function `node` with the message content as the body.

To receive a success or error response after each function invocation, add the `--resptopic` and `--errortopic` flags when creating the trigger:

```bash
$ fission mqtrigger create --name hello --function node --topic foobar \
    --resptopic foo --errortopic bar --maxretries 3
```

If a function returns a 200 HTTP status code, the MQTrigger sends the response body to `resptopic`; otherwise, the MQTrigger retries until it reaches `maxretries` and sends to `errortopic` if all invocations failed.

{{% notice warning %}}
Currently, only **NATS Streaming** and **Kafka** type of message queue trigger supports error topic.
{{% /notice %}}

The following example creates a NATS Streaming trigger with a response topic:

```bash
$ fission mqt create --name hellomsg --function hello --mqtype nats-streaming --topic newfile --resptopic newfileresponse
trigger 'hellomsg' created
```

You can list or update message queue triggers with `fission mqt list`, or `fission mqt update`.

## Message Queue Supportability

Fission now supports following kinds of message queue:

* Kafka
* [NATS Streaming]({{% ref "nats-streaming.md" %}})
* Azure Queue Storage

## How to Add New Message Queue Support

We are always looking forward to any contribution.
To add new message queue, you need to implement the [MessageQueue](https://github.com/fission/fission/blob/master/pkg/mqtrigger/messageQueue/messageQueue.go#L50-L53) interface and see [here](https://github.com/fission/fission/tree/master/pkg/mqtrigger/messageQueue) for current existing implementations.
