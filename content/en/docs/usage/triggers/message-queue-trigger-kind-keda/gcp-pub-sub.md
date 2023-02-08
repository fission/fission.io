---
title: "GCP Pub Sub"
description: "Keda based Message Queue Trigger for GCP Pub Sub"	

date: 2022-01-25T11:39:35+05:30
weight: 4
---

Fission supports Message Queue Trigger using Google Cloud Platform's Pub Sub via Keda.
GCP PubSub is a global messaging system for event driven systems and streaming analytics.
With Fission's Keda based message queue trigger, you can leverage GCP's PubSub system to create an event driven application.

In this document we will demonstrate how to use a GCP PubSub trigger to invoke a Fission function.

## Pre requisites

We'll assume you have Fission and Kubernetes installed.
If not, please head over to the [Fission install guide]({{% ref "../../../installation/_index.en.md" %}}).

> To enable KEDA integration, set the flag `mqt_keda.enabled` to `true` while installing Fission with helm chart.

You need to install [Keda Helm Chart](https://keda.sh/docs/latest/deploy/#helm) in your cluster for Fission Keda GCP Pubsub trigger to work.

### Google Cloud Platform - PubSub

You will need an active Google Cloud account for this demo.
If you don't have one, you can register for a [Google Cloud Account](https://cloud.google.com/).

#### Creating a Project and Topics

To start with this demo, we will create a project followed by three topics

1. Create a **New Project** by providing a name.
2. In the search bar, search for **PubSub**.
3. Click on **Create Topic** button and give a **Topic ID** to create a topic.
4. Create three topics: `request-topic`, `response-topic` & `error-topic`.

{{< img "../images/gcp-pub-sub-topics.png" "" "60em" "1" >}}
Creating Topics in Google Cloud Platform Pub Sub

#### Setting up Authentication

When dealing with an external system, authentication is extremely important.
In this section we will setup authentication to ensure that only our Fission function can send & receive messages from the message queue.
You can refer to the detailed [Steps to Setup Authentication](https://cloud.google.com/pubsub/docs/reference/libraries#setting_up_authentication) for GCP PubSub.

If you followed this correctly, you will have a `json` file downloaded to your system with the credentials.

## Overview

Before we dive into details, let us walk through the overall flow of events and functions involved.

1. A Python producer function (*producer*) that drops a message in a GCP PubSub queue named `request-topic`.
2. Fission GCP PubSub trigger that activates upon message arrival in `request-topic` and invokes another function (*consumer*) with message received from producer.
3. The consumer function (*consumer*) gets body of message and returns a response.
4. Fission GCP PubSub trigger takes the response of consumer function (*consumer*) and drops the message in a response queue named `response-topic`.
   If there is an error, the message is dropped in error queue named `error-topic`.

### Sample App

You can get the source code for the sample app explained in this document in our [Keda GCP PubSub Trigger Repo](https://github.com/fission/examples/tree/main/miscellaneous/message-queue-trigger/keda-gcppubsub)

## Building the app

### Secret

We will first create a `secret.yaml` file that will contain the credentials for our function to connect to GCP queue to send and receive messages.
This demo requires `GoogleApplicationCredentials` env variable to be set.
Using the following command, we'll create the required secret.

```bash
kubectl create secret generic pubsub-secret --from-file=GoogleApplicationCredentials=filename.json --from-literal=PROJECT_ID=project_id
```

*Replace the filename and project_id with your values*

### Publisher Function

The publisher function is a Python program which creates a message with a number and drops into a queue `request-topic`.

```Python
from google.cloud import pubsub_v1
import os

path = os.path.dirname(os.path.realpath(__file__))

# GCP Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path+"/filename.json"

# Project and Topic Ids
project_id = "projectid"
topic_id = "request-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def main():

    for n in range(1, 100):
        data = f"Message number {n}"
        # Data must be a bytestring
        data = data.encode("utf-8")
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        print(future.result())

    print(f"Published messages to {topic_path}.")

    return "Messages Published!"
```

Create a zip archive of `publisher` folder using `zip -j pub.zip pub/*`

Let's create the environment, package and function:

```bash
fission env create --name python-gcp --image fission/python-env --builder fission/python-builder
fission fn create --name producer --env python-gcp --src pub/pub.py  --entrypoint main --src pub/requirements.txt
```

### Consumer Function

The consumer function is a NodeJS program which takes the body of the request, process the message and drops it in the `response-queue`

```js
module.exports = async function (context) {
    console.log(context.request.body);
    let obj = context.request.body;
    return {
        status: 200,
        body: "Consumer Response "+ JSON.stringify(obj)
    };
}
```

Creating the consumer function:

```bash
fission fn create --name consumer --env nodeenv --code consumer.js
```

### Connecting via trigger

Now that we have both Publisher and Consumer functions ready, let's create the Trigger.
This message queue trigger will invoke the consumer function every time there is a message in `request-topic` queue.
The response will be sent to `response-topic` queue and in case of consumer function invocation fails, the error is written to `error-topic` queue.

```bash
fission mqt create --name gcptest --function consumer --mqtype gcp-pubsub --mqtkind keda \
    --topic request-topic-sub --resptopic response-topic --errortopic error-topic \
    --maxretries 3 --cooldownperiod=30 --pollinginterval=5 --metadata subscriptionName=request-topic-sub \
    --metadata credentialsFromEnv=GoogleApplicationCredentials --secret pubsub-secret
```

Parameter list:

- subscriptionName - Name of the subscription for the request queue for which the trigger is created.
- credentialsFromEnv - GCP credentials for authentication.

### Specs

You can also use the following Fission spec.
Read our giude on how to use [Fission spec](https://fission.io/docs/usage/spec/).

```bash
fission spec init
fission env create --name python-gcp --image fission/python-env --builder fission/python-builder --spec
fission fn create --name producer --env python-gcp --src pub/pub.py  --entrypoint main --src pub/requirements.txt --spec
fission env create --name nodeenv --image fission/node-env --spec
fission fn create --name consumer --env nodeenv --code consumer.js --spec
fission mqt create --name gcptest --function consumer --mqtype gcp-pubsub --mqtkind keda \
    --topic request-topic-sub --resptopic response-topic --errortopic error-topic --maxretries 3 \
    --cooldownperiod=30 --pollinginterval=5 --metadata subscriptionName=request-topic-sub \
    --metadata credentialsFromEnv=GoogleApplicationCredentials --secret pubsub-secret --spec
fission spec apply
```

## Testing it out

Let's invoke the producer function so that the queue `request-topic` gets some messages and we can see the consumer function in action.

```shell
$ fission fn test --name producer
3845235698474295
3845233690419265
3845239134812172
3845232823384352
3845239513065630
Published messages to projects/projectid/topics/request-topic.
Messages Published!
```

>> To add authentication to your function calls, refer to our [Fission Authentication](/docs/installation/authentication) guide.

To verify if the messages were successfully sent, navigate to the Google Cloud console and observe the `request-topic-sub` subscription and verify the count of messages sent.

{{< img "../images/gcp-pub-sub-queue.png" "" "60em" "1" >}}
Messages in the GCP Pub/Sub request queue

If you've followed the tutorial correctly, the message queue trigger will be triggered and our `consumer` function will be invoked.

When the consumer function is invoked, it will process the message in the `request-topic` and push them to the `response-topic`.
We can verify the same by checking the messages in the `response-topic` on the GCP console.

{{< img "../images/gcp-pub-sub-response-queue.png" "" "60em" "1" >}}
Messages in the GCP Pub/Sub response queue

## Debugging

For debugging, you can check the logs of the pods created in the `fission` and `default` namespace.

Typically, all function pods would be created in the `default` namespace.
Based on the environment name, the pods would be created in the `default` namespace.
You can check consumer and producer function logs.

Try out the [Sample app](#sample-app) to see it in action.
