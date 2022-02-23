+++
title = "8 Must Know Serverless Terms For A Developer"
date = "2022-02-23T11:30:34+05:30"
author = "Atulpriya Sharma"
description = "Planning to start your cloud native journey? Here are 8 Must Know Serverless Terms For A Developer."
categories = ["General"]
type = "blog"
images = ["images/featured/single-monolith-featured.png"]
+++

I’ve been a mobile developer for most of my professional career.
The transition from Java to Android wasn’t a big deal. However, over the years the entire technological landscape has transformed, thanks to serverless and microservices. Many of the mobile apps that I developed have a serverless component running somewhere on the cloud.

What that meant is that a lot of us developers had to get a hang of the serverless world.
So to help all of you looking to get started with the serverless journey, here are the **8 Must Know Serverless Terms** you should know as a developer.

## Starting Your Serverless Journey

Serverless is the present and future of the software industry.
Irrespective of what type of an IT professional you are, you would definitely have to interact with some serverless or cloud components in the future.
To help you get started quickly, here are some serverless terms you should know as a developer.

### Cloud Native

I’m sure that you are aware of what cloud computing is.
If you are not, you should read more about [cloud computing](https://glossary.cncf.io/cloud_computing/).
Cloud Native is essentially a concept of building and deploying applications in such a way that they take full advantage of the distributed cloud computing offering.

Cloud native applications leverage the services in the cloud to be more resilient, scalable and flexible.
More often than not, such applications are developed without a lot of coding, thanks to the various cloud services.
A cloud native developer would often design an application using **microservices**, deploy it on a container and run it on the cloud.

### Microservices

Back in the day, a typical application code used to be one large file with lots of lines of codes.
Developing them wasn’t easy and updating/maintaining them was a herculean task.
Realizing that problem, we started making our code more and more loosely coupled eventually leading to microservices.

Microservice architectural pattern is where a software is composed of **many small independent services** that communicate with each other using APIs.
Each of these micro services can be developed, upgraded and deployed without affecting the other services.
Each of these services have the ability to **independently scale** to meet the peak demands.

The best part that I like is that each of these services can be written in a completely different language using different tools.
So I can have an input screen in React, middleware in .NET, data layer in python and the output using Vue! And that is possible because each of these services is packaged in a container.
We have an interesting article around [single vs monolith](/blog/single-or-monolith-serverless-functions-what-should-you-choose) serverless functions that you should read.

### Container

A container is a software package that contains application code, configuration files and all the related libraries along with all the dependencies that are required to run the application.
Just like shipping containers are used to isolate the cargo on a ship, **software containers are used to isolate applications**.

One of the major problems before containers was that an application would run perfectly on one system.
But as soon as it is deployed on another system, it fails due to dependencies, libraries not being present.
Containers get rid of this problem by packaging all the dependencies, libraries along with the source code in a lightweight, immutable container.

The containerized application can be tested and deployed as a container image on any system with a host os and will guarantee that your application executes.
Some of the popular containerization tools are **Docker**, **AmazonECS**, **Azure Container Service**, **Google Container Engine**.

### Kubernetes

Applications today comprise of hundreds of microservices packaged in hundreds of containers.
As the number of containers increased, the need for a single tool to manage them all arised.
And that’s where Kubernetes came in.

An orchestration tool originally developed by Google, Kubernetes has become a **de facto container orchestration tool** today.
It allows you to manage all your containers across multiple clusters.
It is an open source tool that allows you to deploy, scale and manage your containerized applications.
Don't be consfused if you see K8s, it's just another way of denoting Kubernetes.

This is one of the most important tools you must know when you’re starting your serverless journey.
If you’re new to Kubernetes, you can check out these free videos on [School of Kubernetes](https://www.infracloud.io/kubernetes-school/).

### Serverless

As applications become increasingly complex, we want developers to focus more on the code rather than the setting up of the environment/infrastructure.
Serverless is a cloud execution model that provides an easier and cost effective way to deploy cloud native applications.

Serverless allows for **automatic provision of computing resources** to run applications either on demand or on occurrence of a specific event.
It will also scale the resources automatically in response to an increase or decreased demands.
Hence, as a developer your focus will be on writing the code while the cloud service provider will ensure you have the required resources to run it, when you need it.

### Function As a Service - FaaS

Another important offering around serverless is FaaS - *function as a service*.
As the name implies, FaaS is a **cloud computing service that allows you to execute code in response to a trigger event**.
As a developer, you will only deploy the code for a function and the cloud provider will automatically provision the resources required to execute it.
FaaS is a cost efficient mode to deploy and execute code whilst being flexible and scalable.

There are a lot of FaaS service offerings out there namely **Lambda**, **Azure Functions**, **Google Cloud Functions** to name a few.
While these offerings run on their respective clouds, there are services like [**Fission**](https://fission.io) that are open source and allow you to deploy and execute functions on Kubernetes clusters irrespective of where they reside.

### Cold Start

When we talk about function as a service, an important term that you’ll often come across is cold start.
Function as a service provides us an easy way to focus on code, and not worry about the provisioning of the underlying infrastructure.

However, every time your function is invoked, there is some time required for the system to gather all the resources for your function to execute.
That setup time is called Cold Start.
To keep the costs down, when your function is idle for a certain amount of time, the cloud provider de-provisions the resources.
If there is any invocation at this point in time, the resources are provisioned again which takes some time, *usually in milliseconds.*

In short, **the more the cold start time, the more time it will take for the function to execute**.
So one can pay more and have resources running always to eliminate cold starts.
Or, they can keep the costs down by having slightly higher execution times.
Cold start vs cost is often something that businesses need to decide.

### Infrastructure as Code

Infrastructure until now was provisioned manually by means of shell scripts.
However with the advent of cloud computing and cloud native design, the demand for accurate, reusable and disposable infrastructure increased.
It also required infrastructure to be scalable and all of this should be repeatable.

To ensure the consistency of infrastructure along with easier management, the concept of Infrastructure as code came in.
It enables you to **store infrastructure definitions in files**.
These files can then be deployed in existing CI/CD pipelines to always have a consistent infrastructure.

Some of the popular Infrastructure as code tools are **Ansible**, **Terraform**, **Puppet** and **Chef**.

## Conclusion

The world of cloud computing and serverless is a universe in itself that is vast and ever expanding.
The serverless terms mentioned above can be a good starting point for anyone who wants to embark on a cloud native journey.
While it may sound Greek and Latin at the moment, you’ll slowly understand them as you start using them.
So if you’ve been waiting to start your cloud native journey, we’ve now made it easier for you.

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)