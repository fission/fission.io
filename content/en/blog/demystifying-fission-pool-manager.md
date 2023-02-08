+++
title = "Demystifying Fission - Pool Manager"
date = "2022-02-07T11:30:34+05:30"
author = "Atulpriya Sharma"
description = "Learn how you can use Pool Manager to supercharge your Fission functions."
categories = ["Fission"]
type = "blog"
images = ["images/featured/demystifying-fission-pool-manager.png"]
+++

As the demand for faster shipping increased, the software development process and tools were also streamlined.
With CI/CD developers don’t really have to worry about integrating, building and deploying their code.
With serverless they don’t need to worry about the environment and infrastructure at all.
**Serverless is the present and the future of the software development process.**

## Function as a Service

Serverless today isn’t a buzzword anymore, it’s fairly mainstream to say. From spinning up VMs in the cloud to storing data and executing functions, serverless is a sea today.
**Function as a Service (FaaS)** is one of the key components of the serverless world that is helping developers focus only on their code.
All the cloud service providers have the FaaS offering with different names and similar features.

Fission too is a serverless framework that allows developers to create serverless functions on Kubernetes.
It provides you the freedom and flexibility to use it with any of the existing cloud service providers or your own infrastructure.

**Benefits of Serverless Functions:**

* Faster time to market with increased developer productivity
* Comes with inherent ability to scale
* Low-cost Option as you pay only for the duration your function executes
* Support for different languages

## Challenges of FaaS

Just like everything else in the world has advantages and disadvantages, FaaS too has both. We wouldn’t term it as a disadvantage per se, but it’s just that in certain situations, FaaS isn’t a great option.

Amongst all the other concerns that serverless has, below are a few concerns of FaaS:

* **Added Latency** - there are times when a function just takes a little longer to execute, thanks to the network overheads. Cold Start - first execution of the function - happens when the underlying containers aren’t ready yet. Hence, for time critical functions FaaS might not be a great choice.
* **Resource Limitations** - every cloud service provider has some pre-configured CPU & memory limits. If your function does a lot of heavy lifting then you may notice suboptimal performances if you don’t code your functions well.
* **No local storage** - most of the offerings don’t have any storage option available. Thus, your application needs to be stateless, or you need to plan otherwise.

