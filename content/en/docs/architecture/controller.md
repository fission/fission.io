---
title: "Controller"
weight: 2
description: >
  Accept REST API requests and create Fission resources
---

{{< notice info >}}
Controller is deprecated from version 1.18.0. You can still enable it using - `controller.enabled` flag in helm charts.
{{< /notice >}}

Controller is the component that the client talks to.
It contains CRUD APIs for functions, triggers, environments, Kubernetes event watches, etc. and proxy APIs to internal 3rd-party services.

All fission resources are stored in <a href="https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/" target="_blank">Kubernetes CRDs</a>.
It needs to be able to talk to Kubernetes API service.
To access CRDs in all namespaces, a service account with cluster-wide admin permission is used by Controller.

{{< img "../assets/controller.png" "Fig.1 Controller" "40em" "1" >}}

1. The clients send requests to the endpoints on Controller.
2. (A) Controller operates the CRDs based on the request.
3. (B) If a request is to another internal service, proxy the request to the service.

## API

See [here](https://github.com/fission/fission/blob/master/pkg/controller/api.go) for more details.

* `/v2/apidocs.json`: The OpenAPI 2.0 (Swagger) doc of all CRUD APIs for Fission CRDs.
* `/proxy/*`: The proxy APIs to internal services.
* `/v2/<resources>/*`: The CRUD APIs for Fission CRDs.
* `/healthz`: The health check endpoint.
