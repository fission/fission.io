+++
title = "Automated Canary Deployments in Fission"
date = "2018-10-16T01:02:00Z"
author = "Soam Vasani"
description = "Canary deployments for serverless functions in Fission"
categories = ["Tutorials"]
type = "blog"
+++

Canary Deployments are a time-tested deployment strategy to reduce
risk. The fundamental idea is that deploying software into a
production cluster is different from releasing it to its users. With
canary deployments, you deploy both old and new versions into a
production environment, but send only a small percentage of traffic to
the newer version. That way, if the new version fails, only a few
users are affected rather than the application’s entire user base. If
the newer version works well, the traffic proportion being sent to it
is increased incrementally until the new version has been rolled out
to all live traffic.

With _Automated Canary Deployments_, the feedback loop is automated --
success causes the new version's proportion of traffic to be
increased, and failure causes the new version's traffic proportion to
be rolled back to zero.  This saves ops teams from having to either
manually manage canary deployments, or build automation to do so
themselves.

Fission is the first open source serverless function framework to have
built-in, easy-to-configure Automated Canary Deployments.

Users can configure the percentage of traffic that will receive the
new version of the function, the error rate that will constitute as
failure, and the release rate at which to roll out the new version.

Let’s go over a quick tutorial on using Automated Canary Deployments
in Fission.

## Using Automated Canary Deployments in Fission

Automated Canaries are supported from Fission version 0.11.  For the
next section we'll assume you're already set up with this version; if
not, checkout the [install guide](/docs/installation/).

For this tutorial, we'll start with two versions of a function
deployed on a cluster, and show how automated canary deployments
incrementally transfer load from one version to another.

First, download a couple of trivial sample functions:

```sh
$ curl -LO https://raw.githubusercontent.com/fission/fission/master/demos/canary-successful-scenario/func-v1.js
$ curl -LO https://raw.githubusercontent.com/fission/fission/master/demos/canary-successful-scenario/func-v2.js
```

Next, create the environment and functions on your Fission cluster:

```sh
$ fission env create --name nodejs --image fission/node-env

$ fission fn create --name func-v1 --env nodejs --code func-v1.js

$ fission fn create --name func-v2 --env nodejs --code func-v2.js
```

Next, create a route with two weighted functions.  This route is set
up to send 100% of load to `func-v1`, and none to `func-v2`.  Still,
it's important that it's set up for two function versions.

```sh
$ fission route create --name route-canary \
       --method GET --url /canary          \
       --function func-v1 --weight 100     \
       --function func-v2 --weight 0 
```

Fission's canary automation can roll out the newer version by changing
these weights over time.  Let's create a canary configuration
resource, which configures the parameters of how exactly the automated
rollout will occur, and when it will rollback if necessary.

```sh
fission canary-config create --name canary-1        \
       --funcN func-v2 --funcN-1 func-v1            \
       --httptrigger route-canary                   \
       --increment-step 10 --increment-interval 30s \
       --failure-threshold 10
```

First, the configuration needs to know the old and new versions.
Next, it needs to know which HTTP route to canary.  The next two
parameters, step and interval, specify how much the traffic shifts and
how often; in other words it's the rate of progress for the canary.
Finally, the user specifies the maximum permissible percentage of
failures; failures beyond this percentage cause a roll back.

The rest is automatic.  In this example we've set the roll out rate to
be pretty fast.  In reality you'd probably want have it much slower,
so you have more real-world testing on the new version before
incrementing it to significant percentages.

With Prometheus, you can view the traffic to the old function drop as
the traffic to the new version rises:

![prometheus graph screenshot](/images/prometheus-canary-screenshot.png)

## An overview of how Automated Canary Deployments work

The user deploys two functions into Fission, and configures a trigger
to split traffic between them.  The Fission router uses this traffic
split configuration to send an appropriate fraction of traffic to each
version of the function.  A common traffic split would be something
like 90% to the old stable version and 10% to the new version.

Fission's Prometheus integration means that the Fission Router reports
error rate metrics for all functions.  Prometheus scrames these
metrics and stores them.

The CanaryController ties everything together.  At each interval, it
samples the error rate metrics from Prometheus, and makes a decision
whether to roll forward or roll back.  If it decides to roll forward,
it modifies the traffic split fraction in the Trigger specification to
increase the traffic to the new version, and the process repeats at
the next interval.  If at any point a failure threshold is reached,
the controller immediately sets the new version's traffic fraction to
zero, and declares the canary status to have failed.

![canary working](/images/canary-deployments.jpg)

## Conclusion

Automated Canary Deployments in Fission give you the ability to move
changes into production with lower risk and increased confidence.

Check out the [Fission installation guide](/docs/installation/) to get started with
Fission.  Join us on the [Fission Slack](/slack) to
chat, or follow us on Twitter at @fissionio.