Of all the challenges of FaaS mentioned above, Fission aims to solve a couple of them - **Latency** and **Runtime configuration**.
Thanks to the way Fission was developed, there are components that help you tweak Fission to make the most out of it.
Do read more about [Fission Architecture](https://fission.io/docs/architecture/) to get a better understanding of Fission.

{{< figure src="/images/featured/demystifying-fission-pool-manager.png" alt="Demystifying Fission - Pool Manager" height="600" width="1000">}}

## Fission Executor and its types

The component that we are going to focus on today is **Executor**.
In simple terms the executor spins up the pods for your functions.
When you execute fission fn test –name hello, underneath, the router will reach out to the executor to check if there are any pods already up and running.
If there is, the executor will return the address of the pod, if it is not, it will use one of the three executor types to spin up a pod.
Each of these executor types have different strategies to launch and manage pods.

* **Pool Manager**- It keeps a constant check on environment CRD changes and proactively creates **generic pools** for environments. When a request comes in, the Pool Manager with the help of fetcher loads the function in one of these pods. For every subsequent request, the function will be executed on this specialized function pod. This is great for short-lived functions & for those that require shorter cold start time.
  
* **New Deploy** - New Deploy on the other hand creates a Kubernetes Deployment along with a **Service** and **Horizontal Pod Autoscaler (HPA)**. This makes it suitable for functions that handle massive traffic. It enables auto-scaling and load balancing of requests between the pods. NewDeploy scales the replicas of a function deployment to the minimum when there are no requests. When there’s a spike, HPA will scale the number of pods to handle the traffic. Though this increases the cold start time, it’s great for functions that need to cater to massive traffic.
  
* **Container Functions** - the newest form of executor that Fission offers is Container functions. This is an alpha feature at the moment that allows you to run containers and functions.

## Everyone’s favorite - Pool Manager

The ability of the pool manager to always keep a **‘warm’** pool of environment and generic containers is its biggest advantage.
It’s because of this F**ission guarantees very low cold start latencies of typically around ~100ms.**
Furthermore, the ability to fine tune the containers with required resources limits makes it a preferred choice.

In fact there are companies that are using Fission with Pool manager as the executor.
They run several hundreds of functions in a single environment.
Most of these functions are time critical and hence the warm pool helps them achieve lower latencies.

```bash

# The default executor type for function is poolmgr
$ fission fn create --name foobar --concurrency=4 --env nodejs --code hello.js

# Or, set executor type to poolmgr explicitly
$ fission fn create --name foobar --env nodejs --code hello.js --executortype poolmgr

```

**Pool Manager Benefits:**

* Maintains a warm pool of pods always
* Low cold start times
* Allows optimization and fine-tuning of containers

## Pool Manager Features

In the earlier versions of Fission, Pool Manager wasn’t quite flexible.
For instance, it allowed a function to be executed only on one pod. That led to issues concerning concurrency.
What if a developer wanted to ensure that the function could process multiple requests at the same time?
That’s when Fission was groomed and more features were added to help you take control of Fission execution with the Pool manager.

Today, Fission provides you with options with which you can limit the resource usage for the pods.
It provides you with multiple ways to fine tune your environment and execution to take the most out of it.

### PoolSize

By default, Fission currently creates a generic pool with 3 pods `-poolsize = 3`.
You can control the default pool size based on your needs. You can do so by setting the flag –version to 3.

For instance, the below code snippet with create a new Python environment with a poolsize of 1.

```bash
$ fission env create --name python --version **3** --poolsize **1** --image fission/python-env:latest
$ kubectl get pod -l environmentName**=**test
```

To give you greater control over resource usages for all functions in the same environment, you can also set CPU and memory flags.

The below snippet limits the min/max cpu to 100 m/200 m, and min/max memory to 128Mi/256Mi respectively. *(The CPU limit is in miliCPU)*

```bash
$ fission env create --name python --version **3** --poolsize **1** --image fission/python-env \
    --mincpu **100** --maxcpu **200** --minmemory **128** --maxmemory **256**
```

#### Requests Per Pod

There might be situations where you want to limit your pod to service only a certain number of requests.
For that you can use the `-rpp` flag.
The number that you pass here will be the maximum number of requests that a pod will serve.
Anything beyond that, a new pod will be created to handle those requests.

```bash
$ fission fn create --name foobar --env nodejs --code hello.js --rpp 5
```

#### OnceOnly

If you have a function that does some intensive tasks and requires more time to execute, you can configure the pod to serve only one request at a time for any such function.
For that you can use the flag `–yolo`.
If it’s set to true, the pod will execute the function only once.

```bash
$ fission fn create --name foobar --env nodejs --code hello.js --yolo true
```

#### Concurrency

In case there’s a function that will be called multiple times, and you want to ensure that all the requests are served simultaneously, you can use the `-con` flag.
The number that you pass here will be the maximum number of requests a pod will process at a given time.

```bash
$ fission fn create --name foobar --env nodejs --code hello.js --con 1000
```

## Pool Manager Use Cases

We’ve now gone through the various features of Pool Manager that you can use to gain more control over the function execution.
The default values are fine for PoC development, however when you move to production, you want to have optimized usage of the resources.
So when exactly to use these flags? Here are a few use cases that we’ve come across:

* You have an application that allows users to securely login to various services. Inside, you have a function that is called to handle the security tokens received from other services. In such situations you may want to limit the execution to **only once** per pod for obvious security reasons.
* In situations when you have functions that are cpu and memory intensive, there are chances that they may request for more resources and get killed with Out of Memory error. To avoid such situations, specify the **CPU and memory limits**.
* You have a specific function that collects and processes data from IoT devices. You’d want to limit the specialized function pod to handle only a **certain number of requests.**  
* If you have a voting application that allows users to vote for a particular poll, you’d want the pod to serve multiple requests simultaneously. In such cases you can define how many **concurrent** requests a pod can serve.

## Final Thoughts

The reason why the cold start times for Fission functions is typically ~100 m is because of how it is designed.
We looked into the details of Pool Manager and its features.
It allows you to fine tune your resources for an environment that is extremely critical for production scenarios.
From controlling the pool size to limiting the resources and controlling function execution, Fission gives you great control and flexibility apart from being fast and vendor-agnostic.

If you have any questions regarding Pool Manager or are confused what’s the best configuration for your setup, feel free to reach out to us.
Join [Fission Slack](https://fission.io/slack) channel or [Tweet to Us](https://twitter.com/fissionio) and we should be more than happy to help!

**Demystifying Fission** is our series of blog posts on topics that'll help you understand Fission better.
Do check out our other posts in the Demystifying Fission series:

- [Understanding New Deploy](/blog/demystifying-fission-new-deploy)
- [Understanding HTTP Requests in Fission](/blog/demystifying-fission-http-requests-in-fission)

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)
