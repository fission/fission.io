---
title: "Glossary"
weight: 9
description: >
  Fission Glossary - List of terms used in Fission.
---

[A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [G](#g) | [H](#h) | [I](#i) | [J](#j) | [K](#k) | [L](#l) | [M](#m) | [N](#n) | [O](#o) | [P](#p) | [Q](#q) | [R](#r) | [S](#s) | [T](#t) | [U](#u) | [V](#v) | [W](#w) | [X](#x) | [Y](#y) | [Z](#z)

## A

---

### Annotation - -*-ingressannotation*

Use `--ingressannotation` to specify meta data while creating HTTP Trigger and customize their behavior.

### Archive

An archive is a zip file containing the source code or compiled binaries.

## B

---

### Builder Pod

Builder pod is a specialized pod that builds the source archive and generate a deployment archive.

### Build Container

Builder Container compiles function source code into executable binary/files and is language-specific.

### Builder Manager

In a nutshell, the builder Manager manages the builds of function source code.

Once an environment that contains a builder image is created, the builder manager will then create the Kubernetes service and deployment under the `default` namespace to start the environment builder. And once a package that contains a source archive is created, the builder manager talks to the environment builder to build the function’s source archive into a deploy archive for function deployment.

### Build Status

Build status indicates the current build status of a package.

### Build.sh

Build.sh is a shell script file that is used to create a custom package by installing third party modules present in the requirements.txt file.

## C

---

### Canary Config

A canary config is custom resource used to configure a canary deployment for Fission functions.

### Canary Deployment

Canary Deployment is a deployment strategy to deploy a new version of your Fission function to a cluster incrementally with minimal risk in a way that it gradually serves user traffic from 0% to 100%.

### Cold Start

It is defined as the setup time that is required for a function to be up and running when it is invoked for the first time in a defined period to serve user requests.

### Concurrency

Concurrency refers to the amount of requests a function should process simultaneously.

### Controller

Controller contains CRUD APIs for functions, triggers, environments, Kubernetes event watches, etc. and proxy APIs to internal 3rd-party services. A client talks to the controller.

## D

---

### Deployment Archive

Deployment archive is an archive file that contains a runnable function.

### Duration - *Canary Config*

Specifies how frequently user traffic needs to be incremented for the new version of function

## E

---

### Environment

Environments provide a run time which is used to execute Fission functions. Currently, Fission supports pre-built environments that include NodeJS, Python3, Go, JVM, Ruby, Binary, PHP, .NET and Pearl.

### Executor

Executor is responsible for spinning up function pods. It retrieves function information from Kubernetes CRD and invokes an executor type to spin up a function pod.

## F

---

### Failure Threshold - *Canary Config*

Specifies the threshold in percentage beyond which the new version of a function is declared unhealthy.

### Failure Type - *Canary Config*

Specifies the parameter for checking the health of the new version of a function. *For now, the only supported type is status-code which is the http status code. So if a function returns a status code other than 200, it is considered to be unhealthy.*

### Fetcher

Fetcher pulls the [source archive](#source-archive) from the [storage service](#storage-service) and verifies the checksum of the file. After the build is complete, it uploads the [deployment archive](#deployment-archive) to the storage service.

### Fission CLI

Fission CLI is the command line utility that allows you to interact with and operate Fission.

### Fission Images

### Fission Specs

Fission spec is a declarative way to manage an application's specification.

### Function

A serverless function in Fission.

### Function Pod

Function pod is where a Fission function is loaded and executed. A function pod serves HTTP requests it receives from clients.

## G

---

## H

---

### HTTP Trigger / Route

It is a type of trigger that invokes a Fission function whenever there is an HTTP request. You can specify a relative URL and HTTP method for an HTTP trigger.

---

## I

---

## J

---

## K

---

### Kubernetes Watch Trigger

KubernetesWatchTrigger is a custom resource that watches Kubernetes resource events and invokes functions.

### KubeWatcher

Kubewatcher watches the Kubernetes API and invokes functions associated with watches, sending the watch event to the function.

## L

---

### Logger

Logger is a daemonset that forwards function logs to a centralized database service for log persistence. *Currently only InfluxDB is supported.*

## M

---

### Max CPU

Maximum CPU to be assigned to pod *(function in case of New Deploy)* *(In millicore, minimum 1)*

### Min CPU

Minimum CPU to be assigned to pod *(function in case of New Deploy)* *(In millicore, minimum 1)*

### Max Memory

Maximum memory to be assigned to pod *(function in case of New Deploy)* *(In megabyte)*

### Min Memory

Minimum memory to be assigned to pod *(function in case of New Deploy)**(In megabyte)*

### Max Scale

Maximum number of pods *(Uses resource inputs to configure HPA)*

### Min Scale

Minimum number of pods *(Uses resource inputs to configure HPA)*

### Message Queue Trigger

A message queue trigger listens to messages in a message queue and invokes a function based on the arrival of a message in a queue.

## N

---

### New Deploy

New Deploy is a type of [executor](#executor) that creates a Kubernetes deployment along with a service and a Horizontal Pod Autoscalar (HPA) for function execution.

### New Function - *Canary Config*

Specifies the name of the latest version of the function.

## O

---

### Old Function - *Canary Config*

Specifies the name of the current stable version of the function.

## Once Only

OnceOnly is similar to a Kubernetes Job, it is useful in long-running tasks where only one request is served by one pod. Each request is assured to be served by a new pod.

## P

---

### Package

A package in fission can be a source package or a deployment package. A source package contains your source code and related libraries while a deployment package is the one that has an executable code.

### Persistent Volume

A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes.

### Pool Manager

PoolManager manages pools of generic containers and function containers.

### Pool Size

The size of pool i.e.: number of pods in a pool.

## Q

---

## R

---

### Requests Per Pod

RequestsPerPod denotes how many requests will be routed to each pod in Pool Manager.

### Requirements.txt

This is a file that lists down all the external 3rd party modules, libraries that are required for your function to execute.

### Router

Router is responsible for forwarding HTTP requests to function pods.

### Runtime

## S

---

### Source Archive

Source archive is an archive file that contains the source code.

### Specification

Specifications (*specs*) are YAML files that are used to instruct Fission CLI about what objects to create or update.

### Storage Service

The storage service is the home for all archives of packages with sizes larger than 256 KB.

## T

---

### Target CPU

This is the CPU utilization limit (*in percentage*) based on which the HPA adds/removes pods.

### Timer

A timer invokes a function periodically by sending a request to the router. Suitable for background tasks that need periodic execution.

### Time Trigger

TimeTrigger invokes functions based on given cron schedule.

### TLS - *--ingressTLS*

Set this flag to enable TLS termination while creating an ingress.

### Toleration

Toleration is a mechanism in Kubernetes to influence the scheduling of pods.

### Trigger

Trigger configures Fission to use an event to invoke a function.

### Trigger - *Canary Config*

Specifies the name of the http trigger object.

## U

---

## V

---

### Volume

A volume is Kubernetes represents a directory with data that is accessible across multiple containers in a pod.

## W

---

### Weight Increment - *Canary Config*

Specifies the percentage increase of user traffic towards the new version of the function.

## X

---

## Y

---

## Z

---
