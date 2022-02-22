+++
title = "Function builders also support PodSpec now"
date = "2019-11-01T12:39:32+05:30"
image = "/images/2020/builder.jpg"
author = "Vivek Singh"
description = "Using PodSpec with Fission buider for function deployment artifact"
categories = ["Fission"]
type = "blog"
+++

In a previous [post](/blog/functions-on-steroids-with-podspec/) we discussed about how we can leverage `PodSpec` in the environment pods to enable the functionalities like tolerations, nodeSelectors, volumes, security and a lot others. That functionality was only supported in the environment pods, but now we can provide the `podspec` in the builder pods as well. The details about what `PodSpec` is and the functionalities that it enables are described in the mentioned post. 

In this post we will be looking into how do we use `PodSpec` in builder so that the deployment that will be created for the builder will have `podspec` that we mention in the environment for builder. If we take a look at below environment spec
{{< highlight "yaml" >}}
apiVersion: fission.io/v1
kind: Environment
metadata:
  creationTimestamp: null
  name: python-env
  namespace: default
spec:
  builder:
    command: build
    image: fission/python-builder
  keeparchive: false
  poolsize: 3
  resources: {}
  runtime:
    image: fission/python-env
  terminationGracePeriod: 360
  version: 2
{{< /highlight  >}}

 
We can see that for builder we are just specifying the command and image, and if we look into the pod that will be created, if we apply this spec, it will only have standard `podspec` that will be set by Fission itself.

## Using NodeSelector in builder podspec
Now assume that you want the builder pod for this Fission environment to only get scheduled on the machine that has some label, let's say `machinecap=high`, till now there was no way to do that but now you can have `Podspec` in the builder itself to achieve the same. Now let's have a look at the environment spec below

{{< highlight "yaml" >}}
apiVersion: fission.io/v1
kind: Environment
metadata:
  creationTimestamp: null
  name: py-builder
  namespace: default
spec:
  builder:
    command: build
    image: fission/python-builder
    container: 
      command: ["sleep", "1"]
    podspec:
      containers:
      - name: containertwo 
        image: nginx 
      nodeSelector: 
        machinecap: high 
  keeparchive: false
  poolsize: 3
  resources: {}
  runtime:
    image: fission/python-env
    terminationGracePeriod: 360
  version: 2
{{< /highlight  >}}

You can see that for builder we are now specifying the `podspec` and in that we can have almost everything that is supported in kubernetes [PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#pod-v1-core) specification, for example to satisfy our requirement to schedule the builder pod only on the nodes that have label `machinecap=high` we have introduced [nodeSelector](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector) in the builder `podspec` that takes care of this requirement.
Now if we create this environment, using `fission spec apply` and check the builder pod that has been created, we will be able to see that it has nodeSelector in its `podSpec`.
{{< highlight "yaml" >}}
spec:
  nodeSelector:
    machinecap: high
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: fission-builder
  serviceAccountName: fission-builder
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
{{< /highlight >}}

I am running this example on a cluster that is provisioned through minikube and if I check the status of that pod we see that the pod is in `Pending` state  
```
# kubectl describe pod -n fission-builder py-builder-1971419-6dd5658569-c88tc

Events:
  Type     Reason            Age              From               Message
  ----     ------            ----             ----               -------
  Warning  FailedScheduling  7s (x5 over 6m)  default-scheduler  0/1 nodes are available: 1 node(s) didn't match node selector.

```
you might have guessed that this is because we have mentioned the `nodeSelector` in the environment spec but we don't have any node in the cluster that has this label already set. If we want this pod to be running on the minikube node that we have, we will have to set the label in the minikube node, let's try to do that and then check the status 
```
# kubectl get pods -n fission-builder 
NAME                                  READY   STATUS    RESTARTS   AGE
py-builder-1971419-6dd5658569-c88tc   0/3     Pending   0          10m

# kubectl label nodes minikube machinecap=high
node/minikube labeled

# kubectl get pods -n fission-builder 
NAME                                  READY   STATUS    RESTARTS   AGE
py-builder-1971419-6dd5658569-c88tc   2/3     Running   0          10m
```

So, as you can see in the example given we can now provide `podspec` for builder while creating an environment, which enables us a lot of new functionality. 

## Using tolerations in builder podspec 
Let's take another example, we will now taint the node minikube and then try to provide toleration in the pods to get it successfully scheduled on the minikube node. Set the tain on the node using below command
```
# kubectl taint node minikube env=prod:NoSchedule
node/minikube tainted
```
and if we apply the same environment spec once again and check the builder pod that is created, you will be able to see that in `Pending` state
```
# kubectl get pods -n fission-builder
NAME                                  READY   STATUS    RESTARTS   AGE
py-builder-1973401-6f847c9448-nkg5b   0/3     Pending   0          10s
```
and describing it will tell us that the node has taint that this builder pod doesn't tolerate
```
# kubectl describe po -n fission-builder py-builder-1973401-6f847c9448-nkg5b
Events:
  Type     Reason            Age                 From               Message
  ----     ------            ----                ----               -------
  Warning  FailedScheduling  39s (x3 over 115s)  default-scheduler  0/1 nodes are available: 1 node(s) had taints that the pod didn't tolerate.

```

Now let's go ahead and try to create the builder pod with the tolerations set, change the environment spec like the file given below 
{{< highlight "yaml" >}}
apiVersion: fission.io/v1
kind: Environment
metadata:
  creationTimestamp: null
  name: py-builder
  namespace: default
spec:
  builder:
    command: build
    image: fission/python-builder
    container: 
      command: ["sleep", "1"]
    podspec:
      containers:
      - name: containertwo 
        image: nginx 
      tolerations:
      - key: "env"
        value: "prod"
        operator: "Equal" 
        effect: "NoSchedule"
      nodeSelector: 
        machinecap: high 
  keeparchive: false
  poolsize: 3
  resources: {}
  runtime:
    image: fission/python-env
    terminationGracePeriod: 360
  version: 2
{{< /highlight >}}

You can see that we are setting `tolerations` for builder pod in the environment spec. Let's apply this environment spec and check if the pod is scheduled on `minikube` node successfully.
```
# kubectl get pod -n fission-builder   
NAME                                  READY   STATUS    RESTARTS   AGE
py-builder-1974124-865f5fd498-2m9sn   2/3     Running   0          16s
```
Describing the pod will let you know that the pod now has been created with the correct tolerations that we have specified for builder in the environment spec.

**_Author:_**

* [Vivek Singh](https://viveksingh.dev)  **|**  Software Engineer - [InfraCloud Technologies](http://infracloud.io/)
