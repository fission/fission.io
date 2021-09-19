+++
title = "How to Develop a Serverless Application with Fission (Part 1)"
date = "2018-09-06T15:48:12+08:00"
author = "Ta-Ching Chen"
description = "Write serverless Java functions with JVM"
categories = ["Fission", "application"]
type = "post"
+++

# Introduction

When users try to develop serverless applications, they often choose
to start with Serverless services offered on public clouds, like [AWS
Lambda](https://aws.amazon.com/lambda/) or [Google Cloud
Functions](https://cloud.google.com/functions/). However, users may
encounter following problems after application development:

1. Simulating the same environment on local machines is difficult
2. Vendor lock-in prevents moving applications from one cloud provider to another
3. Sensitive data that should not be sent outside an on-premises datacenter

[Fission](https://fission.io/) is a serverless framework built on top of [Kubernetes](https://kubernetes.io/). Here are some benefits for adopting Fission as serverless solution to develop a severless application:

* `Portability`
    * Laptop, PC, On-premises datacenter, even cloud providers. Wherever you can run Kubernetes, you can run Fission.
    * Recreate a serverless application in short time with fission `spec` files.
* `Support rich event sources`
    * HTTP Trigger
    * Message queue trigger: NATS, Kafka
    * Time trigger
* `Rich Environment (Language) supportability`
    * NodeJs, Go, Python, Java (JVM languages), Ruby, Perl, PHP7, DotNet, DotNet2, Binary
    * BYOE (Build Your Own Environment)
* `Build automation`
    * Builder manager inside Fission helps to create a deployable function package from source code.

After seeing these advantages for adopting Fission as serverless framework, you may feel exciting and start wondering how to create a serverless applciation with Fission. Let's dive into the concepts of fission first.

# Installation

You can install kubernetes and fission by following install guides.

* [Kubernetes installation guide](https://docs.fission.io/docs/installation/#kubernetes-cluster)
* [Fission installation guide](https://docs.fission.io/docs/installation/#install-fission)

# Basic Fission Concepts

![Trigger, Function, Environment](/images/how-to-develop-a-serverless-application-with-fission/trigger-function-environment.svg)

There are three basic concepts of fission:

## Function: 

A snippet of code write in specific programming language and will be invoked when requests come to fission router.

Following is a simple nodejs helloworld sample

```js
module.exports = async function(context) {
    return {
        status: 200,
        body: "Hello, world!\n"
    };
}
```

Currently, fission support multiple popular language like NodeJs, Go, Python, Java...etc. For more examples in different languages, please visit [fission language examples](https://github.com/fission/fission/tree/master/examples).

## Environment

The environment(language) container which runs user function to serve HTTP requests. When a request hit fission router, the env container will load user function into runtime container first, then execute the function to serve the request. 

## Trigger

A fission object maps incoming requests to the backend functions. When a trigger receives requests/events, 
it will invoke the target function defined in trigger object by sending a HTTP request to function pod. 

Currently, fission supports following types of trigger:

* `HTTP Trigger`
    * The trigger first registers a specific url path to router and proxy all requests hit the url to user function.
* `Time trigger` 
    * A function will be invoked based on the schedule of `cron` spec.
* `Message Queue Trigger`
    * The trigger will subscribe and handle any messages sent to the message queue topic. Then, publish function response/error to the predefined response/error topic.
* `Kubernetes Watch Trigger`
    * A watcher will be created to watch changes of kubernetes objects. If any changes occurred, invoke the target user function.

# How Function Pod handles HTTP Requests

By default, when a trigger invokes the target function, a HTTP request will be send to the function pod. 
At this moment a fission component call `executor` will send specialize requests to function pod(s) to load in user function.

![Function pod specialization](/images/how-to-develop-a-serverless-application-with-fission/specialization.svg)

A function pod is consist of two containers: 

* `fetcher`: fetch user function from storage and put it into a shared volume that can read from env container. 
* `env`: load user function and serve HTTP requests.

Here are steps for how to specialize a function pod:

1. Executor sends 1st specialize requests to fetcher to fetch user function
2. Fetcher fetches function from Kubernetes CRD or fission storagesvc
3. Put function file to shared emptyDir volume. Un-archive function file if its a ZIP file
4. Executor sends 2nd specialize requests to env to load-in function
5. Env container search&read function file from shared volume
6. Once whole specialization process finished, Env container start to serve HTTP requests 

# Hello World in Golang (Sample)

After explanation of basic fission concepts and how function pod handles requests, let's start with a simple function first. 

Here are some steps to deploy a Golang function:

1. Create environment
2. Create function
3. Create trigger
4. Check function execution logs

## Create environment

Unlike NodeJS and Python, Golang is compile language and need to compile source code into binary before actually running it. 
From 1.8 Golang added a [plugin](https://golang.org/pkg/plugin/) package, it allows a program to load binary plugin file dynamically.

Luckily, we don't need to build plugin ourselves cause fission `buildermgr` build function source code into executable binary automatically 
once any changes happen to package. 

To enable this feature, we have to assign builder image with `--builder` flag.

```bash
$ fission env create --name go --image fission/go-env --builder fission/go-builder
```

## Create function

Here is a hello world example (hw.go) in Golang:  

```go
// Due to golang plugin mechanism,
// the package of function handler must be main package
package main

import (
    "net/http"
)

// Handler is the entry point for this fission function
func Handler(w http.ResponseWriter, r *http.Request) {
    msg := "Hello, world!\n"
    w.Write([]byte(msg))
}
```

You can create & test with commands:

```bash
# Create golang env with builder image to build go plugin
$ fission fn create --name helloworld --env go --src hw.go --entrypoint Handler
```

There are two interesting flags when creating the function: `--src` and `--entrypoint`.

* `--src` is the source file of a function. Normally, it will be a `ZIP` file, with Golang env you can use a single file as well.
* `--entrypoint` let server know which function to run with. In Go, the value of entrypoint is simply the function name.

When we create a function with `--src` flag, CLI creates a package contains the file we given as `source archive`. A 
fission component call `buildermgr` will detect change of package CRD and help us to build go source code into a plugin file. 
Once the build process completed, the final artifact will be saved in storagesvc and buildermgr will update the reference of `deploy archive` 
in package for fetcher to download with.

You can check the build status & logs with following commands:

```bash
$ fission pkg list
NAME              BUILD_STATUS ENV
hw-go-aazf        succeeded    go

$ fission pkg info --name hw-go-aazf
Name:        hw-go-aazf
Environment: go
Status:      succeeded
Build Logs:
Building file /packages/hw-go-aazf-tzxrip in /usr/src/hw-go-aazf-tzxrip
+ basename /packages/hw-go-aazf-tzxrip
+ srcDir=/usr/src/hw-go-aazf-tzxrip
+ trap rm -rf /usr/src/hw-go-aazf-tzxrip EXIT
+ [ -d /packages/hw-go-aazf-tzxrip ]
+ [ -f /packages/hw-go-aazf-tzxrip ]
+ echo Building file /packages/hw-go-aazf-tzxrip in /usr/src/hw-go-aazf-tzxrip
+ mkdir -p /usr/src/hw-go-aazf-tzxrip
+ cp /packages/hw-go-aazf-tzxrip /usr/src/hw-go-aazf-tzxrip/function.go
+ cd /usr/src/hw-go-aazf-tzxrip
+ go build -buildmode=plugin -i -o /packages/hw-go-aazf-tzxrip-nk71no .
+ rm -rf /usr/src/hw-go-aazf-tzxrip
```

Once the status change from `running` to `succeeded`, we can test function with the built-in test command.

```bash
$ fission fn test --name helloworld
```

**NOTE**: You may experience long cool start time compare to other language. It was caused by the size of deploy archive.

## Create trigger

Now we create a HTTP trigger to listen on the url path `/my-first-function` with `GET` HTTP method.

```bash
# fission httptrigger create --method <HTTP method> --url <url path> --function <function name>
$ fission httptrigger create --method GET --url "/my-first-function" --function helloworld
```

Then, you can access the function with url path defined.

```bash
$ curl http://${FISSION_ROUTER}/my-first-function
```

**NOTE**: For how to set up `$FISSION_ROUTER`, please visit https://docs.fission.io/latest/installation/env_vars/

## Check function execution logs

Fission provides a easy way to view function logs.  

```bash
$ fission fn logs -f --name helloworld
```

Then, the logs of function pod will be printed. 

```bash
[2018-08-22 11:35:35.505701219 +0000 UTC] Listening on 8888 ...
[2018-08-22 11:35:36.088239423 +0000 UTC] 2018/08/22 11:35:36 Fetcher ready to receive requests
[2018-08-22 11:43:49.838357658 +0000 UTC] 2018/08/22 11:43:49 fetcher received fetch request and started downloading: {1 {hw-go-aazf  default    0 0001-01-01 00:00:00 +0000 UTC <nil> <nil> map[] map[] [] nil [] }   e582f69d-a5fe-11e8-a55e-08002720b796 [] [] false}
[2018-08-22 11:43:53.587107386 +0000 UTC] 2018/08/22 11:43:53 Successfully placed at /userfunc/e582f69d-a5fe-11e8-a55e-08002720b796
[2018-08-22 11:43:53.587132444 +0000 UTC] 2018/08/22 11:43:53 Checking secrets/cfgmaps
[2018-08-22 11:43:53.587146255 +0000 UTC] 2018/08/22 11:43:53 Completed fetch request
[2018-08-22 11:43:53.587203725 +0000 UTC] 2018/08/22 11:43:53 elapsed time in fetch request = 3.752048132s
[2018-08-22 11:43:53.588843964 +0000 UTC] Specializing ...
[2018-08-22 11:43:53.588859882 +0000 UTC] loading plugin from /userfunc/e582f69d-a5fe-11e8-a55e-08002720b796/hw-go-aazf-tzxrip-nk71no
[2018-08-22 11:43:53.59725246 +0000 UTC] Done
```

# Add Additional Go Dependencies

Though we already demonstrate how to create a function with single Go file, we often write a Go application with different 
dependencies in real world. To support this, here are couple steps to follow with:

1. Download all necessary dependencies to `vendor` directory
2. Archive all go files (include dependencies)
3. Create function with ZIP file just created

Let's use [vendor-example](https://github.com/fission/fission/tree/master/examples/go/vendor-example) as demonstration. The structure of `vendor-example` looks like this
```bash
vendor-example/
├── main.go
└── vendor
    └── github.com
        └── ......
```

You can use popular Go dependency management tool like `dep` and `glide` to download all dependencies to `vendor` directory. 
Since `vendor-example` is the root directory of user function, we need to ignore it when archiving function files. Otherwise,
the function builder will not be able to find Go files to built with.    

```bash
$ cd ${GOPATH}/src/github.com/fission/fission/examples/go/vendor-example/

# Only archive the files under vendor-example, 
# otherwise go builder will not be able to build plugin
$ zip -r example.zip .

$ fission fn create --name foobar --env go --src example.zip --entrypoint Handler

$ fission fn test --name foobar
```

# Conclusion

This part we introduce the advantage of adopting fission as serverless framework on kubernetes, basic concept of 
around fission core and how to create a simple HelloWorld example with fission.

For [Part 2](/posts/how-to-develop-a-serverless-application-with-fission-pt-2) of this post, we will talk about 
what's the actual request payload being passed to user function and how to create a guestbook application with fission!

In the meantime, feel free to [join the Fission community](https://fission.io/community/)!

---

**_Authors:_**

* Ta-Ching Chen **|** [Fission Contributor](https://github.com/life1347) **|** [Tech blog](https://tachingchen.com/blog)
