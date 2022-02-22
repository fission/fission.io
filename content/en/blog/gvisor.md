---
title: "Using gVisor with Fission"
date: 2021-02-10T18:09:02+05:30
author: "Harsh Thakur"
categories: ["Tutorials"]
description: "Running workloads securely with gVisor "
type: "blog"
---

# Introduction

Have you ever run into a scenario where you had to run untrusted code? Containers are great from a performance perspective but they have a considerable access to the kernel which can be exploited. In order to have the security of VMs and speed of containers, projects like [gVisor](https://github.com/google/gvisor) and [kata containers](https://github.com/kata-containers/kata-containers) have risen. In this post, we'll take a look at gVisor provides an application kernel for containers. It provides a runtime which can be used by Kubernetes. To understand more about how gVisor provides security, please go through [this](https://gvisor.dev/docs/architecture_guide/security/).

# Setup of cluster

If you're not using Google Kubernetes Engine, you can checkout the installation supported for your cluster [here](https://gvisor.dev/docs/user_guide/quick_start/kubernetes/).
Google Kubernetes Engine provides the option of using gVisor out of the box. You need to have a GKE cluster running, after which you can add a new node pool on which gVisor is enabled. The new node pool should have :
- Image type should have a container runtime of containerd
- Machine type should be of standard class or higher

You can now browse to the security section and enable sandbox with gVisor

![gvisor-enable](/images/enable-gvisor.png)


# Deploying functions with gVisor

The plain installation of Fission is sufficient to utilize gVisor.

To try out :
- You can clone the [examples repository](https://github.com/fission/examples) 
- Browse to the `samples/hello-py-spec/specs` directory and take a look at the spec of   environment within it.
- Thanks to PodSpec support in Fission, any feature that's available in Kubernetes pods can be utilized by Fission too. In this case, all we need to do is add a `runtimeClassName` field which will instruct the function to use gVisor.

![gvisor-podspec](/images/gvisor-podspec.png)

You can now proceed with the usual:

```
fission spec apply
```

Ta-da! Your functions are now utilsing gVisor. 

# Conclusion
Micro-vm technologies are on the rise as the use for running untrusted code has risen. Fission provides the flexibility to utilize such features out of the box as it is Kubernetes friendly.  We would love to hear how you utilize Fission. 

Here is the guide to [Contributing to Fission](/docs/contributing/)


--- 

**_Authors:_**

* [Harsh Thakur](https://twitter.com/harsh_thakur_1)  **|**  [Fission Contributor](https://github.com/RealHarshThakur)  **|**  Product Engineer - [InfraCloud Technologies](http://infracloud.io/)