---
title: "Troubleshoot Fission Setup"
weight: 2
description: >
  Troubleshoot your Fission setup 
---

In this section, we will cover how to troubleshoot your functions and collect information to troubleshoot problems related to Fission.

### Fission Services Check

From v1.16.0, Fission CLI supports environment check that allows you to check the status of Kubernetes environment and Fission services with a single `check` command.

Check the status of Kubernetes cluster before installing Fission

```bash
$ fission check --pre

kubernetes
--------------------
√ kubernetes version is compatible

```

After Fission is installed, check if all the Fission services are running and healthy

```bash
$ fission check

fission-services
--------------------
√ controller is running fine
√ executor is running fine
√ router is running fine
× storagesvc deployment is not running

fission-version
--------------------
√ fission is up-to-date

```

*The above output shows when any of the Fission services is not running as expected.*

Refer to the following sections for further analysis.

### Check Pods Status and Logs

If the Fission installation doesn't work for you, you can follow guides below to troubleshoot.

#### Core Components

All core component should stay in `RUNNING` state.
If the pod is not in RUNNING state or the `RESTARTS` counts keep increasing, you can get some useful information with commands.

In most cases, `Events` shows common errors like wrong image name, and can help you to locate common problems.

```bash
$ kubectl -n fission describe pod -f <pod>
```

If Events doesn't provide any information, you then need to dump component logs

```bash
$ kubectl -n fission logs -f <pod>
```

For example, here is log from executor which shows that in-Cluster DNS problem (port 53).

```bash
error posting to getting service for function: Post http://executor.fission/v2/getServiceForFunction:
dial tcp: lookup executor.fission on 127.0.0.53:53: read udp 127.0.0.1:59676->127.0.0.53:53: read: connection refused
```

#### Function Pods

A function pod consists with two containers: `Fetcher` and `Runtime`.
Fetcher fetches user function into function pod during specialization stage.
Runtime is a container contains necessary language environment to run user function.

You can filter out function pods you're interesting in and dump logs as follows.

```bash
$ kubectl get pod -l functionName=<fn-name>
```

You can also add additional labels to filter out pods.
Here are some labels you can use.

| Label           | Possible Value    | Example                |
|-----------------|-------------------|------------------------|
| environmentName | environment name  | environmentName=go     |
| functionName    | function name     | functionName=hello     |
| executorType    | poolmgr/newdeploy | executorType=newdeploy |

If you also want to filter out function pod in specific state like `RUNNING`, try:

```bash
$ kubectl get pod -l functionName=<fn-name> \
    --field-selector status.phase=Running
```

Dump logs from containers:

```bash
$ kubectl describe pod -f <pod>
$ kubectl logs -f <pod> -c <container>
```

#### Builder Pods

The builder pods is similar to function pod but for building user function source code into a deployable package.

```bash
$ fission pkg create --env go --src go.zip
Package 'go-zip-5obh' created

$ fission pkg list
NAME          BUILD_STATUS ENV
go-zip-5obh   running      go
```

Your function won't work until the package function used turns into `succeeded` state.
If a package shows state other than succeeded you can retrieve build logs with commands as follows. 

```bash
$ fission pkg list
NAME          BUILD_STATUS ENV
go-zip-a7ns   failed       go

$ fission pkg info --name go-zip-a7ns
Name:        go-zip-a7ns
Environment: go
Status:      failed
Build Logs:
Error building deployment package: Internal error - {"artifactFilename":"go-zip-a7ns-tu8wfl-bkkmcd",
"buildLogs":"Building in directory /usr/src/go-zip-a7ns-tu8wfl\n++ basename /packages/go-zip-a7ns-tu8wfl\n+ 
srcDir=/usr/src/go-zip-a7ns-tu8wfl\n+ trap 'rm -rf /usr/src/go-zip-a7ns-tu8wfl' EXIT\n+ '[' -d /packages/go-zip-a7ns-tu8wfl ']'
\n+ echo 'Building in directory /usr/src/go-zip-a7ns-tu8wfl'\n+ ln -sf /packages/go-zip-a7ns-tu8wfl 
/usr/src/go-zip-a7ns-tu8wfl\n+ cd /usr/src/go-zip-a7ns-tu8wfl\n+ '[' -f go.mod ']'\n+ '[' '!' -z 1.12.7 ']'\n+ 
version_ge 1.12.7 1.12\n++ head -n 1\n++ sort -rV\n++ tr ' ' '\\n'\n++ echo 1.12.7 1.12\n+ test 1.12.7 == 1.12.7\n+ 
go mod download\n+ go build -buildmode=plugin -i -o /packages/go-zip-a7ns-tu8wfl-bkkmcd .\n# 
github.com/fission/fission/examples/go/go-module-example\n./main.go:4:2: imported and not used: 
\"fmt\"\n+ rm -rf /usr/src/go-zip-a7ns-tu8wfl\nerror building source package: error waiting for cmd \"build\": exit status 2\n"}
```

To dump builder logs, you can do:

```bash
$ kubectl get pod -l envName=<env-name>
$ kubectl describe pod -f <pod>
$ kubectl logs -f <pod> -c <container>
```

### Dump Logs for Further Help

If steps above cannot help you to solve the problem, you can run `support` command to dump logs.

```bash
$ fission support dump
```

Then, you can open issue on [GitHub](https://github.com/fission/fission/issues) and upload the dump file for others to help.
