+++
title = "Setting Ingress for your Functions"
date = "2019-10-28T22:09:38+08:00"
author = "Ta-Ching Chen"
description = "How to use ingress with TLS for Fission functions"
categories = ["Fission"]
type = "blog"
+++

Some exciting updates to ingress host path, annotations, and TLS support.
In Fission version 1.6.0, which was released on Friday 11 October 2019, new features arrived. This blogpost covers the exciting updates to ingress host path, annotations, and TLS support.

Fission previously supported ingress. However, it lacked support for TLS, host field, and ingress annotations. Now with version 1.6, all three are supported.

In this blog post, we will cover all three of the new features. But first, let's talk about ingress some more.

What is ingress?
Ingress exposes HTTP and HTTPS routes from outside of the Kubernetes cluster to services located within the cluster.

An ingress object can be configured to give services externally-reachable URLs, load balance traffic, terminate TLS, and can offer name-based virtual hosting.
An ingress controller is responsible for fulfilling the ingress object.

Check below for an example deployment.

```
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: sample-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /testpath
        backend:
          serviceName: ingress
          servicePort: 80
```

To learn more about Kubernetes ingress check out [this link](https://kubernetes.io/docs/concepts/services-networking/ingress/)

# Ingress host rule

You can enable ingress host rule by adding `--ingressrule` to your fission route command. 
The format to use is `host=path`. You have to provide both the host and the endpoint path. 
You can allow access from all hosts by providing an astrix as the host like:

``` 
--ingressrule "*=/foobar" 
```

You can also specify specific hosts by providing the name like:

```
--ingressrule "example.com=/foobar"
```

Command example:

```
$ fission route create --name foobar --method GET \
    --function nodejs --url "/foobar" --createingress --ingressrule "*=/foobar"
```

# Ingress annotations

You can now specify annotations to ingress when creating the HTTP trigger.
To use ingress annotations, --ingressannotation needs to be added when creating or updating a fission route.

If you, for example, want to disable TLS auto-redirect and enable regular expressions. You have to use the following command:

```
$ fission route create --name foo --url /foo --function foofn --createingress \
    --ingressannotation "nginx.ingress.kubernetes.io/ssl-redirect=false" \
    --ingressannotation "nginx.ingress.kubernetes.io/use-regex=true"
```

# Ingress TLS

To enable this, you first have to create a secret that contains the TLS private key and the certificate.
To enable ingress TLS, `--ingresstls` needs to be added when creating or updating a fission route.

Command example:
```
$ fission route create --name foo --url /foo/{bar} --function foofn --createingress \
    --ingressannotation "nginx.ingress.kubernetes.io/ssl-redirect=false" \
    --ingressannotation "nginx.ingress.kubernetes.io/use-regex=true" \
    --ingressrule "*=/foo/*" --ingresstls "foobartls"
```

Fission 1.6.0 added a lot of other cool features as well. Check out the [full changelog](https://github.com/fission/fission/blob/master/CHANGELOG.md#change-log) 
or go directly to the [release page](/docs/releases/1.6.0/) here.