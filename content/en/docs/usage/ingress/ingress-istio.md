---
title: "Istio as Ingress"
weight: 2
description: "Learn how to use Istio as Ingress with Fission."
---

Istio is one of the most popular open source service mesh.
It provides a platform to manage microservices and also facilitates communication between them.
It offers features for traffic management, security, observability and extensibility.
In this document, we shall look into how you can use Istio as Ingress with Fission.

## Pre-requisites

To begin with, you need to have Istio installed on your cluster.
There are multiple options to set up Istio and based on your setup, you can choose one of many ways available to [install Istio](https://istio.io/latest/docs/setup/install/).

To install Fission you can refer to [Fission Installation](/docs/installation).
Set the `enableIstio` flag as `true` during the setup to enable Istio in Fission

```bash
helm install --version {{% release-version %}} --namespace fission \
  --set serviceType=NodePort,routerServiceType=NodePort \
  --set enableIstio=true \
  fission-charts/fission-all
```

Enable `istio-injection` for fission namespace

```bash
kubectl label namespace fission istio-injection=enabled
```

At this point, you have fission installed along with Istio sidecar injection enabled.
Let us now look into various ways of using Istio with Fission.

For this entire documentation, we are going to use our [Single vs Monolith](https://fission.io/blog/single-or-monolith-serverless-functions-what-should-you-choose/) example.
You can clone it from our [examples repository](https://github.com/fission/examples/tree/main/python/SinglevsMonolith).

## Configure Istio Gateway

One of the features of Istio is its ability to let you easily control the flow of traffic and API calls between services.
It provides a lot of options to manage traffic coming in to your cluster.
While Istio supports Kubernetes Ingress, it offers an **Istio Gateway** that provides more customization and flexibility than Ingress.
[Istio Gateway](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/) brings in the flexibility and allows you to control the traffic coming in to your cluster.
All of this can be done using Istio routing rules.

But before we create and deploy our Istio gateway, we need to determine the ingress IP and ports.

```bash
kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                      AGE
istio-ingressgateway   LoadBalancer   10.106.99.144   <pending>     15021:30487/TCP,80:31638/TCP,443:32533/TCP   5d3h
```

> If the `EXTERNAL-IP` is set, your environment has an external load balancer that you can use for ingress gateway. If the value is `<none>` or `<pending>` then your environment doesn't provide an external load balancer. In such situations, you can access the gateway using Node Port.

In this case, the system doesn't provide an external load balancer, hence we will configure the Ingress Host and Ingress Ports accordingly

### Setting Ingress Ports

```bash
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
```

### Setting Ingress Host

The steps to set up an Ingress host varies from provider to provider depending on your architecture.
You can refer to the [Istio Gateway documentation](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/#determining-the-ingress-ip-and-ports) to configure the host.

In our setup, we have used minikube IP address as the `$INGRESS_HOST`

```bash
export INGRESS_HOST=$(minikube ip)`
```

1. Create an `Istio-Gateway`

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: gateway
spec:
  selector:
    istio: ingressgateway # use Istio default gateway implementation
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
```

2. Deploy the configuration

```bash
kubectl apply -f gateway.yaml
```

Since our setup uses Minikube, we need to configure Minikube to transfer traffic to the Istio gateway.
And in order to do that, you need to run `minikube tunnel` in a separate terminal window.

The above gateway contains only one rule that allows traffic on port 80 using HTTP protocol.
To test if your gateway is working or not, on a browser navigate to the url.
For example, navigate to `http://$INGRESS_HOST:$INGRESS_PORT/main` to view your application.

At this point, all the external traffic that enters the Istio Service mesh will be through the Istio gateway that we have configured.

## Request Routing

As discussed earlier, Istio allows extended configuration when it comes to traffic management.
One of them is **request routing** and this will be done using a **Virtual Service**.
With this you can set the traffic percentage and decide a destination to send the traffic to.

1. Create a `Virtual Service`

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: http
spec:
  hosts:
  - "*"
  gateways:
  - gateway
  http:
  - match:
    - uri:
        prefix: /main
    route:
    - destination:
        port:
          number: 80
        host: router.fission.svc.cluster.local
```

In the above file, notice the `gateway`, it should be the Istio Gateway that we created in the earlier step.
The http match rule allows access only to `/main` and the host is the fission router service `router.fission.svc.cluster.local`.


2. Deploy the configuration

```bash
kubectl apply -f virtualservice.yaml
```

After deploying the virtual service, visit the url from your browser.
You'll notice that you can access only the route mentioned in the yaml file, access to all other routes will be blocked by default.
Internally, the traffic comes in to the `gateway` which then forwards them to the host, `fission router` in this case.
The router then forwards it to the respective application based on the `routes` created.

### Add HTTP Fault Delay

As part of the Traffic Management services, Istio allows you to add an HTTP fault delay.
This comes handy when you want to test the resiliency of your application.
HTTP fault delays allow you to add delays before a request is processed, that way it'll help you discover timeout related issues.

1. Create a Fault Injection Rule to delay the incoming traffic

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: http
spec:
  hosts:
  - "*"
  gateways:
  - gateway
  http:
  - match:
    - uri:
        prefix: /main
    route:
    - destination:
        port:
          number: 80
        host: router.fission.svc.cluster.local
    fault:
      delay:
        fixedDelay: 7s
        percentage:
          value: 100
```

2. Deploy the configuration

```bash
kubectl apply -f virtualservice.yaml
```

To confirm if this is working as expected or not, open the url in a browser and navigate to the `/main` url.
You should observe that the page is taking longer to load and that's because of the fault delay that we've added.

## Configuring Access To Functions

In this section, we'll show you how to configure access to fission functions.
By the end of this, you'll be able to enable/disable access to certain routes based on your requirements.
To do this, we will configure an **Authorization Policy**.

1. Create an `Authorization Policy`

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: users-deny-all
  namespace: fission-function
spec:
  action: DENY
  rules:
  - to:
    - operation:
        methods: ["POST"]
        paths: ["/getstock"]
```

2. Deploy the configuration

```bash
kubectl apply -f authpolicy.yaml
```

After applying this configuration, you'll notice that you get an error while accessing the `/getstock` path.
This is because of the `DENY` action that is applied to the `POST` method on the path.

These were a few services offered by Istio that can be integrated with your Fission based applications.
You can refer to [Istio Documentation](https://istio.io/latest/docs/) to explore all the other things that you can do to leverage the full potential of Istio.