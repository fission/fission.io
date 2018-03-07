---
title: "Hello World: Creating Functions using Fission (in Golang)"
author: "Timirah James, Developer Advocate"
date: 2018-03-05T11:13:45-08:00
draft: true
---


# First, What is Serverless?

In the last blog post [Kubernetes for Newbies](https://fission.io/blog/posts/kubernetes_hello-world/), we went over how to get an application up and running on Kubernetes. Though Kubernetes is surely a hot topic in tech, the “serverless” space has become just as (if not even more) trendy. Why is serverless so popular in the dev community? 

Turns out, serverless is a developer’s saving grace when it comes to managing servers. Instead of managing a bunch of servers, Serverless solutions allow developers to … well … not manage servers at all! Serverless completely takes away the burden of managing servers. One could say that Serverless separates the “ops” from devs. Functions as a Service (FaaS) enable developers to deploy parts of an application on an "as needed" basis using short-lived functions in just about any programming language. 

Benefits of using FaaS range from simplified scaling, to easier deployment, lowered costs (you only pay for the resources you use, as opposed to otherise paying on a per-second basis).



Let’s do a quick walk thru of how to deploy "Hello World" using Fission Functions!


---- 

# Installations

Before we begin, we’ll need to make sure we’ve done the following:

- Install the [Kubernetes CLI (kubectl)](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Install [Minikube](https://github.com/kubernetes/minikube)
- Install and initialize [Helm](https://github.com/kubernetes/helm)


**_Now we can install Fission._**

Let’s do so using this command:

	$ helm install --namespace fission https://github.com/fission/fission/releases/download/0.6.0/fission-all-0.6.0.tgz


### Install the Fission CLI

Let’s install the command-line tool for Fission.

If you’re running **OS X**, you can install the Fission CLI by running the following command:				
					
	$ curl -Lo fission
	https://github.com/fission/fission/releases/download/0.6.0/fission-cli-osx
	&& chmod +x fission && sudo mv fission /usr/local/bin/


**For Linux:**

	$ curl -Lo fission https://github.com/fission/fission/releases/download/0.6.0/fission-cli-linux && chmod +x fission && sudo mv fission /usr/local/bin/


**For Windows, download the executable using [this link](https://github.com/fission/fission/releases/download/0.6.0/fission-cli-windows.exe).**

>_You can find a complete list of Fission releases here: https://github.com/fission/fission/releases_

>_To check the current installed version of Fission on your cluster, simply run:_

	$ helm ls


----


# Deploy "Hello World!"

### Run Fission (Locally)

Now that we have all the proper tooling installed, we’re now ready to create our first function with Fission! 

*(Just as we did in the [previous blog post](http://fission.io/blog/posts/kubernetes_hello-world/), we'll be using Minikube to run Kubernetes locally.)*

Go ahead and launch your cluster by running the following commands:			
					
	$ minikube start
	$ kubectl get nodes

----

### Creating Our Function

In order to create a function, you’ll need to first create an _environment_, which makes Fission language specific.

Let’s create a **Go** environment using the following command:

	fission env create --name go --image fission/go-env --builder fission/go-builder


We’ll be using the Golang Hello World example from the fission github repo (which can be found [here](https://github.com/fission/fission/blob/master/examples/go/hello.go)), so we’ll need to download the code using the following command:
									
	$ curl https://raw.githubusercontent.com/fission/fission/master/examples/go/hello.go > /tmp/hello.go


Now let’s deploy our function using this command:

	$ fission function create --name hello --env go --code /tmp/hello.go --entrypoint Handler

>

Finally, we can invoke our function, using this command:

	$ fission function test --name hello

	
----

## What's Next?

Go ahead and try your hand at using Fission Functions for your own cool projects! Remember that you can use Fission with other languages. Try it out using NodeJS, Python, Ruby, or any of the other languages within our listed [enviroments](https://github.com/fission/fission/tree/master/environments)! Don't forget to tell us about what you made by tweeting us [@Fissionio](http://twitter.com/fissionio), and feel free to ask questions on our Slack http://fissionio.slack.com.



_**Author:**_ Timirah James **|** Fission Developer Advocate, Platform9 Systems  **|**  [Tweet the Author](https://www.twitter.com/timirahj)
