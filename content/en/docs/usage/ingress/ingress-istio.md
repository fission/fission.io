---
title: "Istio as Ingress"
weight: 2
description: "Learn how to use Istio as Ingress with Fission."
---

**Use Istio as an ingress gateway to control traffic, routing, and access to your Fission functions.**

Istio is a popular open source service mesh that manages microservices and the communication between them.
It offers features for traffic management, security, observability, and extensibility.

## Pre-requisites

You need Istio installed on your cluster.
Based on your setup, choose one of the available ways to [install Istio](https://istio.io/latest/docs/setup/install/).

To install Fission, see [Fission Installation](/docs/installation).
Set the `enableIstio` flag to `true` during the setup to enable Istio in Fission.

```bash
helm install --version {{% release-version %}} --namespace fission \
  --set serviceType=NodePort,routerServiceType=NodePort \
  --set enableIstio=true \
  fission-charts/fission-all
```

Enable `istio-injection` for the fission namespace:

```bash
kubectl label namespace fission istio-injection=enabled
```

At this point, Fission is installed with Istio sidecar injection enabled.

This guide uses the [Single vs Monolith](https://fission.io/blog/single-or-monolith-serverless-functions-what-should-you-choose/) example throughout.
Clone it from the [examples repository](https://github.com/fission/examples/tree/main/python/SinglevsMonolith).

## Configure Istio Gateway

Istio provides extensive options to control the flow of traffic and API calls between services.
While it supports Kubernetes Ingress, Istio offers an **Istio Gateway** that provides more customization and flexibility than Ingress.
The [Istio Gateway](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/) controls traffic entering your cluster using Istio routing rules.

Before creating and deploying the Istio gateway, determine the ingress IP and ports.

```bash
kubectl get svc istio-ingressgateway -n istio-system
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                      AGE
istio-ingressgateway   LoadBalancer   10.106.99.144   <pending>     15021:30487/TCP,80:31638/TCP,443:32533/TCP   5d3h
```

> If the `EXTERNAL-IP` is set, your environment has an external load balancer that you can use for ingress gateway. If the value is `<none>` or `<pending>` then your environment doesn't provide an external load balancer. In such situations, you can access the gateway using Node Port.

In this case, the system doesn't provide an external load balancer, so we'll configure the Ingress Host and Ingress Ports accordingly.

### Setting Ingress Ports

```bash
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
```

### Setting Ingress Host

The steps to set up an Ingress host vary from provider to provider depending on your architecture.
Refer to the [Istio Gateway documentation](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/#determining-the-ingress-ip-and-ports) to configure the host.

In our setup, we have used the minikube IP address as the `$INGRESS_HOST`.

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

Since this setup uses Minikube, configure Minikube to forward traffic to the Istio gateway by running `minikube tunnel` in a separate terminal window.

The gateway above allows traffic only on port 80 over HTTP.
Test it by navigating to `http://$INGRESS_HOST:$INGRESS_PORT/main` in a browser to view your application.

At this point, all external traffic entering the Istio service mesh passes through the gateway you configured.

## Request Routing

Istio also supports **request routing** through a **Virtual Service**.
A Virtual Service lets you set the traffic percentage and destination for requests.

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

The `gateway` field must reference the Istio Gateway created in the earlier step.
The `http` match rule allows access only to `/main`, routing to the Fission router service `router.fission.svc.cluster.local`.


2. Deploy the configuration

```bash
kubectl apply -f virtualservice.yaml
```

After deploying the virtual service, visit the url from your browser.
Only the route defined in the yaml file is accessible; access to all other routes is blocked by default.
Internally, traffic comes in to the `gateway`, which forwards it to the host, `fission router` in this case.
The router then forwards it to the respective application based on the `routes` created.

### Add HTTP Fault Delay

Istio's traffic management also supports HTTP fault delays, useful for testing your application's resiliency.
Fault delays add a delay before a request is processed, helping you discover timeout-related issues.

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

To confirm this is working, open the url in a browser and navigate to `/main`.
The page takes longer to load because of the fault delay you added.

## Configuring Access To Functions

Configure an **Authorization Policy** to enable or disable access to specific routes.

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

After applying this configuration, accessing the `/getstock` path returns an error, because the `DENY` action applies to the `POST` method on that path.

See the [Istio Documentation](https://istio.io/latest/docs/) for the full range of Istio features you can use with Fission.