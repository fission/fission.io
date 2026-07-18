---
title: "AWS SQS"
description: "Keda based Message Queue Trigger for AWS SQS"	
draft: false
weight: 2
---

**This tutorial shows you how to connect an AWS SQS queue to a Fission function using a KEDA-based message queue trigger.**
We'll assume you have Fission and Kubernetes installed.
If not, head over to the [install guide]({{% ref "../../../installation/_index.en.md" %}}).

You will also need AWS SQS setup which is reachable from the Fission Kubernetes cluster.

## Installation

If you want to setup SQS on the Kubernetes cluster, you can use the [information here](https://github.com/localstack/localstack) or you can create queue using your aws account [docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-setting-up.html).  

Localstack is only for testing and dev environments — not for production usage.

## Overview

Here's the overall flow of events and functions involved.

1. A Go producer function (producerfunc) or aws cli command which acts as a producer and drops a message in a SQS queue named `input`.
2. Fission SQS trigger activates and invokes another function (consumerfunc) with body of SQS message.
3. The consumer function (consumerfunc) gets body of message and returns a response.
4. Fission SQS trigger takes the response of consumer function (consumerfunc) and drops the message in a response queue named `output`.
   If there is an error, the message is dropped in error queue named `error`.

{{% notice info %}}
When communicating to localstack we need aws cli installed in the respective container (deployment).
This is because it uses aws configuration to connect to localstack.
Below are the commands to create a queue and send a message to it.

```bash
aws sqs create-queue --queue-name input
aws sqs create-queue --queue-name output
aws sqs create-queue --queue-name error
aws sqs list-queues
aws sqs send-message --queue-url https://sqs.ap-south-1.amazonaws.com/xxxxxxxx/input --message-body 'Test Message!'
```

{{% /notice %}}

## Building the app

### Producer Function

The producer function is a Go program which creates a message with a timestamp and drops it into the `input` queue.
For brevity all values have been hard coded in the code itself.

``` go
package main
​
import (
    "fmt"
    "log"
​
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/credentials"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sqs"
)
​
func Handler(w http.ResponseWriter, r *http.Request) {​
    queueURL := "https://sqs.ap-south-1.amazonaws.com/xxxxxxxxxxxx/input"
    region := "ap-south-1"
    config := &aws.Config{
        Region:      &region,
        Credentials: credentials.NewStaticCredentials("xxxxxxxxxxxx", "xxxxxxxxxx", ""),
    }
​
    sess, err := session.NewSession(config)
    if err != nil {
        log.Panic("Error while creating session")
    }
    svc := sqs.New(sess)
​
    for i := 100; i < 200; i++ {
        msg := fmt.Sprintf("Hello Msg %v", i+1)
        _, err := svc.SendMessage(&sqs.SendMessageInput{
            DelaySeconds: aws.Int64(10),
            MessageBody:  &msg,
            QueueUrl:     &queueURL,
        })
        if err != nil {
            log.Panic("Error while writing message")
        }
    }
}
```

Since the Go program writes to the SQS queue, you need to create the `input` queue before running it.

We are now ready to package this code and create a function so that we can execute it later.
The following commands create an environment, package, and function.
Verify that the package build succeeded before proceeding.

```sh
$ mkdir sqs && cd sqs
$ go mod init

# create a producer.go file with above code replacing the placeholder values with actual ones
$ go mod tidy
$ zip -qr sqs.zip *

$ fission env create --name goenv --image ghcr.io/fission/go-env --builder ghcr.io/fission/go-builder
$ fission package create --env goenv --src sqs.zip
$ fission fn create --name producerfunc --env goenv --pkg sqs-zip-xpoi --entrypoint Handler
$ fission package info --name sqs-zip-xpoi
Name:        sqs-zip-xpoi
Environment: go-sqs
Status:      succeeded
Build Logs:
Building in directory /usr/src/sqs-zip-xpoi-1bicov
```

### Consumer function

The consumer function is a Node.js function which takes the body of the request, appends "Hello", and returns the resulting string.

```js
module.exports = async function (context) {
    console.log(context.request.body);
    let obj = context.request.body;
    return {
        status: 200,
        body: "Hello "+ JSON.stringify(obj)
    };
}
```

Let's create the environment and function:

```bash
fission env create --name nodeenv --image ghcr.io/fission/node-env
fission fn create --name consumerfunc --env nodeenv --code hellosqs.js
```

### Connecting via trigger

We have both the functions ready but the connection between them is the missing glue.
Let's create a message queue trigger which will invoke the consumerfunc every time there is a message in `input` queue.
The response will be sent to `output` queue and in case of consumerfunc invocation fails, the error is written to `error` queue.

```bash
fission mqt create  --name sqstest --function consumerfunc --mqtype aws-sqs-queue --topic input --resptopic output --mqtkind keda --errortopic error --metadata queueURL=https://sqs.ap-south-1.amazonaws.com/xxxxxxxx/input --metadata awsRegion=ap-south-1 --secret awsSecrets
```

Parameter list:

| Parameter | Description |
|---|---|
| `queueURL` | Full URL for the SQS queue |
| `awsRegion` | AWS region for the SQS queue |
| `secret` | AWS credentials required to connect to the queue (example below) |

{{% notice info %}}
With localstack you don't need to provide a secret.
With AWS SQS you do — here's an example of creating one.

```bash
kubectl create secret generic awsSecrets --from-env-file=./secret.yaml
```

The `secret.yaml` file should contain values that correspond to the `parameter` name in `TriggerAuthentication.spec.secretTargetRef`, for example:

```yaml
awsAccessKeyID=foo 
awsSecretAccessKey=bar
```

{{% /notice %}}

### Testing it out

Let's invoke the producer function so that the queue `input` gets some messages and we can see the consumer function in action.

```bash
$ fission fn test --name producerfunc
Successfully sent to input
```

>> To add authentication to your function calls, refer to our [Fission Authentication](/docs/installation/authentication) guide.

There are a couple of ways you can verify that the consumerfunc is called:

- Check the logs of `mqtrigger-sqs` pods:

```text
{"level":"info","ts":1602057916.444865,"caller":"app/main.go:165","msg":"message deleted"}
{"level":"info","ts":1602057917.4880567,"caller":"app/main.go:165","msg":"message deleted"}
```

- Go to the AWS SQS queue and check if messages are coming in on the `output` queue.

## Introducing an error

Let's introduce an error scenario - instead of the consumer function returning a 200, you can return 400 which will cause an error:

```js
module.exports = async function (context) {
    console.log(context.request.body);
    let obj = context.request.body;
    return {
        status: 400,
        body: "Hello "+ JSON.stringify(obj)
    };
}
```

Update the function with new code and invoke the producer function:

```bash
$ fission fn update --name consumerfunc --code hellosqs.js

$ fission fn test --name producerfunc
Successfully sent to input
```

We can verify the message in the error queue as we did earlier:

- Go to the AWS SQS queue and check if messages are coming in on the `error` queue.
