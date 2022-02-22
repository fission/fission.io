+++
title = "New in Fission: Live-Reload, Canary Deployments, Prometheus integration "
date = "2018-10-16T01:05:00-07:00"
author = "Fission"
description = "Live-Reload, Canary Deployments, Prometheus integration in Fission"
categories = ["Fission"]
type = "blog"
+++


Today we're really excited to launch a set of new features for
[Fission](http://fission.io), our open source Kubernetes-native
serverless framework.  These features are all designed to help you
improve the quality and reliability of your serverless applications on
Kubernetes.

Serverless architectures have obvious productivity advantages.  You
can get your apps up and running quickly, reducing the total lead time
to ship your new application.  However, to make this "production
ready", serverless architecture needs to be not just about moving
fast, but also about moving fast _safely_, and at scale.  That means
we need features focused on code quality, testing, better deployment
and release practices.

Fission is the first open source serverless framework to offer
live-reload, record-replay, and automated canary deployments.  We're
making serverless functions on Kubernetes more mature, and ready for
production use.

## Live-reload: Test as you type

With Live-reload, Fission automatically deploys the code as it is
written into a live Kubernetes test cluster, and allows developers to
toggle between their development environment and the runtime of the
function, to rapidly iterate through their coding and testing cycles.

<iframe width="560" height="315"
src="https://www.youtube.com/embed/3CbSmt1zLto?rel=0" frameborder="0"
allow="autoplay; encrypted-media" allowfullscreen></iframe>

This allows bugs to be found and fixed earlier in the application
development lifecycle, when it is cheaper to do so – before they are
discovered in the higher environments or cause any service disruption
in Production. Further, it simplifies and increases the fidelity of
integration tests, by running them earlier in the process using a live
environment that’s consistent with the configuration and related
services (i.e. database, API calls, etc.) that are used in Production.

![Live-Reload](/images/record-replay.jpg)

[Check out this blog post to learn how to use live-reload in
Fission.](/blog/live-reload-in-fission-instant-feedback-on-your-serverless-functions/)

## Record-replay: Simplify testing and debugging

Fission is the first serverless solution to offer Record-replay for
functions.  This feature allows you to record function invocations
into a database, examine these recordings, and replay them on-demand
for testing and troubleshooting.

You can configure which functions and workflows to record and for how
long to retain the recorded events.

Record-replay is useful for developers to reproduce complex failures
during testing or debugging.  It can also make regression testing
easier.  In addition, operations teams can enable recording on a
subset of live production traffic -- this can help developers
reproduce failures, and test application updates.

![Record-replay](/images/record-replay.jpg)

## Automated Canary Deployments: Reduce the risk of failed releases

Canary deployments are a proven deployment strategy to minimize the
risk in deploying new releases.

In this strategy, a new version is initially released only to a small
fraction of users.  If this version works well, it's released to more
and more users; if it doesn't work, those users are shifted back to
the stable version, and only that small set of users was affected by
the unstable new version.

Fission is the first open source serverless framework to provide fully
automated Canary Deployments.  This means that Fission helps with not
just the traffic-splitting portion of Canary Deployments, but also the
feedback loop of checking for success and slowly rolling forward or
rolling back.

Fission automatically increments traffic proportions to the newer
version of a function as long as it succeeds, and rolls back to the
old version if the new version fails.  You can configure the initial
percentage of traffic for the new version of the function, the the
release rate at which to roll out the new version, and the error rate
that will trigger a roll back.

![Automated Canary Deployments](/images/prometheus-canary-screenshot.png)

[See this post for details on how to use Automated Canary Deployments
in Fission](/blog/automated-canary-deployments-in-fission/)

## Prometheus Integration: Easy metrics collection and alerts

Fission exposes Prometheus metrics for all your functions, so you
don’t have to build Prometheus integration into any of your code.  You
get metrics simply by deploying functions into Fission.

Fission's Prometheus integration gives you metrics for function
invocation rate, function duration, and error rate.  These metrics can
also be used to set up alerts with Prometheus' AlertManager service.

Prometheus has a powerful query language that you can use to produce
graphs. Additionally, Prometheus metrics can also feed Grafana to
create dashboards.

![Prometheus screenshot](/images/prometheus-screenshot-generic.png)

## Cost Optimizations in Fission

Since Fission is open source and works on any Kubernetes cluster, it
enables you to run on any infrastructure -– this means you can use
cheaper VM instance types on public clouds (such as spot instances on
AWS or preemptible instances on GCP).

And if you're in a company with investments in datacenters, you can
continue taking advantage of those datacenters.  Fission scales
resource usage up and down with demand, allowing you to maximize
infrastructure utilization (in both public cloud and on-premises
datacenter cases).

Fission functions can be configured with specific CPU and memory
resource usage limits, minimum/maximum number of instances and
auto-scaling parameters.

These parameters allow for functions to be tuned with an execution
strategy that best fits the specific business use case -- you can
optimize for cost, for performance, or for something in between.

For example, functions that have severe cost constraints can be
deployed into containers on-demand, minimizing costs at the expense of
performance.  Conversely, functions that need performance above all
other requirements can be configured to have instances always running,
ensuring low latency but driving up costs.  Functions can also take
advantage of Fission’s pre-warmed container pools, which aggregate the
cost of pooling over a large number of functions, while providing
performance benefits for all of them.

[See the docs for more about controlling Function execution in
Fission](/docs/architecture/executor/)

## Enterprises love Fission

<img src="/images/snapfish-logo.png" alt="Snapfish logo" width="300px" style="width:300px; float:left; margin-right: 3rem;">

Headquartered in San Francisco, CA., Snapfish is the leader in online
photo printing services. Founded in 1999, it provides high-quality
photo products to consumers looking for great value and selection. The
company operates in multiple countries around the world and supports
blue-chip companies’ photo efforts.

Using Fission, Snapfish is able to simplify their development
experience, modernizing their applications to take advantage of
Serverless while leveraging their existing datacenter investments.

“Our global photo platform helps hundreds of millions of devoted users
preserve their memories by combining all of their favorite photos on
thousands of customized products. We are always looking for ways to
improve the way we manage the scale and quality of our
applications. These new Fission features will help our developers
deliver new customer experiences built on serverless applications
without the dependency of managing the complexity of scale”, said
Kenneth Lam, Director of Technology at Snapfish. “Fission allows our
company to benefit from the speed, cost savings and scalability of a
cloud-native development pattern on any environment we choose, whether
it be the public cloud or on-prem.”

## See a quick demo of all the new features in Fission

<iframe width="560" height="315"
src="https://www.youtube.com/embed/3GGbd2RMPLM?rel=0&amp;start=2363"
frameborder="0" allow="autoplay; encrypted-media"
allowfullscreen></iframe>

## Try Fission out!

[Learn more](https://fission.io) about Fission, or come chat with us on
[our Slack](/slack).

If you're ready to try it out head over to the docs for instructions
on [how to install Fission](/docs/installation).
