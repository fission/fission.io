+++
title = "Fission WebSocket Sample"
date = "2021-06-11T10:50:51+05:30"
author = "Gaurav Gahlot"
description = "Write a serverless broadcast function with NodeJS"
categories = ["Tutorials"]
type = "blog"
+++

## Introduction

In this post we will look into how we can develop a simple a web socket based chat application using Fission functions.
Fission's [NodeJS environment][15] now has built in support for [WebSocket][1].
So, we are going to use this environment to power our simple web based chat application.

Let's first understand how this is going to work.

![architecture](/images/fission-websocket-sample.png)

- We start by creating a NodeJS environment using the [fission/nodejs-env][2] Docker image.
- Then we create a fission function for with [broadcast.js][3].
It is this piece of code that will broadcast a message to all connected clients.
- Next, we will create an [HTTP trigger][4] for the above created function.
- We then update our chat application to connect over the route, we just created.
- We will also create a function to host the this chat application.
- As you send a message from one chat window, the function will be triggered and the message will be broadcasted to all connected clients. 

We will cover two approaches using which you can test this setup.

## Prerequisites

You will need a Kubernetes cluster with Fission installed.
Please follow the [instructions here][5] for installing Fission in your Kubernetes cluster.
Then, verify that the fission cli is working by using the `fission version` command.
Please note that the example works with fission version v1.13 and higher. 

## Try it out

In order to try it out, you can either use fission specs provided with the example or manually generate the specs.
We will cover both the approaches in this blog.


### Get router details

- The fission router is exposed as a service.
If you are running a kind cluster, you must get the node internal IP and router service node port.

```
kubectl get nodes -o wide
kubectl get svc -n fission -l application=fission-router
```

- Edit the `web/app.html` and update the connection URL at line `32`.

```
...
conn = new WebSocket("ws://<node-internal-ip>:<router-svc-node-port>/broadcast");
...
```

### Use existing specs

- Clone the [fission/examples][6] repository and navigate to websocket sample code.

```
git clone https://github.com/fission/examples.git
cd examples/miscellaneous/websocket
```

- There you must have the `specs` directory. 
We are going to use these specs and deploy our function.

```
fission spec apply

DeployUID: 1df9464b-5f73-4623-8187-a2f431d5c828
Resources:
 * 2 Functions
 * 2 Environments
 * 2 Packages
 * 2 Http Triggers
 * 0 MessageQueue Triggers
 * 0 Time Triggers
 * 0 Kube Watchers
 * 2 ArchiveUploadSpec
Validation Successful
Spec doesn't belong to Git Tree.
2 environments created: nodejs, python
2 packages created: broadcast-pkg, web-pkg
2 functions created: broadcast, web
2 HTTPTriggers created: broadcast, web
```

Now that we have deployed the function, let's test our chat application.
Open multiple browser windows and go to `http://<router-ip:router-svc-port>/chat/app.html` to access the application.
Send message from either of the window, it will be broadcasted to all others.

### Manually generate specs

- Clone the [fission/examples][6] repository and navigate to websocket sample code.

```
git clone https://github.com/fission/examples.git
cd examples/miscellaneous/websocket
```

- Remove the existing specs directory
```
rmdir specs
```

- Create an initial declarative application specification.
The command will recreate a `specs` directory and a fission deployment config spec file.

```
fission spec init
```

### Spec for broadcast function

- Create fission [environment][7] for the broadcast function.

```
fission env create \
 --name=nodejs \
 --image=fission/node-env:latest \
 --spec
```

- Create spec for the broadcast [function][8].

```
fission fn create \
 --name=broadcast \
 --env=nodejs \
 --rpp=5 \
 --deploy=broadcast.js \
 --spec
```

- Create spec for [HTTP trigger][4].

```
fission httptrigger create \
 --name=broadcast \
 --url=/broadcast \
 --function=broadcast \
 --spec
```

### Spec for web function

- Create fission [environment][7] for the web function.

```
fission env create \
 --name=python \
 --image=fission/python-env:latest \
 --spec
```

- Create fission [package][14] for the web function.

```
fission package create \
 --name=web-pkg \
 --env=python \
 --deploy="web/*" \
 --spec
```

- Create spec for the web [function][8].

```
fission fn create \
 --name=web \
 --env=python \
 --pkg=web-pkg \
 --entrypoint=app.main \
 --spec
```

- Create spec for [HTTP trigger][4].

```
fission httptrigger create \
 --name=web \
 --url='/chat/{html:[a-zA-Z0-9\.\/]+}' \
 --function=web \
 --spec
```

- Now, we can validate and apply the generated declarative application specifications.

```
fission spec apply
```

- In order to test the application, open multiple browser windows and go to `http://<router-ip:router-svc-port>/chat/app.html` to access the application.
Send message from either of the window, it will be broadcasted to all others.

- One important thing to note here is that when the WebSocket is idle for a certain duration, the function pod(s) will be cleaned up.
It means that we are not running the function pod(s) all time, but only when there are requests.
- You can set this timeout while creating a function by setting the `--idletimeout` (in seconds) flag.
The default value is 120.
- You can cleanup and delete all Fission resources in the application specification by executing the command:

```
fission spec destroy
```

Congratulations!
You just deployed your serverless chat application.
If you run into any issues, please feel free to reach out at Fission [slack][13].


**Follow us on Twitter for more updates! [@fissionio][9]**

--- 


**_Author:_**

* [Gaurav Gahlot][10]  **|**  [Fission Contributor][11]  **|**  Software Engineer - [InfraCloud Technologies][12]

[1]: https://datatracker.ietf.org/doc/html/rfc6455
[2]: https://hub.docker.com/r/fission/node-env/tags?page=1&ordering=last_updated
[3]: https://github.com/fission/examples/blob/main/miscellaneous/websocket/broadcast.js
[4]: https://fission.io/docs/usage/triggers/http-trigger/
[5]: https://fission.io/docs/installation/
[6]: https://github.com/fission/examples
[7]: https://fission.io/docs/usage/languages/
[8]: https://fission.io/docs/concepts/#functions
[9]: https://www.twitter.com/fissionio
[10]: https://twitter.com/_gauravgahlot
[11]: https://github.com/gauravgahlot
[12]: http://infracloud.io/
[13]: https://fission.io/slack
[14]: https://fission.io/docs/concepts/#packages
[15]: https://github.com/fission/environments/tree/master/nodejs
