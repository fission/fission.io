+++
title = "8 Must Know Terms For A Serverless Developer"
date = "2022-03-03T15:30:34+05:30"
author = "Atulpriya Sharma"
description = "Are you building a serverless application? Here are 8 terms you must know as a serverless developer."
categories = ["General"]
type = "blog"
images = ["/images/featured/serverless-developer.png"]
+++

I’ve been a mobile developer for most of my professional career.
The transition from Java to Android wasn’t a big deal.
However, most of the mobile apps today have shifted their backend to serverless.
This makes mobile apps more light-weight and improves their maintainability.

As I set out to build and learn more about serverless applications, I'd like to share my learnings with you.
This post lists **8 terms you must know as a serverless developer**.

{{< figure src="/images/featured/serverless-developer.png" alt="Are you building a serverless application? Here are 8 terms you must know as a serverless developer." height="600" width="1000">}}

## Terms You Should Know As A Serverless Developer

Serverless has become a preferred way to build applications by developers.
Thanks to the ease of building and deployment that it offers.
Irrespective of what type of an IT professional you are, you would definitely have to interact with some serverless or cloud components in the future.
To help you get started quickly, here are some serverless terms you should know as a developer:

- Cloud Native
- Microservices
- Container
- Kubernetes
- Serverless
- Function As A Service
- Cold Start
- Infrastrcuture As A Code
  
### Cloud Native

