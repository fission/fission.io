+++
title = "Live-Reload in Fission: Instant feedback on your Serverless Functions"
date = "2018-10-16T01:04:00-07:00"
author = "Ta-Ching Chen"
description = "Live reloading of functions for faster feedback"
categories = ["Fission"]
type = "blog"
+++


Accelerating feedback loops are an important devops
principle: the sooner you find a bug, the cheaper it is
to fix it.

While developing your application, you’re typically
going through a cycle: write code, build, deploy into a
test environment, run tests, fix, repeat. The build and
deploy stages of this cycle are idle, unproductive time
where you’re simply waiting. As a project grows, these
stages get slower and slower. Once they’re slow enough,
you end up context switching to another task, while
waiting, and that makes it harder to get back into the
right context and fix any bugs you find in testing.

Fission comes built-in with live-reload, a feature that
drops the time from code to running tests to a few
seconds.  Fission is the first open source serverless
function framework to do this.



## Using live-reload in Fission

The `fission` CLI supports [declarative
specifications](/docs/usage/spec/)
for Fission resources -- such as functions,
environments, triggers, etc.  These resources are specified as a set of YAML files that are stored in the specs directory at the root of your Fission application. You don’t have to write these YAML files from scratch - Fission automatically generates the initial versions for you.  And because configuration is declarative, you don’t have to write any imperative deployment scripts for configuration management.

As part of Declarative specifications, you can also configure Packaging – how source code is bundled up and uploaded to the cluster. Fission then uses that to consistently deploy your code on any environment - from Dev, to Test, through to Production.

The deployment of all resources in the specifications is triggered by the fission spec apply command. With this command, the fission CLI checks the state of the cluster against the desired state as configured in the specs.


**To use live-reload, simply add the --watch option:**

```sh
$ fission spec apply --watch
```

And then, edit your code in your editor as usual. 

Whenever you save a file, the fission CLI notices a
change on the filesystem, and automatically packages up
the code and uploads it.

On the cluster, if this is a compiled language, the
source is compiled. Then the function deployment is
automatically updated. Within a few seconds, the new
function is ready to be tested.

Since Fission automatically deploys into a test cluster
as you code, you get faster feedback, enabling you to
rapidly iterate through your coding and testing cycles.
 
This allows bugs to be found and fixed earlier in the
development lifecycle. It also increases the fidelity
of your tests, since you can run them in a real
cluster, along with whatever other services your code
depends on.

Here's a quick demo video of live-reload in action:

<iframe width="560" height="315" src="https://www.youtube.com/embed/3CbSmt1zLto?rel=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

## Behind the scenes -- how it works

picture:

[editor] -> `fission spec apply --watch` -> [fission storagesvc] -> [builder] -> [back to storage] -> [runtime pod]

## Conclusion

Live reload in Fission gives you a smooth, fast
development experience.  It accelerates feedback loops
-- allowing you to test your code as you type.

Check out the [Fission installation guide](/docs/installation/) to get started with
Fission.  Join us on the [Fission Slack](/slack) to chat, or follow us on Twitter at @fissionio.
