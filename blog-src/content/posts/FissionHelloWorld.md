---
title: "Hello World: Creating Functions using Fission"
author: "Timirah James, Developer Advocate"
date: 2018-03-05T11:13:45-08:00
draft: true
---


In the last blog post [Kubernetes for Newbies](https://fission.io/blog/posts/kubernetes_hello-world/), we went over how to get an application up and running on Kubernetes. Though Kubernetes is surely a hot topic in tech, the “serverless” space has become just as -- if not even more -- trendy. So what’s the big deal? Why is serverless so popular in the dev community? To tell you the truth, I hadn’t discovered the answer to this until just a few months ago... 

[Elaborate briefly on benefits]



Let’s do a quick walk thru of how to deploy Hello World using Fission Functions!


### Prerequisites

Before we begin, we’ll need to make sure we’ve done the following:

- Install the Kubernetes CLI [link]
- Install Minikube [link]
- Install and initialize Helm [link]

----

### Install Fission

Now we can install Fission. 

Let’s do so using this command:

$ helm install --namespace fission --set serviceType=NodePort https://github.com/fission/fission/releases/download/0.6.0/fission-all-0.6.0.tgz


>_The serviceType variable allows configuring the type of Kubernetes service outside the cluster. You can use **ClusterIP** if you don’t want to expose anything outside the cluster._


### Install the Fission CLI

Let’s install the command-line tool for Fission.

If you’re running **OS X**, you can install the Fission CLI by running the following command:				
					
	$ curl -Lo fission
	https://github.com/fission/fission/releases/download/0.6.0/fission-cli-osx
	&& chmod +x fission && sudo mv fission /usr/local/bin/


**For Linux:**

	$ curl -Lo fission https://github.com/fission/fission/releases/download/0.6.0/fission-cli-linux && chmod +x fission && sudo mv fission /usr/local/bin/


**For Windows, download the executable using [this link] [ask Soam for 0.6.0 release link].**


>_To check the current installed version of Fission, simply run:_

	fission --version


----

In the [previous blog post](https://fission.io/blog/posts/kubernetes_hello-world/), we ran Kubernetes locally using Minikube. Let’s take a look at how we’d do the same here with Fission. 

### Run Fission (Locally)

Now that we have all the proper tooling installed, we’re now ready to create our first function with Fission! 

Go ahead and launch your cluster by running the following commands:			
					
	$ minikube start
	$ kubectl get nodes

----

### Environment Variables

Environment Variables

Next, we’ll need to set the Fission environment variables, FISSION_URL and FISSION_ROUTER. 

Let’s do this by running these commands:

	$ export FISSION_URL=http://$(minikube ip):31313
	$ export FISSION_ROUTER=$(minikube ip):31314

> FISSION_URL is used by the Fission CLI to find the server. We'll look into the FISSION_ROUTER variable later on in the project.


----

### Creating Our Function

In order to create a function, you’ll need to first create an _environment_, which makes Fission language specific.

Let’s create a **Go** environment using the following command:

	fission env create --name go --image fission/go-env


We’ll be using the Golang Hello World example from the fission github repo (which can be found [here](https://github.com/fission/fission/blob/master/examples/go/hello.go)), so we’ll need to download the code using the following command:
									
	$ curl https://raw.githubusercontent.com/fission/fission/master/examples/go/hello.go > /tmp/hello.go


Now let’s deploy our function using this command:

	$ fission function create --name hello --env go --code /tmp/hello.go


Finally, we need to create a route to our function, using this command:

	$ fission route create --method GET --url /hello --function hello


And now we can use our other environment variable, **FISSION_ROUTER** in order to trigger our function. We can do this by making an HTTP request as such:

	$ curl http://$FISSION_ROUTER/hello
	
----

### What's Next?




