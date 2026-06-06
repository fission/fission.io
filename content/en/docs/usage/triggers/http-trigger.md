---
title: "HTTP Trigger"
date: 2019-12-17T14:38:00+08:00
weight: 1
description: >
  Invoke functions over HTTP by mapping URL paths and methods to functions with fission httptrigger create, including URL path parameters.
---

An **HTTP trigger invokes a function when the router receives a matching HTTP request**.
You map a URL path and one or more HTTP methods to a function, and the router forwards matching requests to it.

## Create a basic trigger

Map `GET /hello` to the `hello` function:

```bash
$ fission httptrigger create --url /hello --method GET --function hello
trigger '94cd5163-30dd-4fb2-ab3c-794052f70841' created

$ curl http://$FISSION_ROUTER/hello
Hello World!
```

To send multiple methods to the same function, repeat `--method`:

```bash
$ fission httptrigger create --url /hello --method GET --method POST --function hello
```

{{% notice info %}}
`FISSION_ROUTER` is the externally-visible address of your Fission router service.
For how to set the `FISSION_ROUTER` environment variable, see [Accessing Fission environment variables]({{% ref "../../installation/env_vars.en.md" %}}).
{{% /notice %}}

{{% notice info %}}
To add authentication to your function calls, see the [Fission Authentication]({{% ref "../../installation/authentication.md" %}}) guide.
{{% /notice %}}

## URL parameters

Add placeholders to the `--url` value to capture path parameters:

```bash
$ fission httptrigger create --method GET \
    --url "/guestbook/messages/{id}" --function restapi-get
```

Fission uses [gorilla/mux](https://github.com/gorilla/mux) as the underlying URL router, so you can constrain a parameter with a regular expression to reject malformed requests:

```bash
$ fission httptrigger create --method GET \
    --url "/guestbook/messages/{id:[0-9]+}" --function restapi-get
```

{{% notice info %}}
To read URL parameters inside your function and build a REST API, see [Accessing URL parameters]({{% ref "../function/accessing-url-params.md" %}}).
{{% /notice %}}

## Prefix routing

Use `--prefix` to forward every request under a path to one function.
Prefix takes precedence over `--url`.
By default the prefix is stripped before the request reaches the function; pass `--keepprefix` to forward the full path instead.

```bash
$ fission httptrigger create --prefix /api --method GET --function api-gateway
```

## Path safety

{{% notice info %}}
As of Fission {{< release-version >}}, the URL path and prefix of an HTTP trigger are validated by both the `fission` CLI and the Kubernetes API server (via CEL `x-kubernetes-validations`).
A path must start with `/`, must not be root-only (`/`), and must not contain `..` traversal segments.
It also may not collide with router-owned paths (`/router-healthz`, `/readyz`, `/_version`, `/auth/login`) or shadow the router-internal `/fission-function/` prefix.
Because the rules now run in the API server, a trigger written via `kubectl apply` or GitOps is rejected just like one created with the CLI.
{{% /notice %}}

## Ingress

To expose an HTTP trigger through a Kubernetes Ingress, pass `--createingress` and set the host and path with `--ingressrule host=path`.
If you create an Ingress without a rule, the host defaults to `*`, a wildcard host.

```bash
$ fission httptrigger create --url /hello --method GET --function hello --createingress --ingressrule acme.com=/hello
trigger '94cd5163-30dd-4fb2-ab3c-794052f70841' created

$ fission route list
NAME                                 METHOD HOST     URL      INGRESS FUNCTION_NAME
94cd5163-30dd-4fb2-ab3c-794052f70841 GET    acme.com /hello   true    hello
```

You can attach annotations and TLS to the generated Ingress:

- `--ingressrule host=path` — set the Ingress host and path rule.
- `--ingressannotation key=value` — add an annotation (repeatable); the format depends on your Ingress controller.
- `--ingresstls secretName` — reference a Secret holding the TLS key and certificate.

For Ingress to work, you must deploy an Ingress controller in your cluster, for example:

- [NGINX Ingress Controller](https://github.com/kubernetes/ingress-nginx)
- [GCE Ingress Controller](https://github.com/kubernetes/ingress-gce)

Other controllers such as [F5](http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/v1.5/) and [Kong](https://konghq.com/blog/kubernetes-ingress-controller-for-kong/) also work.

## Related

- [Triggers overview]({{% ref "_index.md" %}})
- [Accessing URL parameters]({{% ref "../function/accessing-url-params.md" %}})
- [Router architecture]({{% ref "/docs/architecture/router.md" %}})
