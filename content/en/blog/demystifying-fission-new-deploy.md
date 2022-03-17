+++
title = "Demystifying Fission - New Deploy"
date = "2022-02-10T11:30:34+05:30"
author = "Atulpriya Sharma"
description = "Understand how New Deploy executor works in Fission."
categories = ["Fission"]
type = "blog"
images = ["images/featured/demystifying-fission-new-deploy-featured.png"]
+++

Times change and technologies evolve.
The serverless architecture has been around for quite some time now as an option to deploy applications to the cloud.
Most of the mainstream cloud providers launched their Function as a Service offerings about a decade ago.

*Fun Fact: Did you know that Amazon’s Alexa Skills are entirely running on AWS Lambda functions? All of [Alexa’s skills are hosted on Lambda functions](https://developer.amazon.com/en-US/docs/alexa/ask-overviews/what-is-the-alexa-skills-kit.html) which are perfect for the use case.*
They need functions to load quickly and don’t need to store any state.

Alexa is just one use case, there are many more such use cases that are perfect candidates for FaaS.
Fission is another serverless framework made for Kubernetes.
It can help you achieve all of these with low cold start times,greater control and without locking you with a particular vendor.
You can carry Fission with you wherever you go - *across vendors and on premise as well*.

## Pool Manager Recap

In our [previous blog post](/blog/demystifying-fission-pool-manager/), we talked about Pool Manager and how it helps you execute Fission functions.
Pool Manager is currently the **default executor in Fission** and also one of the most widely used one.
From maintaining a warm pool, it ensures that you experience lower cold start times without compromising on the performance.

It was also quite flexible in terms of providing you with options to tweak resource limits at the environment level.
From allowing you to define the pool size to deciding on the number of requests per pod, Pool Manager is perfect for a lot of scenarios.

Since you always have a pool of pods in the warm state, you are consuming resources.
And that adds up to your bill.
So if you're wanting to optimize your costs, pool manager might not be a great idea.

Also, pool manager allowed you to configure limits only at the environment level, you couldn’t modify anything on the pods.

{{< figure src="/images/featured/demystifying-fission-new-deploy-featured.png" alt="Understand how New Deploy executor works in Fission." height="600" width="800">}}

## New Deployment - Scale your functions at ease

New Deployment or NewDeploy is the new executor that gives you greater control over your functions along with inherent scaling capabilities.
NewDeploy creates a **Kuberentes deployment** along with a service and **Horizontal Pod Autoscaler**.

To create a function using NewDeploy simply mention it in the `-- executortype` flag as shown below:

```bash
$ fission fn create --name foobar --env nodejs --code hello.js --executortype newdeploy
```

### Features of New Deployment

#### Granular control over functions

NewDeploy also provides auto-scaling and resource limit settings to be configured for individual functions.
Unliked Pool Manager that allowed you to configure settings at an environment level only.
With this capability, each of your functions can specify the resource limits which can be different from different functions based on their use cases.
Another thing to note is that, whatever limits you specify for the function will override the values specified at the environment level.

For instance, you can provide limits to min/max scale, min/max CPU, min/max memory as mentioned below. Do keep in mind that you are creating a function and not an environment unlike Pool Manager

```bash
$ fission fn create --name foobar --env nodejs --code hello.js --executortype newdeploy \
    --minscale 1 --maxscale 3 --mincpu 100 --maxcpu 200 --minmemory 128 --maxmemory 256
```

##### Eliminating Cold Start

If you observe the above code snippet closely, you’ll see that `--minscale is 1`.
That means you’ll always have a pod in place. However, if you change it to 0, your function will experience long cold start times as it takes time for the executor to create the deployment.

```bash
$ fission fn create --name hello --env node --code hello.js --minscale 1 --executortype newdeploy
```

#### Autoscaling

Horizontal Pod Autoscaler is Kubernetes’s way of implementing scaling.
It does so by deploying more pods based on the increased demand. Read more about [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
With HPA, NewDeploy not only enables your functions to scale but also takes care of the load balancing during traffic spikes.
So if you have a function that a user can connect to get the latest new updates, you know there will be massive traffic spikes which will be handled well if NewDeploy is used.  

```bash
$ fission fn create --name hello --env node --code hello.js --executortype newdeploy \
    --minmemory 64 --maxmemory 128 --minscale 1 --maxscale 6 --targetcpu 50

function 'hello' created
```

To see it in action, create a new function called hello and set the target CPU to 50.
When you execute this function and observe the HPA, you’ll see pods being created as the load increases and then gradually slows down.

## Pool Manager or New Deploy?

Having discussed Pool Manager in the previous blog post and New Deployment in this, we assume that you have a fairly good idea of both of these.
While we listed out the use cases for each, you might still have a question: **Pool Manager or New Deploy - which one to choose?**

Both Pool Manager and New Deployment offer you different ways to execute your functions.
The answer pretty much boils down to two things: **Idle Cost vs Latency**
Based on what is more important to you, you can choose to go either with Pool Manager or New Deploy.

With Pool Manager you are guaranteed with low latency due to warm pools of pods.
So if your requirement is low latency, but you’re fine paying for the idle pods, Pool Manager should be your choice.

On the other hand, if you want your functions to scale dynamically to respond to spikes in traffic with a low idle cost but can do with the higher latency, NewDeploy should be your choice. With New Deploy, you can also choose to keep the latency low in this case by setting the `-- minscale > 0`, however that will increase your idle cost.

Hence, depending on your use case, you can choose the option that’s best suited to you. Below is a table for easy reference:

| Executor Type | Min Scale | Latency | Idle Cost                                      |
|---------------|-----------|---------|------------------------------------------------|
| New Deploy    | 0         | High    | Very low, pods get cleaned up after idle time  |
| New Deploy    | > 0       | Low     | Medium, min scale number of pods are always up |
| Pool Manager  | 0         | Low     | Low, pool of pods are always up                |

## Final Thoughts

NewDeploy as the name suggests is a newer way that Fission has adopted to execute functions. This approach not only allows you to set resource limits at a function level, but with the addition of Horizontal Pod Autoscaler, it also takes care of spikes in traffic and load balancing. If idle cost isn’t a concern for you, you can even have a minimum number of pods active to give you the low latency without compromising the scalability.

Now that you have learnt about Pool MAnager and New Deploy, why not try them? Head over to our examples repo and try out the various samples that we have created. Change the executors and see how it works.

If you have a specific requirement and are confused which one to use, please share it in our [Fission Slack](https://fission.io/slack) Channel or get in touch with us on [Twitter](https://twitter.com/fissionio) and we’d be happy to help.

**Demystifying Fission** is our series of blog posts on topics that'll help you understand Fission better.
Do check out our other posts in the Demystifying Fission series:

- [Understanding Pool Manager](/blog/demystifying-fission-pool-manager)
- [Understanding HTTP Requests in Fission](/blog/demystifying-fission-http-requests-in-fission)

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)
