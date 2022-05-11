---
title: "Fission"
linkTitle: Docs
weight: 20
description: >
  Serverless Functions for Kubernetes
---

## What is Fission?

[fission.io](https://fission.io)  [@fissionio](https://twitter.com/fissionio)

Fission is a fast, open source serverless framework for Kubernetes with a focus on developer productivity and high performance.

Fission operates on _just the code_: Docker and Kubernetes are abstracted away under normal operation, though you can use both to extend Fission if you want to.

Fission is extensible to any language; the core is written in Go, and language-specific parts are isolated in something called _environments_ (more below).
Fission currently supports NodeJS, Python, Go, Java, Ruby, PHP, Bash, and any Linux executable, with more languages coming soon.

## Performance: 100msec cold start

Fission maintains a pool of "warm" containers that each contain a small dynamic loader.
When a function is first called, i.e. "cold-started", a running container is chosen and the function is loaded.
This pool is what makes Fission fast: cold-start latencies are typically about 100msec.

## Kubernetes is the right place for Serverless

We're built on Kubernetes because we think any non-trivial app will use a combination of serverless functions and more conventional microservices, and Kubernetes is a great framework to bring these together seamlessly.

Building on Kubernetes also means that anything you do for operations on your Kubernetes cluster &mdash; such as monitoring or log aggregation &mdash; also helps with ops on your Fission deployment.

## Fission Concepts

Visit [concepts]({{% ref "./concepts/" %}}) for more details.

## Usage

{{< tabs "Run Fission Function" >}}
{{< tab "Node.js function" >}}

```sh
# Add the stock NodeJS env to your Fission deployment
$ fission env create --name nodejs --image fission/node-env

# A javascript function that prints "hello world"
$ curl -LO https://raw.githubusercontent.com/fission/examples/main/nodejs/hello.js

# Upload your function code to fission
$ fission function create --name hello-js --env nodejs --code hello.js

# Test your function.  This takes about 100msec the first time.
$ fission function test --name hello-js
Hello, world!
```

{{< /tab >}}
{{< tab "Python function" >}}

```sh
# Add the stock Python env to your Fission deployment
$ fission env create --name python --image fission/python-env

# A Python function that prints "hello world"
$ curl -LO https://raw.githubusercontent.com/fission/examples/main/python/hello.py

# Upload your function code to fission
$ fission function create --name hello-py --env python --code hello.py

# Test your function.  This takes about 100msec the first time.
$ fission function test --name hello-py
Hello, world!
```

{{< /tab >}}
{{< tab "Go function" >}}

```sh
# Add the stock Go env to your Fission deployment
$ fission env create --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16

# A Go function that prints "hello world"
$ curl -LO https://raw.githubusercontent.com/fission/examples/main/go/hello-world/hello.go

# Upload your function code to fission
$ fission function create --name hello-go --env go --src hello.go --entrypoint Handler

# Wait for your source code to be built, package status should be succeeded. This may take a few minutes.
$ fission pkg list | grep hello-go
hello-go-8bb933b5-b12b-499b-a951-ee2245c8f1b5 succeeded    go     23 Nov 21 10:55 IST

# Test your function. This takes about 100msec the first time.
$ fission function test --name hello-go
Hello, world!
```

{{< /tab >}}
{{< tab "Java function" >}}

```sh
# Add the stock Java env to your Fission deployment
$ fission environment create --name java --image fission/jvm-env --builder fission/jvm-builder --keeparchive --version 3

# A Java function that prints "hello world"
$ mkdir -p src/main/java/io/fission/
$ curl -L https://raw.githubusercontent.com/fission/examples/main/java/hello-world/src/main/java/io/fission/HelloWorld.java \
  -o src/main/java/io/fission/HelloWorld.java
# pom.xml contains dependencies for the function.
$ curl -LO https://raw.githubusercontent.com/fission/environments/master/jvm/examples/java/pom.xml

# Upload your function code to fission via zip
$ zip java-src-pkg.zip -r src/ pom.xml
$ fission package create --name hello-pkg --env java --src java-src-pkg.zip
Package 'hello-pkg' created

# Wait for your source code to be built, package status should be succeeded. This may take a few minutes.
$ fission pkg list | grep hello-pkg
hello-pkg                                     succeeded    java   23 Nov 21 11:19 IST

# Test your function. This takes about 100msec the first time.
$ fission function create --name hello-java --env java --pkg hello-pkg --entrypoint io.fission.HelloWorld
$ fission function test --name hello-java
Hello World!
```

{{< /tab >}}
{{< /tabs >}}

## Fission Examples

Check out more examples on how you can use Fission in our [Fission Examples Repo](https://github.com/fission/examples/).

## Join Us

* [Join Slack](/slack)
* Twitter: https://twitter.com/fissionio
