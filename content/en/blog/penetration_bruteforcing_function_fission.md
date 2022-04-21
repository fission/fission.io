+++
title = "Penetration testing with Gobuster & Fission"
date = "2021-04-15T15:57:51+05:30"
author = "Vishal Biyani"
description = "Penetration testing bruteforcing with Gobuster & Fission functions on demand"
categories =["Tutorials"]
type = "blog"
+++

# Introduction

[Gobuster](https://github.com/OJ/gobuster) is a tool for bruteforcing websites Directory/File, DNS and VHost written in Go. It enables penetration testing and and brute forcing for hackers and testers. In this tutorial we will use Gobuster with Fission's binary environment to run it for specific sites and for specific patterns listed in a text file. Fission allows the teams doing penetration testing to focus on code and execution rather than understanding all things around infrastructure.

# Setup

We will start from scratch by creating a Kind cluster and then build from there. We will create a Kind cluster from scratch: 

```
$ kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.18.2) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day! 👋
```

And then create a namespace and install the Fission with a Helm chart. You can update the version of Fission in chart URL to point to latest version

```
$ kubectl create ns fission
$ helm install --namespace fission --name-template fission https://github.com/fission/fission/releases/download/1.12.0/fission-core-1.12.0.tgz

```
# Function code

Now that our Fission setup is ready, let's get the function code ready! You will find all this code and details in fission/example [repo here](https://github.com/fission/examples/tree/main/miscellaneous/gobuster-example) for reference.

We have a simple shell script which uses gobuster binary and provides as argument a website and the txt file which has patterns to be tested for. You can notice that all files are being referenced from directory `/userfunc/deployarchive/` - i.e. because we are using deployment archive type and all files will land in same directory.

```
#!/bin/sh

echo "Inside Shell"
/userfunc/deployarchive/gobuster dir -u https://www.kubeflow.org -w /userfunc/deployarchive/list_small.txt
```

We are using a smaller version of patterns to finish execution faster - but you can always use full list of patterns and use a higher timeout on function so that entire execution actually finishes.

```
.bash_history
.bashrc
.cache
.config
.cvs
.cvsignore
.forward
.git/HEAD
.history
.hta
.htaccess
.htpasswd
```

# Building Custom environment

Now the gobuster binary we plan to use is built for Linux AMD64 architecture but the Fission binary environment is based on Alpine (https://github.com/fission/environments/blob/master/binary/Dockerfile#L8). So we need to customize the Fission's binary environment to use a compatible architecture for gobuster.

So we copy the server.go, env.go and Dockerfile from binary environment of Fission which can be found here: https://github.com/fission/environments/tree/master/binary. 

```
.
├── Dockerfile
├── README.md
├── builder
├── env.go
├── examples
└── server.go
```
We will modify the Dockerfile to use golang image instead of alpine on line 8. We will build this image and use in our function definition.

From:

```Dockerfile
FROM alpine:3.5
```

to:

```Dockerfile
FROM golang:buster
```

# Run, buster, run!

Now that we have all of the things ready, let's create a function spec. The specs are declarative way to use Fission and are easy to make changes and re-apply. For environment we use the Docker image we build in previous step. In function creation command two important points:
- We add all four files to deployarchive - shell script, two txt files with pattern list and the gobuster binary
- The entrypoint for this function is `--entrypoint run.sh`

```
$ fission spec init
$ fission env create --name binary --image vishalbiyani/binary-buster-env:2 --version 3 --poolsize 1 --spec
$ fission fn create --name gobuster --env binary --deploy gobuster --deploy list_small.txt --deploy run.sh --entrypoint run.sh --spec
```
The above commands created the spec file locally, now we can apply them to create in Kind server we created earlier.

```
$ fission spec apply
DeployUID: 911be734-bb01-4abf-b7aa-a8bc99cc7ce9
Resources:
 * 1 Functions
 * 1 Environments
 * 1 Packages
 * 0 Http Triggers
 * 0 MessageQueue Triggers
 * 0 Time Triggers
 * 0 Kube Watchers
 * 1 ArchiveUploadSpec
Validation Successful
uploading archive archive://gobuster-BFoT
1 environment created: binary
1 package created: gobuster-053465b6-c014-4409-8bfb-cc1d4321ab40
1 function created: gobuster

```

Now let's test this against Kubeflow website as an example:

```
$ fission fn test --name gobuster
Inside Shell
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            https://www.kubeflow.org
[+] Threads:        10
[+] Wordlist:       /userfunc/deployarchive/list_small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/04/15 09:17:55 Starting gobuster
===============================================================
===============================================================
2021/04/15 09:17:57 Finished
===============================================================
```

We did not get a whole lot of results, so change the run.sh to point to Apple's website and do fission spec apply again. Now we can test the function with the changes:

```
$ fission fn test --name gobuster
Inside Shell
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            https://www.apple.com
[+] Threads:        10
[+] Wordlist:       /userfunc/deployarchive/list_small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/04/15 06:19:55 Starting gobuster
===============================================================
/.git/HEAD (Status: 403)
/.history (Status: 403)
/.htpasswd (Status: 403)
/.hta (Status: 403)
/.listing (Status: 403)
/.mysql_history (Status: 403)
/.forward (Status: 403)
/.perf (Status: 403)
/.cache (Status: 403)
/.rhosts (Status: 403)
/.htaccess (Status: 403)
===============================================================
2021/04/15 06:19:59 Finished
===============================================================
```

As you can see the results are a bit more verbose this time and Gobuster's response is 403 for a bunch of resources. What we did is a sample of what gobuster can do and we only tried for a few patterns. The gouster can be used with Fission to do extensive penetration testing. The best part is a security person need not know all the things about Kubernetes or deployment and can use Fission to simply write code and execute it.

**Follow us on Twitter for more updates! [@fissionio](https://www.twitter.com/fissionio)**

--- 
**_Author:_**

* [Vishal Biyani](https://twitter.com/vishal_biyani)  **|**  [Fission Contributor](https://github.com/vishal-biyani)  **|**  CTO - [InfraCloud Technologies](http://infracloud.io/)