I’m sure that you are aware of what cloud computing is.
If you are not, you should read more about [cloud computing](https://glossary.cncf.io/cloud_computing/).
**Cloud Native** is a concept of building and deploying applications in such a way that they take full advantage of the distributed cloud computing offering.

{{< figure src="https://docs.microsoft.com/en-us/dotnet/architecture/cloud-native/media/cloud-native-foundational-pillars.png" alt="Cloud Native. Courtesy: Microsoft." height="400" width="600">}} Cloud Native. Courtesy: microsoft.com

Cloud native applications leverage the services in the cloud to be more resilient, scalable and flexible.
More often than not, such applications are developed without a lot of coding, thanks to the various cloud services.
A serverless developer would often design an application using **microservices**, deploy it on a container and run it on the cloud.

### Microservices

Back in the day, a typical application code used to be one large file with lots of lines of codes.
Developing them wasn’t easy and updating/maintaining them was a Herculean task.
Realizing that problem, we started making our code more and more loosely coupled eventually leading to **microservices**.

Microservice architectural pattern is where a software is composed of **many small independent services** that communicate with each other using APIs.
Each of these microservices can be developed, upgraded and deployed without affecting the other services and have the ability to **independently scale** to meet the peak demands.

{{< figure src="https://cdn.pixabay.com/photo/2018/03/21/16/04/ecommerce-3247176_1280.png" alt="Microservices - small independent services. Courtesy: Pixabay." height="400" width="600">}} Microservices - small independent services. Courtesy: pixabay.com.

The best part that I like is that each of these services can be written in a completely different language using different tools.
So I can have an input screen in React, middleware in .NET, data layer in python and the output using Vue! And that is possible because each of these services is packaged in a container.
We have an interesting article around [single vs monolith](/blog/single-or-monolith-serverless-functions-what-should-you-choose) serverless functions that you should read.

### Container

A **container** is a software package that contains application code, configuration files and all the related libraries along with all the dependencies that are required to run the application.
Just like shipping containers are used to isolate the cargo on a ship, **software containers are used to isolate applications**.

One of the major problems before containers was that an application would run perfectly on one system.
But as soon as it is deployed on another system, it fails due to dependencies, libraries not being present.
Containers get rid of this problem by packaging all the dependencies, libraries along with the source code in a lightweight, immutable container.

{{< figure src="https://freesvg.org/img/AWS-Services-Shelf.png" alt="Containers - isolating applications. Courtesy: freesvg" height="200" width="400">}} Containers - isolating applications. Courtesy: freesvg.org.

The containerized application can be tested and deployed as a container image on any system with a host OS and will guarantee that your application executes.
Some of the popular containerization tools are **Docker**, **AmazonECS**, **Azure Container Service**, **Google Container Engine**.

### Kubernetes

Applications today comprise of hundreds of microservices packaged in hundreds of containers.
As the number of containers increased, the need for a single tool to manage them all became much more important.
And that’s where **Kubernetes** came in.

An orchestration tool originally developed by Google, Kubernetes has become a **de facto container orchestration tool** today.
It is an open source tool that allows you to manage all your containers across multiple clusters by enabling you to deploy, scale & manage containerized applications.
*Don't be consfused if you see K8s, it's just another way of denoting Kubernetes.*

{{< figure src="https://d33wubrfki0l68.cloudfront.net/69e55f968a6f44613384615c6a78b881bfe28bd6/42cd3/_common-resources/images/flower.svg" alt="Kubernetes - container orchestration tool. Courtesy: kubernetes.io" height="400" width="600">}} Kubernetes - container orchestration tool. Courtesy: kubernetes.io

This is one of the most important tools you must know when you’re starting your serverless journey.
If you’re new to Kubernetes, you can check out these free videos on [School of Kubernetes](https://www.infracloud.io/kubernetes-school/).

### Serverless

As applications become increasingly complex, we want developers to focus more on the code rather than the setting up of the environment/infrastructure.
**Serverless** is a cloud execution model that provides an easier and cost-effective way to deploy cloud native applications.

{{< figure src="https://www.infracloud.io/assets/New%20Assets/serverless-consulting/serverless-hero-img.svg" alt="Serverless - cost-effective way to deploy cloud native applications. Courtesy: infracloud.io" height="400" width="600">}} Serverless - cost-effective way to deploy cloud native applications. Courtesy: infracloud.io

Serverless allows for **automatic provision of computing resources** to run applications either on demand or on occurrence of a specific event.
It will also scale the resources automatically in response to an increase or decreased demands.
Hence, as a serverless developer your focus will be on writing the code while the cloud service provider will ensure you have the required resources to run it, when you need it.

### Function As a Service - FaaS

Another important offering around serverless is **FaaS** - *function as a service*.
As the name implies, FaaS is a **cloud computing service that allows you to execute code in response to a trigger event**.
As a serverless developer, you will only deploy the code for a function and the cloud provider will automatically provision the resources required to execute it.
FaaS is a cost-efficient mode to deploy and execute code whilst being flexible and scalable.

{{< figure src="https://spring.io/images/diagram-serverless-standalone-bbe45ff683ff780f3014dfdd18a80909.svg" alt="FaaS - execute code in response to a trigger event. Courtesy: spring.io" height="400" width="600">}} FaaS - execute code in response to a trigger event. Courtesy: spring.io

There are a lot of FaaS service offerings out there namely **Lambda**, **Azure Functions**, **Google Cloud Functions** to name a few.
While these offerings run on their respective clouds, there are services like [**Fission**](https://fission.io) that are open source and allow you to deploy and execute functions on Kubernetes clusters irrespective of where they reside.

### Cold Start

When we talk about function as a service, an important term that you’ll often come across is **cold start**.
Function as a service provides us an easy way to focus on code, and not worry about the provisioning of the underlying infrastructure.

However, every time your function is invoked, there is some time required for the system to gather all the resources for your function to execute.
That setup time is called Cold Start.
To keep the costs down, when your function is idle for a certain amount of time, the cloud provider de-provisions the resources.
If there is any invocation at this point in time, the resources are provisioned again which takes some time, *usually in milliseconds.*

{{< figure src="https://miro.medium.com/max/1362/1*m4FMb3fw05hRl1oxICrRlw.png" alt="Cold Start in case of cloud functions. Courtesy: miro.medium.io" height="200" width="400">}} Cold Start in case of cloud functions. Courtesy: miro.medium.io

In short, **the more the cold start time, the more time it will take for the function to execute**.
So one can pay more and have resources running always to eliminate cold starts.
Or, they can keep the costs down by having slightly higher execution times.
Cold start vs cost is often something that businesses need to decide.

### Infrastructure as Code

Infrastructure until now was provisioned manually by means of shell scripts.
However, with the advent of cloud computing and cloud native design, the demand for accurate, reusable and disposable infrastructure increased.
It also required infrastructure to be scalable and all of this should be repeatable.

{{< figure src="https://thecustomizewindows.com/wp-content/uploads/2021/01/What-is-Infrastructure-as-code-IaC.png" alt="Infrastructure As Code - store infrastructure definitions in files. Courtesy: thecustomizewindows.com" height="400" width="600">}} Infrastructure As Code - store infrastructure definitions in files. Courtesy: thecustomizewindows.com

To ensure the consistency of infrastructure along with easier management, the concept of **Infrastructure as code** came in.
It enables you to **store infrastructure definitions in files**.
These files can then be deployed in existing CI/CD pipelines to always have a consistent infrastructure.

Some of the popular Infrastructure as code tools are **Ansible**, **Terraform**, **Puppet** and **Chef**.

## Conclusion

The world of cloud computing and serverless is a universe in itself that is vast and ever expanding.
The terms mentioned above can be a good starting point for anyone who wants to embark on becoming a serverless developer.
While it may sound Greek and Latin at the moment, you’ll slowly understand them as you start using them.
So if you’ve been waiting to start your cloud native journey, we’ve now made it easier for you.

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)