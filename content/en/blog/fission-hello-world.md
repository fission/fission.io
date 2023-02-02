+++
title = "Hello World: Creating Functions using Fission (in Golang)"
date = "2018-03-05T11:13:45-08:00"
author = "Timirah James"
categories = ["Tutorials"]
type = "blog"
+++


# First, What is Serverless?

In the last blog post [Kubernetes for Newbies](/blog/hello-world-creating-functions-using-fission-in-golang/), we went over how to get an application up and running on Kubernetes. Though Kubernetes is surely a hot topic in tech, the “serverless” space has become just as (if not even more) trendy. Why is serverless so popular in the dev community?

Turns out, serverless is a developer’s saving grace when it comes to managing servers. Instead of managing a bunch of servers, Serverless solutions allow developers to … well … not manage servers at all! Serverless completely takes away the burden of managing servers. One could say that Serverless separates the “ops” from devs. Functions as a Service (FaaS) enable developers to deploy parts of an application on an "as needed" basis using short-lived functions in just about any programming language. 

Benefits of using FaaS range from simplified scaling, to easier deployment, lowered costs (you only pay for the resources you use, as opposed to otherwise paying on a per-second basis).

Let’s do a quick walk through of how to deploy "Hello World" using Fission Functions!

----

## Installations

We'll be using Minikube to run Kubernetes locally (just as we did in the [previous blog post](/blog/hello-world-in-go-for-kubernetes-newbies/)).

### Install Minikube

 Go ahead and follow the instructions to [install Minikube](https://github.com/kubernetes/minikube).

After you have Minikube installed, launch your cluster by running the following command:			
					
	$ minikube start

### Install the Kubernetes CLI (kubectl)

Once your cluster is ready, you'll need to install the Kubernetes CLI kubectl [as instructed here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

You can verify if the installation was successful by running:

	$ kubectl get nodes

### Install Helm

Install Helm using the instructions found [here](https://github.com/kubernetes/helm).

Make sure Helm is initialized by running:

	$ helm init


### Install Fission.

Now let's install Fission using the following command:

	$ helm install --namespace fission https://github.com/fission/fission/releases/download/0.6.0/fission-all-0.7.2.tgz


### Install the Fission CLI

Next we'll need to install the command-line tool for Fission.

If you’re running **OS X**, you can install the Fission CLI by running the following command:				
					
	$ curl -Lo fission
	https://github.com/fission/fission/releases/download/0.7.2/fission-cli-osx
	&& chmod +x fission && sudo mv fission /usr/local/bin/


**For Linux:**

	$ curl -Lo fission https://github.com/fission/fission/releases/download/0.7.2/fission-cli-linux && chmod +x fission && sudo mv fission /usr/local/bin/


**For Windows, download the executable using [this link](https://github.com/fission/fission/releases/download/0.6.0/fission-cli-windows.exe).**

> You can find a complete list of Fission releases here: https://github.com/fission/fission/releases

_To check the current installed version of Fission on your cluster, simply run:_

	$ helm ls


----


# Deploy "Hello World!"


Now that we have all the proper tooling installed, we’re now ready to create our first function with Fission! 


### Creating Our Function

In order to create a function, you’ll need to first create an _environment_, which makes Fission language specific.

Let’s create a **Go** environment using the following command:

	fission env create --name go --image fission/go-env --builder fission/go-builder

>**NOTE**: _Since you are creating a new environment, it may take a few extra seconds before the Go environment pods are up and running in the default namespace._

To verify if the pods are up and running, be sure to run this command:

	$ kubectl get pods | grep go

>_(The status of the pods should be "Running")_


We’ll be using the Golang Hello World example from the fission github repo (which can be found here: https://github.com/fission/examples/blob/main/go/hello-world/hello.go ), so we’ll need to download the code using the following command:
									
	$ curl https://raw.githubusercontent.com/fission/examples/main/go/hello-world/hello.go > /tmp/hello.go

Now let’s deploy our function using this command:

	$ fission function create --name hello --env go --src /tmp/hello.go --entrypoint Handler


Finally, we can invoke our function, using this command:

	$ fission function test --name hello

	
----

## What's Next?

Go ahead and try your hand at using Fission Functions for your own cool projects! Remember that you can use Fission with other languages. Try it out using NodeJS, Python, Ruby, or any of the other languages within our listed [fission environments](/environments/)! Don't forget to tell us about what you made by tweeting us [@fissionio](http://twitter.com/fissionio), and feel free to ask questions on our Slack http://fissionio.slack.com.



_**Author:**_ Timirah James **|** Fission Developer Advocate, Platform9 Systems  **|**  [Tweet the Author](https://www.twitter.com/timirahj)
