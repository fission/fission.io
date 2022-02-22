+++
title = "Functions On Steroids With PodSpec"
date = "2019-05-20T13:41:33+05:30"
author = "Vishal Biyani"
description = "Using podSpec with Fission function specifications"
categories = ["Fission"]
type = "blog"
+++

There are features which enable a specific new functionality and then there are features which enable a whole new class of functionality in a product. I am excited to share that PodSpec is now available in Fission. Fission functions can be extended to do many things with PodSpec - such as tolerations, volumes, security context, and more.

Previously, Fission had support for "container specs" - which allowed you to add environment variables, etc. to functions. With PodSpec - a whole spectrum of new possibilities are now unlocked. While "container spec" still exists for backward compatibility, we recommend using PodSpec for extending your Fission functions moving forward. In this tutorial we will walk through various use cases and working examples with PodSpec.

## What is PodSpec

A pod in Kubernetes is basic unit of deployment. Like every Kubernetes resource the pod consists of the basic declaration, metadata, spec & status.

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    svc-name: svc-name
  name: podname
spec:
  containers:
  ```

The spec in a pod, also known as PodSpec, defines [the specifications](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) of many behaviors in a declarative manner. A PodSpec defines the containers, environment variables for the container and other properties such as the scheduler name, security context etc.

```
spec:
  containers:
    env:
    - name: ENV_NAME
      value: ENV_VALUE
    image: image_url
    imagePullPolicy: IfNotPresent
  dnsPolicy: ClusterFirst
  nodeName: nodename
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: fission-svc
```

Fission now supports using PodSpec in the Fission environment specs. In this tutorial we will look at various use cases that are possible with PodSpec support in Fission. To learn more about the Fission specs please check [this documentation link](/docs/usage/spec/).

## Podspec use cases for serverless functions

**Note**: PodSpec is in alpha stage and it's behavior may be changed in the future.

### Tolerations on functions

**Taints and tolerations** are mechanisms to influence scheduling of pods in Kubernetes. There are use cases where you want to schedule specific pods onto machines with certain hardware or specific capabilities such as CPU intensive instances. The basic mechanism works by applying taints on nodes of a cluster and tolerations on pods. The pods with tolerations matching a certain taint can get scheduled on those nodes.

Now you can specify tolerations on functions in the function specification. Let's start with tainting two nodes with "reservation=fission" and two nodes with "reservation=microservices" as shown below. The intent is that two nodes are optimized for functions and other two nodes in cluster are better optimized for long running microservices. We want to schedule functions on nodes with taints meant for functions.

```
$ kubectl taint nodes gke-vishal-fission-dev-default-pool-87c8b616-549c gke-vishal-fission-dev-default-pool-87c8b616-5q2c reservation=fission:NoSchedule

node "gke-vishal-fission-dev-default-pool-87c8b616-549c" tainted
node "gke-vishal-fission-dev-default-pool-87c8b6aCloud16-5q2c" tainted

$ kubectl taint nodes gke-vishal-fission-dev-default-pool-87c8b616-pg05 gke-vishal-fission-dev-default-pool-87c8b616-t5q1 reservation=microservices:NoSchedule

node "gke-vishal-fission-dev-default-pool-87c8b616-pg05" tainted
node "gke-vishal-fission-dev-default-pool-87c8b616-t5q1" tainted
```

In the fission env spec, let's add PodSpec and toleration for "reservation=fission"

```
  runtime:
    functionendpointport: 0
    image: fission/node-env
    loadendpointpath: ""
    loadendpointport: 0
    podspec:
      tolerations:
      - key: "reservation"
        operator: "Equal"
        value: "fission"
        effect: "NoSchedule"
```

Once we apply fission specs and run the function - you will notice that the pods go only on nodes with taints that match the toleration:

```
$kgpo $ff -owide
NAME                                                 READY     STATUS    RESTARTS   AGE       IP             NODE
newdeploy-pyfunc-default-kgsuik0l-66cd755675-jgjj6   2/2       Running   0          51s       10.16.177.16   gke-vishal-fission-dev-default-pool-87c8b616-549c
poolmgr-python-default-okhvkdsv-57b866b774-hbz7q     2/2       Running   0          49s       10.16.176.34   gke-vishal-fission-dev-default-pool-87c8b616-5q2c
poolmgr-python-default-okhvkdsv-57b866b774-hqnl2     2/2       Running   0          49s       10.16.176.35   gke-vishal-fission-dev-default-pool-87c8b616-5q2c
poolmgr-python-default-okhvkdsv-57b866b774-pmtzv     2/2       Running   0          49s       10.16.177.17   gke-vishal-fission-dev-default-pool-87c8b616-549c

