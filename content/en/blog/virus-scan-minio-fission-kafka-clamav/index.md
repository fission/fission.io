+++
title = "Virus scan MinIO buckets using ClamAV, Fission and Kafka"
date = "2022-08-01T09:30:34+05:30"
description = "Using Fission serverless functions to perform virus scan on MinIO buckets using ClamAV and Kafka"
categories = ["Tutorials"]
type = "blog"
images = ["images/featured/scan-minio-buckets-fission.png"]
canonicalUrl="https://medium.com/@andreifer20/virus-scan-minio-buckets-using-clamav-fission-and-kafka-8a1b409c713b"
+++

All organizations want to protect their systems and have a good strategy in order to stay away from malware or other potential threats.
Before introducing files and binaries into your system organization is very important to scan them and respond immediately based on a predefined strategy.

## About Fission

Fission is an **open-source** and **Kubernetes-native serverless framework** that lets developers to run code functions easily.
Kubernetes has powerful orchestration capabilities to manage and schedule containers while Fission takes advantage of them, being flexible.
In other words, Fission can focus on developing the function-as-a-service (FaaS) features.

Fission supports many programming languages such as Pyhton, NodeJs, PHP, Go and C#.
Also, this tool allows you to create a message queue trigger like Apache Kafka, AWS SQS, AWS Kinesis, GCP Pub Sub, Nats Streaming.
In this way, the product becomes an open-source version of AWS Lambda.

Fission has three core concepts: Function, Environment , and Trigger.

1. Function: the code that is written by using a specific language for execution. In our case we have Python code.

2. Environment: the special language environment that is used to run user function

3. Trigger: used to associate functions and event sources

Refer to [Fission documentation](/docs/) to learn more about Fission.

{{< figure src="/images/featured/scan-minio-buckets-fission.png" alt="Fission serverless functions to perform virus scan on MinIO buckets" height="600" width="1000">}}

## Implementation in Action

This walkthrough will show you how to build a pipeline in order to scan your MiniIO files using asynchronous triggers.
When a new file will be pushed in our MinIO buckets
(1) a new notification will be sent to the Kafka
(2) the trigger will start the function
(3), scanning the file for viruses
(4). Process of scanning files

{{< figure src="https://miro.medium.com/max/1274/1*w_x71r3tglUp_Qgc2AooFQ.png" alt="Fission serverless functions to perform virus scan on MinIO buckets">}}

For this walkthrough, you should have the following prerequisites:

- MinIO Server and 2 buckets: test-bucket, infected-objects
- Apache Kafka and 3 topics: bucketevents, bucketevents-response, bucketevents-error
- Fission in Kubernetes environment , [install Fission](https://fission.io/docs/installation/) client CLI.

In order to implement what was described you have to follow the steps:

### Step 1- Enable MinIO to send notification using Kafka when we put new objects in the bucket

MinIO supports updating Kafka endpoints on a running MiniIO server process using the MinIO client (mc) and mc admin config set command and the notify_kafka configuration key.

    mc admin config set ALIAS/ notify_kafka:IDENTIFIER brokers="<ENDPOINT>" topic=”<string>” 

Replace IDENTIFIER with a unique descriptive string for the Kafka service endpoint.
Replace ENDPOINT with a comma separated list of Kafka brokers (e.g: 192.168.10.10:9092,192.168.10.11:9092,192.168.10.12:9092).
The topic name in our case is bucketevents.
You must restart the MinIO server process to apply any new or updated configuration settings.

Use the mc event add command to add a new bucket notification (when you put new objects ) with the configured Kafka service as a target:

    mc event add ALIAS/BUCKET arn:minio:sqs::IDENTIFIER:kafka --event put

### Step 2 - Create Python code which uses ClamAV

Here I’ve created a Python code which is available in GitHub.
You have to change MinIO credentials in order to connect to it.
Your objects will be copied inside the container and scanned using clamdscan from ClamAV.
If the file is infected will be moved to “/tmp/infected-files/” and placed in a special bucket (infected-objects) for deep investigations.

### Step 3 - Create Fission environment, function and trigger

In a default scenario Fission uses image based on language environments (in our case Python), but you can create your own image using Dockerfile.
After that, you can upload this new image in your Docker registry and when you create a new environment you will specify your custom image and secret if necessary.
Our custom image installs ClamAV and all the necessary components for scanning files.

Now, let’s create a function with python as environment:

    fission environment create --name python --image --image=YOUR_DOCKER_IMAGE --imagepullsecret="regcred"

Let’s assumed that Python code is saved in minio-scan.py file. Using this file you have to create your Fission function like so:

    fission function create --name=minio-scan --env python --code minio-scan.py

You can use the following command to create a Kafka-based message queue trigger mqt-test.
This trigger subscribes to messages of the input topic (bucketevents), and it immediately triggers function execution when it receives any message.
The function execution result is written to the output topic (bucketevents-response) if a function execution succeeds, or to the error topic(bucketevents-error) if it fails.

    fission mqt create --name mqt-test --function minio-scan --mqtype kafka --mqtkind keda --topic bucketevents --resptopic bucketevents-response --errortopic bucketevents-error --metadata bootstrapServers=ENDPOINT:PORT --metadata consumerGroup=fission-test --metadata topic=bucketevents

Replace ENDPOINT:PORT with a comma separated list of Kafka brokers

### Step 4 - Check the logs and Fission behaviour

Your function will be deployed as pod in default namespace into Kuberentes cluster.
Using kubectl logs -f -c python $POD_NAMEyou can check the logs in real time to see what happens there.
Also, you have to take a look at Kafka topics (response or error) in order to know the output of your function.

## Conclusion

Fission is a versatile framework that can be used with different programming languages that help us to build FaaS in Kubernetes.
In this scenario, I used some basic features of Fission for scanning new S3 object and I'll totally recommend you to read more regarding Fission.

**_Author:_**

**[Andrei Fer](https://www.linkedin.com/in/andrei-fer-4b0b54144)** works as a DevOps for a Public Organization in Romania.
He is always on the hunt forlatest tools and methodologies.
He aims to make bad processes better through automation, testing, and education.
Interested to Learn on the updated Technologies and also keep learning and working on the Automation and Continuous Deployment Process in Agile Technology.
