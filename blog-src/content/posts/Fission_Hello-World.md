---
title: "Hello World: Creating Functions using Fission"
author: "Timirah James, Developer Advocate"
date: 2018-03-07T13:52:34-08:00
draft: false
---


In the last blog post (Kubernetes for Newbies) [link], we went over how to get an application up and running on Kubernetes. Though Kubernetes is surely a hot topic in tech, the “serverless” space has become just as -- if not even more -- trendy. So what’s the big deal? Why is serverless so popular in the dev community? To tell you the truth, I hadn’t discovered the answer to this until just a few months ago.   . . .


Let’s do a quick walk thru of how to deploy Hello World using Fission Functions!


## Prerequisites

Before we begin, we’ll need to make sure we’ve done the following:

- Install the Kubernetes CLI [link]
- Install Minikube [link]
- Install and initialize Helm [link]


Install the Fission CLI

Let’s install the command-line tool for Fission.

If you’re running OS X, you can install the Fission CLI by running the following command:				
					
	$ curl -Lo fission
	https://github.com/fission/fission/releases/download/0.6.0/fission-cli-osx
	&& chmod +x fission && sudo mv fission /usr/local/bin/


For Linux:

	$ curl -Lo fission https://github.com/fission/fission/releases/download/0.6.0/fission-cli-linux && chmod +x fission && sudo mv fission /usr/local/bin/


For Windows, download the executable using [this link] [ask Soam for 0.6.0 release link].


>_To check the current installed version of Fission, simply run:_

	fission --version

