---
title: "Installing Fission"
linkTitle: Installation
weight: 1
description: >
  Installation guide for Fission installation
---
Welcome! This guide will get you up and running with Fission on a Kubernetes cluster.

## Prerequisites

First, let's ensure you have the [Kubernetes CLI](https://kubernetes.io/docs/reference/kubectl/overview/) and [Helm](https://helm.sh/docs/intro/install/) installed and ready along with a [Kubernetes Cluster](https://kubernetes.io/docs/setup/).
If you already have Helm, [skip ahead to the fission install](#install-fission).

### Kubernetes Cluster

If you don't have a Kubernetes cluster, [here's a official guide to set one up](https://kubernetes.io/docs/setup/).

{{< notice info >}}
Fission requires Kubernetes 1.19 or higher
{{< /notice >}}

### Kubectl

Kubectl is a command line interface for running commands against Kubernetes clusters, visit [kubectl docs](https://kubernetes.io/docs/tasks/tools/#kubectl) to see how to install it.

Next, ensure you have access to a cluster. Do this by using kubectl to check your Kubernetes version:

```console
kubectl version
```

### Helm

Helm is an installer for Kubernetes. If you already use helm, [skip to the next section](#install-fission).

If you cannot use Helm, there is an alternative installation method possible; see [installing without Helm](#without-helm).

To install helm, first you'll need the helm CLI. Visit [here](https://helm.sh/docs/intro/install/) to see how to install it.

{{< notice info >}}
Helm v2 is deprecated, Fission can be installed via Helm v3.
You can skip the following and head over [Fission installation](#install-fission) if you're using Helm **v3**.
{{< /notice >}}

## Install Fission

### With Helm

{{< notice warning >}}
With 1.15 release, `fission-core` is removed. Please use `fission-all` chart for migration.

Refer [1.15 release notes]({{< ref "v1.15.0.md" >}}) for more details.

If you are upgrading Fission, do check [upgrade guide]({{< ref "upgrade.md" >}})
{{< /notice >}}

{{< notice warning >}}
With 1.18 release, the namespaces `fission-function` and `fission-builder` will no longer be created. Instead, all resources will be created in the same namespace for all namespaces.

Refer [1.18 release notes]({{< ref "v1.18.0.md" >}}) for more details.
{{< /notice >}}

{{< notice info>}}
serviceType, routerServiceType can be `NodePort` or `LoadBalancer` for external access to Fission in below steps.
You can use `ClusterIP` if you want to access Fission from within the cluster.

See [Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing). 
To see all configurable options with detailed comments:

```shell
helm show values fission-charts/fission-all
```

Checkout [Fission on ArtifactHub](https://artifacthub.io/packages/helm/fission-charts/fission-all) for chart supported values.
{{< /notice >}}

{{< tabs "fission-install" >}}
{{< tab "GKE, AKS, EKS" >}}

See [how to add token to kubeconfig]({{% ref "../trouble-shooting/setup/kubernetes.md" %}}#kubeconfig-for-connecting-to-cluster) if you're not able to connect to cluster.

```sh
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
helm install --version {{% release-version %}} --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

{{< /tab >}}
{{< tab "Minikube, Docker Desktop, Kind" >}}

```sh
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
helm install --version {{% release-version %}} --namespace $FISSION_NAMESPACE fission \
  --set serviceType=NodePort,routerServiceType=NodePort \
  fission-charts/fission-all
```

{{< /tab >}}
{{< tab "OpenShift without LoadBalancer" >}}

```sh
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
helm install --version {{% release-version %}} --namespace $FISSION_NAMESPACE fission \
  --set serviceType=NodePort,routerServiceType=NodePort,logger.enableSecurityContext=true \
  fission-charts/fission-all
```

{{< /tab >}}
{{< tab "OpenShift" >}}

```sh
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
helm repo add fission-charts https://fission.github.io/fission-charts/
helm repo update
helm install --version {{% release-version %}} --namespace $FISSION_NAMESPACE fission \
    --set logger.enableSecurityContext=true \
    fission-charts/fission-all
``````

{{< /tab >}}
{{< /tabs >}}


### Without helm

This method uses `kubectl apply` to install Fission.
You can edit the YAML file before applying it to your cluster, if you want to change anything in it.
Create namespace for fission installation.

```sh
kubectl create namespace fission
```

{{% notice info %}}
If you want to install in another namespace, please consider to use `helm` or generate yaml for first with `helm template` command.
{{% /notice %}}

Choose _one_ of the following commands to run:

{{< tabs "fission-install-without-helm" >}}
{{< tab "Basic with LoadBalancer" >}}

```bash
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl config set-context --current --namespace=$FISSION_NAMESPACE
kubectl apply -f https://github.com/fission/fission/releases/download/{{% release-version %}}/fission-all-{{% release-version %}}.yaml
```

{{< /tab >}}
{{< tab "Minikube, Docker Desktop, Kind" >}}

```bash
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl config set-context --current --namespace=$FISSION_NAMESPACE
kubectl apply -f https://github.com/fission/fission/releases/download/{{% release-version %}}/fission-all-{{% release-version %}}-minikube.yaml
```

{{< /tab >}}
{{< tab "OpenShift" >}}

```bash
kubectl create -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
kubectl config set-context --current --namespace=$FISSION_NAMESPACE
kubectl apply -f https://github.com/fission/fission/releases/download/{{% release-version %}}/fission-core-{{% release-version %}}-openshift.yaml
```

{{< /tab >}}
{{< /tabs >}}

## Install Fission CLI

Fission CLI helps you to operate Fission. Checkout [Fission CLI reference]({{< ref "fission-cli" >}}) for more.

{{< tabs "fission-cli-install" >}}
{{< tab "MacOS" >}}

```bash
curl -Lo fission https://github.com/fission/fission/releases/download/{{% release-version %}}/fission-{{% release-version %}}-darwin-amd64 \
    && chmod +x fission && sudo mv fission /usr/local/bin/
```

{{< /tab >}}
{{< tab "Linux" >}}

```bash
curl -Lo fission https://github.com/fission/fission/releases/download/{{% release-version %}}/fission-{{% release-version %}}-linux-amd64 \
    && chmod +x fission && sudo mv fission /usr/local/bin/
```

{{< /tab >}}
{{< tab "NixOS" >}}

```sh
nix-env -iA nixos.fission
```

{{< /tab >}}
{{< tab "Windows" >}}
For Windows, you can use the linux binary on WSL. Or you can download
this windows executable: [fission.exe](https://github.com/fission/fission/releases/download/{{% release-version %}}/fission-{{% release-version %}}-windows-amd64.exe)
{{< /tab >}}
{{< /tabs >}}


## Verify fission installation
Once you are done with fission installation, run these commands to make sure fission is installed successfully and all core components of fission are working properly.

To check fission is installed successfully, run this command and verify both client and server version should be same. 

```shell
$ fission version
client:
  fission/core:
    BuildDate: "2023-01-25T04:56:25Z"
    GitCommit: deb3523
    Version: {{% release-version %}}
server:
  fission/core:
    BuildDate: "2023-01-25T04:53:33Z"
    GitCommit: deb3523
    Version: {{% release-version %}}

```

To check fission core components are working properly, run this command.

```shell
$ fission check
fission-services
--------------------
√ executor is running fine
√ router is running fine
√ storagesvc is running fine
√ webhook is running fine

fission-version
--------------------
√ fission is up-to-date

```

{{% notice info %}}
If you have enabled authentication while installing fission, mentioned above commands won't show proper result. You need to generate token to make it work.

See [How to generate auth token](https://fission.io/docs/installation/authentication/#generating-auth-token), if authentication is enabled.
{{% /notice %}}

## Run an example

Finally, you're ready to use Fission!

{{% notice info %}}
It might take one or two mintues for fission to start running. check the status using `kubectl get pods -n fission`. 
{{% /notice %}}

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

For more language tutorials, visit [Language]({{< ref "../usage/languages/" >}}).

## What's next?

If something went wrong, we'd love to help -- please [drop by the Fission slack](/slack) and ask for help.

Check out the
[examples](https://github.com/fission/examples/tree/main)
for some example functions.
