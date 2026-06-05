---
title: "Running container as functions"
draft: false
weight: 46
---

{{% notice info %}}
Support for running containers as functions is in **alpha**.
We plan to improve the experience over the coming releases, and your feedback is most welcome.
{{% /notice %}}

Fission can run an existing container image as a function using the `container` executor type.
This is useful when you already have a containerized HTTP service and want to invoke it through Fission's router and triggers.
For how this executor compares to `poolmgr` and `newdeploy`, see [Controlling Function Execution]({{% ref "executor.en.md" %}}).

#### Running container image with Fission

`fission function run-container` provides required options to run an existing container image as a Fission function.

```sh
$ fission function run-container --name cn-hello --image gcr.io/google-samples/node-hello:1.0 --port 8080
function 'cn-hello' created
```

Listing functions,

```bash
$ fission function list
NAME     ENV    EXECUTORTYPE MINSCALE MAXSCALE MINCPU MAXCPU MINMEMORY MAXMEMORY TARGETCPU SECRETS CONFIGMAPS
cn-hello        container    1        1        0      0      0         0         80
```

Test container function,

```bash
$ fission fn test --name cn-hello
Hello Kubernetes!
```

The container details live in `spec.podspec` of the Function spec.
A function with the `container` executor type must include a pod spec; the API server rejects it otherwise.
To explore the available fields:

```sh
kubectl explain functions.spec.podspec
```

You can also generate function spec with Fission CLI.

```sh
$ fission spec init
Creating fission spec directory 'specs'
$ fission function run-container --name cn-hello --image gcr.io/google-samples/node-hello:1.0 --port 8080 --spec
Saving Function 'default/cn-hello' to 'specs/function-cn-hello.yaml'
$ cat specs/function-cn-hello.yaml
apiVersion: fission.io/v1
kind: Function
metadata:
  creationTimestamp: null
  name: cn-hello
  namespace: default
spec:
  InvokeStrategy:
    ExecutionStrategy:
      ExecutorType: container
      MaxScale: 1
      MinScale: 1
      SpecializationTimeout: 120
      TargetCPUPercent: 80
    StrategyType: execution
  environment:
    name: ""
    namespace: ""
  functionTimeout: 60
  idletimeout: 120
  package:
    packageref:
      name: ""
      namespace: ""
  podspec:
    containers:
    - image: gcr.io/google-samples/node-hello:1.0
      name: cn-hello
      ports:
      - containerPort: 8080
        name: http-env
      resources: {}
  resources: {}
```

### Running Next.js app container with Fission

You can run a sample Next.js based app.

```sh
$ fission fn run-container --name=nextapp --image fission/next-sample-app:1.0.0 --port 3000
function 'nextapp' created
$ fission route create --name nextapp --function nextapp --prefix /nextapp --keepprefix
trigger 'nextapp' created
```

Visit app URL, `http://<router_url>/nextapp/`

You can refer it source for the application [here](https://github.com/fission/examples/tree/main/miscellaneous/container-functions/next-app).

### Command options

The CLI provides short aliases: use `fission fn runc` for `fission function run-container`, and `fission fn updatec` for `fission function update-container`.

Run `fission fn run-container --help` to see all options for creating container-based functions.

#### Related

* [Controlling Function Execution]({{% ref "executor.en.md" %}}) — choosing and tuning executor types.
* [Create a function]({{% ref "functions.en.md" %}}) — the standard source-based function workflow.
