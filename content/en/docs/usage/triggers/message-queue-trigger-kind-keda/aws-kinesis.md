---
title: "AWS Kinesis"
description: "Keda based Message Queue Trigger for AWS Kinesis"
draft: false
weight: 3
---

**This guide connects an AWS Kinesis stream to a Fission function using a KEDA-based message queue trigger.**
It assumes Fission and Kubernetes are already installed — see the [install guide]({{% ref "../../../installation/_index.en.md" %}}) if not.
You'll also need an AWS Kinesis stream reachable from the Fission Kubernetes cluster.

## Installation

To set up Kinesis on the Kubernetes cluster, use [localstack](https://github.com/localstack/localstack), or create streams directly in AWS using the [Kinesis getting-started docs](https://aws.amazon.com/kinesis/data-streams/getting-started/?nc=sn&loc=3).
localstack is suited to testing and dev only — not production.

## Overview

The trigger wires together four steps:

1. A Go producer function (producerfunc) or aws cli command which acts as a producer and drops a message in a Kinesis stream named `request`.
2. Fission Kinesis trigger activates and invokes another function (consumerfunc) with body of Kinesis message.
3. The consumer function (consumerfunc) gets body of message and returns a response.
4. Fission Kinesis trigger takes the response of consumer function (consumerfunc) and drops the message in a response stream named `response`.
   If there is an error, the message is dropped in error stream named `error`.

{{% notice info %}}
When communicating with localstack, the aws CLI must be installed in the respective container (deployment) because it uses aws configuration to connect to localstack.
Below are the commands to create the streams and send a message:

```bash
$ aws kinesis create-stream --shard-count 2  --stream-name request
$ aws kinesis create-stream --shard-count 1  --stream-name response
$ aws kinesis create-stream --shard-count 1  --stream-name error
$ aws kinesis list-streams
$ aws kinesis put-record --stream-name request --partition-key 111 --data 'Test Message'
```
{{% /notice %}}

## Building the app

### Producer Function

The producer function is a go program which creates a message with timestamp and drops into a kinesis stream `request`.
For brevity all values have been hard coded in the code itself.

``` go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "strconv"

    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/credentials"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/kinesis"
)

type message struct {
    Content string `json:"content"`
}

func Handler(w http.ResponseWriter, r *http.Request) {
    region := "ap-south-1"
    config := &aws.Config{
        Region:      &region,
        Credentials: credentials.NewStaticCredentials("xxxxxxxxxxxx", "xxxxxxxxxx", ""),
    }

    s, err := session.NewSession(config)
    if err != nil {
        w.Write([]byte(fmt.Sprintf("error creating a session: %v", err)))
        return
    }

    kc := kinesis.New(s)
    for i := 11; i <= 20; i++ {
        record, err := json.Marshal(&message{
            Content: fmt.Sprintf("message count %v", i+1),
        })

        if err != nil {
            w.Write([]byte(fmt.Sprintf("error marshaling the message: %v", err)))
            return
        }
        params := &kinesis.PutRecordInput{
            Data:         record,                      // required
            PartitionKey: aws.String(strconv.Itoa(i)), // required
            StreamName:   aws.String("request"),       // required
        }
        _, err = kc.PutRecord(params)
        if err != nil {
            w.Write([]byte(fmt.Sprintf("error putting a record: %v", err)))
            return
        }
    }
    w.Write([]byte("messages sent successfully"))
}
```

Since the go program uses Kinesis stream, we need to create the request stream to run the above program.

The following commands create an environment, package, and function.
Verify that the package build succeeded before proceeding.

```sh
$ fission env create --name goenv --image ghcr.io/fission/go-env --builder ghcr.io/fission/go-builder
$ zip -qr kinesis.zip *
$ fission package create --env goenv --src kinesis.zip
Package 'kinesis-zip-cy16' created
$ fission fn create --name producerfunc --env goenv --pkg kinesis-zip-cy16 --entrypoint Handler
$ fission package info --name kinesis-zip-cy16
Name:        kinesis-zip-cy16
Environment: goenv
Status:      succeeded
Build Logs:
Building in directory /usr/src/kinesis-zip-cy16-o3vrx1
```

### Consumer function

The consumer function is nodejs function which takes the body of the request, appends a "Hello" and returns the resulting string.

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
fission fn create --name consumerfunc --env nodeenv --code hellokinesis.js
```

### Connecting via trigger

Both functions exist but aren't yet connected.
The message queue trigger below invokes consumerfunc every time a message lands in the `request` stream, sends its response to the `response` stream, and writes errors to the `error` stream.

```bash
fission mqt create  --name kinesisdeployment --function helloworld --mqtype aws-kinesis-stream --topic request --resptopic response --mqtkind keda --errortopic error --maxretries 3 --metadata streamName=request --metadata shardCount=2 --metadata awsRegion=ap-south-1 --secret awsSecrets
```

The trigger accepts these metadata parameters:

| Parameter | Description |
|---|---|
| `streamName` | Name of the AWS Kinesis stream. |
| `awsRegion` | AWS region for the Kinesis stream. |
| `shardCount` | The target value that a Kinesis data streams consumer can handle. |
| `secret` | AWS credentials required to connect to the stream — see below. |

{{% notice info %}}
With localstack, no secret is needed.
With AWS-managed Kinesis streams, provide a secret — for example:

```bash
kubectl create secret generic awsSecrets --from-env-file=./secret.yaml
```

The secret.yaml file should contain values like:

```yaml
AWS_ACCESS_KEY_ID=foo
AWS_SECRET_ACCESS_KEY=bar
```

{{% /notice %}}

### Testing it out

Invoke the producer function to put messages on the `request` stream and trigger the consumer function:

```bash
$ fission fn test --name  
Successfully sent to input
```

>> To add authentication to your function calls, refer to our [Fission Authentication](/docs/installation/authentication) guide.

There are a couple of ways you can verify that the consumerfunc is called:

- Check the logs of `mqtrigger-kinesis` pods:

```text
{"level":"info","ts":1603106377.3910372,"caller":"aws-kinesis-http-connector/main.go:212","msg":"done processing message","shardID":"shardId-000000000001","message":"Hello Msg 112"}
{"level":"info","ts":1603106377.3916092,"caller":"aws-kinesis-http-connector/main.go:212","msg":"done processing message","shardID":"shardId-000000000000","message":"Hello Msg 111"}
```

- Go to aws Kinesis stream and check if messages are coming in response stream

## Introducing an error

To trigger an error scenario, change the consumer function to return 400 instead of 200:

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
$ fission fn update --name consumerfunc --code hellokinesis.js

$ fission fn test --name producerfunc
Successfully sent to input
```

Verify the message landed in the error stream the same way as before:

- Go to aws Kinesis stream and check if messages are coming in error stream