```

Let's remove taint from all nodes so we are back to original clean state:

```
$ kubectl taint nodes gke-vishal-fission-dev-default-pool-87c8b616-549c gke-vishal-fission-dev-default-pool-87c8b616-5q2c gke-vishal-fission-dev-default-pool-87c8b616-pg05 gke-vishal-fission-dev-default-pool-87c8b616-t5q1 reservation:NoSchedule-
```

### Functions with volumes

Functions are great for stateless things but there use cases where functions deal with data, that is best attached as volume. For example, functions used in data pipelines would benefit a lot from volumes being attached to functions. 

With PodSpec you can now attach a volume to a function. You have to **define a volume** and then **mount it on specific container**. In the following example we create a simple volume with Kubernetes downward API which dumps information of labels in a file. The volume is then mounted on the function container at `/etc/funcdata`


```
apiVersion: fission.io/v1
kind: Environment
metadata:
  creationTimestamp: null
  name: nodep
  namespace: default
spec:
  TerminationGracePeriod: 360
  ...
  <SOME CONTENT TRUNCATED>
  ...
  podspec:
      # A container which will be merged with for pool manager
      Containers:
      - name: nodep
        image: fission/node-env
        volumeMounts:
          - name: funcvol
            mountPath: /etc/funcdata
            readOnly: true
      volumes:
        - name: funcvol
          downwardAPI:
            items:
              - path: "labels"
                fieldRef:
                  fieldPath: metadata.labels
  ```


### InitContainers with Volumes!

Functions could also benefit from an **initialization process** before actually executing the functions. The initialization could allow you to fetch data from a remote bucket, for example, before actually starting the processing. 

PodSpec allow you to **define init containers** and also use volumes like we did in the previous example.

```
    podspec:
      initContainers:
      - name: init-py
        image: fission/python-env 
        command: ['sh', '-c', 'cat /etc/infopod/labels']
        volumeMounts:
          - name: infopod
            mountPath: /etc/infopod
            readOnly: false
      volumes:
        - name: infopod
          downwardAPI:
            items:
              - path: "labels"
                fieldRef:
                  fieldPath: metadata.labels
```

We can see that the init container is run first, before the actual function container is run:

```
$ kgpo $ff
NAME                                               READY     STATUS            RESTARTS   AGE
poolmgr-python-default-9eik2gxd-6fdc8d9696-hkkgn   0/2       Init:0/1          0          10s
poolmgr-python-default-9eik2gxd-6fdc8d9696-lpmgl   0/2       PodInitializing   0          10s
poolmgr-python-default-9eik2gxd-6fdc8d9696-tkmdc   0/2       PodInitializing   0          10s
```

And the init container here is simply printing the file which was mounted and we can verify the same by looking at logs of the init container:

```
$ k logs $ff poolmgr-python-default-9eik2gxd-6fdc8d9696-lpmgl -c init-py
environmentName="python"
environmentNamespace="default"
environmentUid="68e3f909-3e86-11e9-9378-42010aa00057"
executorInstanceId="dqaukdxy"
executorType="poolmgr"
pod-template-hash="2987485252"

```


## Sidecar for functions

You can also **add a sidecar** to the function container with PodSpec:

```
    podspec:
      # A container which will be merged with for pool manager
      Containers:
      - name: nodep
        image: fission/node-env
        volumeMounts:
          - name: funcvol
            mountPath: /etc/funcdata
            readOnly: true
      # A additional container in the pods
      - name: yanode
        image: fission/node-env
        command: ['sh', '-c', 'sleep 36000000000']
```        


## Many More!

The examples above are only the tips of the iceberg for what your functions can do with PodSpec. 

Here are some additional ideas for how you can use PodSpec to enhance your function pods:

- You can add a **custom scheduler** to be used for specific functions.
- Additional security policies and settings can be set with **security context** field in PodSpec.
- Introduced in Kubernetes 1.11 **readiness gates** allow extra feedback to the pod status and enable advanced mechanism to signal to Kubernetes that the pod can now serve production traffic.
- **Priority and priority Class Name** are used with a custom admission controller so you can set the priorities of the pods and effectively allocate resources to pods/functions with higher priority.
- **Node selector** allows scheduling function pods on specific nodes of the cluster.
- **Image Pull Secrets** will enable using private registries for all your images!

### Final thoughts

PodSpec is extremely powerful and extends the functionality of serverless functions for a wide variety of use cases and user needs. We have some exciting things we want to try with these new features, keep an eye out for new tutorials and hacks for using PodSpec with Fission functions.

**_Author:_**

* [Vishal Biyani](https://twitter.com/vishal_biyani)  **|**  [Fission Contributor](https://github.com/vishal-biyani)  **|**  CTO - [Infracloud Technologies](http://infracloud.io/)
