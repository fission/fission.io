---
title: "Exposing Functions With Ingress"
linkTitle: Ingress
draft: false
weight: 60
description: >
  Expose a Fission function outside the cluster on an FQDN using an NGINX ingress controller and Fission's route with --createingress.
---

{{% alert title="Deprecated — use the Gateway API" color="warning" %}}
The Kubernetes Ingress API is frozen, and Fission's `--createingress` flow is **deprecated**.
For new functions, prefer [Exposing Functions With the Gateway API]({{% ref "../gateway-api/" %}}) — its official successor — available since **Fission v1.26.0**.
The Ingress flow documented below keeps working for the deprecation window; see [Migrating from Ingress]({{% ref "../gateway-api/_index.md#migrating-from-ingress" %}}) when you are ready to switch.
{{% /alert %}}

**This tutorial exposes a Fission function on a public FQDN using an NGINX ingress controller and Fission's route with `--createingress`.**

Ingress is a Kubernetes resource that routes traffic from outside the cluster to in-cluster services with the help of an ingress controller.
For background on ingress concepts, see the [Kubernetes ingress docs](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers); for other controllers besides NGINX, see the [list of ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/#additional-controllers).

## Setup & pre-requisites

You will need a Kubernetes cluster with Fission installed (Please check [installation page]({{% ref "../../installation/" %}}) for details).
This tutorial uses a cloud load balancer, but if you are using Minikube you might want [to take a look at details here](https://github.com/kubernetes/minikube/issues/496).

Later parts of this tutorial use an FQDN to reach the function.
If you plan to go along in this section, you will need a domain name setup and access to modify the NS records and create `A` record in the zone of the domain name you have.
The tutorial uses Google cloud to walk through the tutorial but you can use any cloud you prefer to.
Also the changes in name server can take 24-48 hours so you may want to use an already created domain name.

## Setup an Ingress Controller

This tutorial uses the NGINX ingress controller.
Choose [any installation method that fits your setup](https://kubernetes.github.io/ingress-nginx/deploy/).
The steps below should work with other ingress controllers too, but only NGINX has been tested.

Let's verify that the installation succeeded:

```bash
$ kubectl get all -n ingress-nginx
NAME                                           READY     STATUS    RESTARTS   AGE
po/default-http-backend-66b447d9cf-4q8f7       1/1       Running   0          19d
po/nginx-ingress-controller-58fcfdc6fd-2cwts   1/1       Running   0          19d

NAME                       CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGE
svc/default-http-backend   10.11.243.109   <none>           80/TCP                       19d
svc/ingress-nginx          10.11.245.254   35.200.150.175   80:31000/TCP,443:30666/TCP   19d

NAME                              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deploy/default-http-backend       1         1         1            1           19d
deploy/nginx-ingress-controller   1         1         1            1           19d

NAME                                     DESIRED   CURRENT   READY     AGE
rs/default-http-backend-66b447d9cf       1         1         1         19d
rs/nginx-ingress-controller-58fcfdc6fd   1         1         1         19d

```

Validate the installation against the output above:

- The ingress controller pod is up and running
- The ingress-nginx service has an external IP address populated
- If you hit the external IP address of the ingress-nginx, you get the default backend page:

```bash
$ curl http://35.200.150.175

default backend - 404
```

## Deploying Function with ingress

With the ingress controller running, the next steps create a function and expose it through an ingress resource.

## Create a function

We will create an environment, a function and test that it works:

```bash
$ fission env create --name nodejs --image ghcr.io/fission/node-env
environment 'nodejs' created

$ cat hello.js
module.exports = async function(context) {
    return {
        status: 200,
        body: "Hello, Fission!\n"
    };
}

$ fission fn create --name hello --env nodejs --code hello.js 
function 'hello' created

$ fission fn test --name hello
Hello, Fission!
```

## Create an internal route

Let's create a route which is not exposed via the ingress controller so that it can be consumed by resources inside the cluster only.

Functions are currently also exposed via the Fission router, so this route is reachable from outside the cluster today — but the router may stop exposing all functions externally in future versions.

```bash
$ fission route create --url /ihello --function hello
trigger '249838c9-9ae3-492a-bba1-b0464ae65671' created

$ fission route list
NAME                                 METHOD HOST URL     INGRESS FUNCTION_NAME
249838c9-9ae3-492a-bba1-b0464ae65671 GET         /ihello false   hello
```

This route is accessible at `http://$FISSION_ROUTER/ihello`, but accessing it on the ingress controller address `http://<INGRESS-CONTROLLER-EXTERNAL-IP>/ihello` returns the default backend page.
This is expected, since we did not create an ingress for this route.

## Create an external route

Now let's create a route exposed over the ingress controller, using the `createingress` flag:

```bash
$ fission route create --url /hello --function hello --createingress --ingressannotation "kubernetes.io/ingress.class=nginx"
trigger '301b3cb0-5ac1-4211-a1ed-2b0ad9143e34' created
```

{{% notice info %}}
The `kubernetes.io/ingress.class` annotation is deprecated in modern Kubernetes in favor of the `spec.ingressClassName` field on the Ingress resource and a corresponding `IngressClass` object.
Most controllers still honor the annotation for backward compatibility, but check your controller's documentation — for the NGINX controller you can instead create an `IngressClass` named `nginx` and rely on it as the cluster default.
{{% /notice %}}

```bash
$ fission route list
NAME                                 METHOD HOST URL     INGRESS FUNCTION_NAME
249838c9-9ae3-492a-bba1-b0464ae65671 GET         /ihello false   hello
301b3cb0-5ac1-4211-a1ed-2b0ad9143e34 GET         /hello  true    hello
```

If you check the ingress controller pod logs, you will notice that the ingress controller has re-loaded the configuration for the newly created ingress resource:

```text
I0604 12:47:08.983567       5 controller.go:168] backend reload required
I0604 12:47:08.985535       5 event.go:218] Event(v1.ObjectReference{Kind:"Ingress", Namespace:"fission", Name:"301b3cb0-5ac1-4211-a1ed-2b0ad9143e34", UID:"64bffe8c-67f5-11e8-98e8-42010aa00018", APIVersion:"extensions", ResourceVersion:"18017617", FieldPath:""}): type: 'Normal' reason: 'CREATE' Ingress fission/301b3cb0-5ac1-4211-a1ed-2b0ad9143e34
I0604 12:47:09.117629       5 controller.go:177] ingress backend successfully reloaded...
```

If you now hit the function at the ingress controller's IP and the path (`http://<INGRESS-CONTROLLER-EXTERNAL-IP>/hello`), you get the function's response.
Depending on your setup, try HTTP or HTTPS — some ingress controllers enable SSL redirect by default, so you may need the HTTPS URL.

```bash
$ curl -k  https://35.200.150.175/hello
Hello, Fission!
```

## Create an FQDN route

This step is optional and requires the DNS pre-requisites from the setup section above.
Map the FQDN to the function with the following steps:

- Map the domain name's name server to your cloud provider.
  For example we used domain name fission.sh and mapped the name server to google cloud (Since this tutorial setup is on Google cloud).
  The instructions are specific to your domain name provider, please check the documentation of the provider.

- Create a zone for the root domain in the cloud provider (we created a zone for fission.sh in Google Cloud).

- Create a sub-domain A record that maps to the IP address of the ingress controller load balancer.
  In this tutorial we created an A record in the zone above for `ing.fission.sh` and pointed it to the IP of the ingress controller load balancer, `35.200.150.175` (A records can take 30 minutes to 4 hours to update).

- Once these steps are configured, the function is reachable at the FQDN below:

```bash
$ curl -k  https://ing.fission.sh/hello
Hello, Fission!
```
