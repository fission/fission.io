---
title: "Redis Lists"
draft: false
description: "Keda based Message Queue Trigger for Redis"
weight: 8
---

**This tutorial shows how to trigger a Fission function from messages on a Redis list.**
We'll assume you have Fission and Kubernetes installed.
If not, head over to the [install guide]({{% ref "../../../installation/_index.en.md" %}}).

You will also need Redis setup which is reachable from the Fission Kubernetes cluster.

## Installation

If you want to setup Redis server on the Kubernetes cluster, you can use the [information here](https://ot-container-kit.github.io/redis-operator/guide).

## Overview

The flow connects two functions through a Redis trigger:

1. A Go producer function (producerfunc) which acts as a producer and drops a message in a Redis queue named `request-topic`.
2. Fission Redis trigger activates and invokes another function (consumerfunc) with message received from producerfunc.
3. The consumer function (consumerfunc) gets body of message and returns a response.
4. Fission Redis trigger takes the response of consumer function (consumerfunc) and drops the message in a response queue named `response-topic`.
   If there is an error, the message is dropped in error queue named `error-topic`.

## Building the app

### Producer Function

The producer function is a Go program which creates a message with timestamp and drops into a queue `request-topic`.
For brevity all values have been hard coded in the code itself.

```go
package main
​
import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "strconv"
    "time"

    "github.com/go-redis/redis/v8"
)

type publish_data struct {
    Sid  int    `json:"sid"`
    Data string `json:"data"`
    Time int64  `json:"time"`
}

func Handler(w http.ResponseWriter, r *http.Request) {

    address := "redis-headless.ot-operators.svc.cluster.local:6379"
    password := ""
    listName := "request-topic"

    var ctx = context.Background()
    rdb := redis.NewClient(&redis.Options{
        Addr:     address,
        Password: password,
        DB:       0,
    })

    for i := 0; i < 10; i++ {
        current_time := time.Now()
        secs := current_time.Unix()
        resp := publish_data{
            Sid:  i,
            Data: "Message number: " + strconv.Itoa(i+1),
            Time: secs,
        }
        resp_json, _ := json.Marshal(resp)
        _, err := rdb.RPush(ctx, listName, resp_json).Result()
        if err != nil {
            w.Write([]byte(fmt.Sprintf("Failed to publish message to topic %s: %v", listName, err)))
            return
        }
    }
    w.Write([]byte(fmt.Sprintf("Successfully sent to %s", listName)))
}
```

Package this code and create a function.
The following commands create an environment, package, and function.
Verify that the package build succeeded before proceeding.

```sh
$ mkdir redis_test && cd redis_test
$ go mod init

# create a producer.go file with above code replacing the placeholder values with actual ones
$ go mod tidy
$ zip -qr redis.zip *

$ fission env create --name goenv --image ghcr.io/fission/go-env-1.26 --builder ghcr.io/fission/go-builder-1.26
$ fission package create --env goenv --src redis.zip
$ fission fn create --name producerfunc --env goenv --pkg redis-zip-zlre --entrypoint Handler
$ fission package info --name redis-zip-zlre
Name:        redis-pkg
Environment: goenv
Status:      succeeded
Build Logs:
Building in directory /usr/src/redis-zip-zlre-2gucll
```

### Consumer function

The consumer function is a Node.js function which takes the body of the request, appends a "Hello" and returns the resulting string.

```js
module.exports = async function (context) {
  console.log(context.request.body);
  let obj = context.request.body;
  return {
    status: 200,
    body: "Hello " + JSON.stringify(obj),
  };
};
```

Let's create the environment and function:

```bash
fission env create --name nodeenv --image ghcr.io/fission/node-env
fission fn create --name consumerfunc --env nodeenv --code hello.js
```

### Connecting via trigger

Both functions exist, but nothing connects them yet.
Create a message queue trigger that invokes consumerfunc every time a message arrives in the `request-topic` queue.
The response goes to the `response-topic` queue; if the consumerfunc invocation fails, the error goes to the `error-topic` queue.

```bash
fission mqt create --name redistest --function consumerfunc --mqtype redis --mqtkind keda --topic request-topic --resptopic response-topic --errortopic error-topic --maxretries 3 --metadata address=redis-headless.ot-operators.svc.cluster.local:6379 --metadata listLength=10 --metadata listName=request-topic
```

The `--metadata` flags above configure the trigger:

| Parameter | Description |
|---|---|
| `address` | Host and port of the Redis server |
| `listLength` | Length of list after which the function should be triggered |
| `listName` | The list to be monitored |

### Testing it out

Let's invoke the producer function so that the queue `request-topic` gets some messages and we can see the consumer function in action.

```bash
$ fission fn test --name producerfunc
Successfully sent to request-topic
```

>> To add authentication to your function calls, refer to our [Fission Authentication](/docs/installation/authentication) guide.

There are a couple of ways you can verify that the consumerfunc is called:

- Check the logs of `mqtrigger-redis` pods:

```text
{"level":"info","ts":1630296782.86601,"caller":"app/main.go:58","msg":"Message sending to response successful"}
{"level":"info","ts":1630296782.8708184,"caller":"app/main.go:58","msg":"Message sending to response successful"}
```

- Connect to your redis server and check if messages are coming in the `response-topic` queue.

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
$ fission fn update --name consumerfunc --code hello.js

$ fission fn test --name producerfunc
Successfully sent to input
```

We can verify the message in the error queue as we did earlier:

- Connect to your redis server and check if messages are coming in `error-topic` queue.
