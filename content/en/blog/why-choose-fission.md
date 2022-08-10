+++
title = "4 Reasons to Choose Fission Kubernetes Serverless Framework"
date = "2022-03-23T08:30:34+05:30"
author = "Atulpriya Sharma"
description = "Fission is one of the popular open source Kubernetes serverless framework. In this post we help you understand why should you choose Fission."
categories = ["Fission"]
type = "blog"
images = ["images/featured/why-fission-serverless-framework.png"]
+++

The Serverless paradigm is empowering developers to focus only on building the application and not worry about anything else.
Kubernetes has become an industry standard for hosting cloud native or container based microservice applications.
It works seamlessly across public/private clouds and provides a common platform without any vendor lock-in.
Hence, it makes naturally a good choice to build serverless frameworks on top of Kubernetes.

There are a handful of Kubernetes serverless frameworks out there and Fission is one of the popular ones.

## What is Fission

Fission is the Kubernetes serverless framework that helps you build serverless applications.
It allows you to **write and deploy functions almost instantly**.
You don't need to create any containers or deal with Docker registry.
With just a few commands your application will be live.
You can host your applications on your laptop, public cloud or in your private data center as it runs on Kubernetes.
If you're wondering why to choose Fission Kubernetes serverless framework, read on and let us tell you why.

{{< figure src="/images/featured/why-fission-serverless-framework.png" alt="Reasons to choose Fission Kuberenetes Serverless Framework" height="600" width="800">}} Why Choose Fission Kuberenetes Serverless Framework


## Why Choose Fission?

### Customizable Environments

Fission provides unmatched extensibility.
The core of Fission is written in **Go**, it has [Environments](/docs/concepts/#environments) which are the language-specific parts.
An environment in Fission contains only the adequate code that is required to run a function.
Fission currently supports **NodeJS, Python, Go, Java, Ruby, PHP**, and **.NET**.
You can check out all the [Fission supported environments](/environments/).

{{< figure src="https://fission.io/docs/concepts/assets/trigger-function-environment.png" alt="Environment in Fission" height="500" width="500">}} Functions execute inside an environment.

The key of Fission resides in customizable environments.
As a developer, you can **modify any of Fission's supported environments** and rebuild them.
Not only that, you can even create a new environment from scratch.
We have a blog post about using [PostgreSQL with Fission](../how-to-use-postgresql-database-with-fission-functions/) where we show how to modify an environment.
Even the components in Fission are stored as Kubernetes Custom Resource Definitions(CRDs) and are customizable.

Due to customizability of environments, there are many organizations that prefer using Fission.
Many have of them have build Function as a service(FaaS) platform on top of Fission for enterprise hosting.

### Greater Control Over Your Infrastructure

While Fission takes care of the underlying infrastructure, it also offers you a lot of customization options and better control through abstractions.
From configuring memory limits to CPU utilization, you can configure these settings at the lowest pod/container level.
Fission Executors like [Pool Manager](../demystifying-fission-pool-manager) & [New Deploy](../demystifying-fission-new-deploy) allow you to fine tune the function execution by configuring settings at the environment and pod level.

```bash
# Fission code snippet with custom configuration
$ fission fn create --name foobar --env nodejs --code hello.js --executortype newdeploy \
    --minscale 1 --maxscale 3 --mincpu 100 --maxcpu 200 --minmemory 128 --maxmemory 256
```

For instance, you can configure a pod to execute only one function at a time.
You can also create and maintain a pool of warm pods to reduce the cold start times for functions.
Thanks to Fission's ability to integrate with observability tools like [OpenTelemetry & Datadog](../observability-with-opentelemetry-datadog-in-fission/), you know what's exactly happening in your infrastructure.
Based on the observability, you can fine tune your applications and infrastructure to take the maximum advantage.

### Vendor agnostic

Most of the cloud service providers today provide managed Kubernetes offering.
In just a few clicks, you can create a Kubernetes cluster and start deploying workloads.
While it all is easy, you are pretty much locked in with a vendor.

{{< figure src="https://d33wubrfki0l68.cloudfront.net/964dac0d5d27fec1d6b6d1a723842f4d14c1ead3/78fef/images/fission-illustration.svg" alt="Fission Serverless Framework" height="500" width="500">}} Fission is built on Kubernetes

When you use an AWS lambda serverless function, it is tightly coupled with the entire AWS ecosystem.
Hence, if you want to move such a serverless function to another cloud provider like Azure or GCP, it isn’t going to be easy as you would have to create and configure a lot of things from scratch in the new environment.

On the other hand, **Fission is built on top of Kubernetes** and hence migrating applications across different clouds is much easier.
Disaster recovery also is relatively easier to set up and deploy in Fission due to [Fission spec files](/docs/usage/spec/).

### Community Support

**Did we tell you Fission completely is Open Source?**
It's one of the few Kubernetes serverless frameworks that is **open source**.
The biggest asset of Open Source is community.
Fission has a thriving community behind it that is helping steer the course of Fission.
We have an active [Slack community](https://fissionio.slack.com/) where developers from across the globe contribute to Fission.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">We have more than 1500 enthusiasts in our community who are not only using Fission but also helping us improve it.<br><br>If you are an <a href="https://twitter.com/hashtag/OpenSource?src=hash&amp;ref_src=twsrc%5Etfw">#OpenSource</a> enthusiast interested in <a href="https://twitter.com/hashtag/Kubernetes?src=hash&amp;ref_src=twsrc%5Etfw">#Kubernetes</a> &amp; everything <a href="https://twitter.com/hashtag/Serverless?src=hash&amp;ref_src=twsrc%5Etfw">#Serverless</a>, join us &amp; learn how you can contribute 👇🏽<a href="https://t.co/cdkwzywVVA">https://t.co/cdkwzywVVA</a></p>&mdash; fissionio (@fissionio) <a href="https://twitter.com/fissionio/status/1483764282953465857?ref_src=twsrc%5Etfw">January 19, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

While we strive hard to have the documentations in place, if there's anything missing, our active community is there to help you out.
From the most basic of issues to the most complex ones, there's a pretty good **community support that comes Free with Fission** ;)

With a suite of benefits that come along with Fission, don't you think it's time to give Fission a try?
Fission is powering applications of enterprises across the globe, so it is production ready.
With the dedicated support from the maintainers and the active community, you can trust Fission to take care of your enterprise requirements.

Read more about [Fission](/docs/) or get in touch with us so that we can help you get started.

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)
