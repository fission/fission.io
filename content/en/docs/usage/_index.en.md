---
title: "Usage"
weight: 5
description: >
  Build, run, and operate functions on Fission day to day.
---

This section is the hands-on guide to using Fission once it is installed on your cluster.
Each page is task-oriented: it states what you will accomplish, lists the commands to run, and shows the output to expect.

If you have not installed Fission yet, start with the [Installation guide]({{% ref "/docs/installation/_index.en.md" %}}).
For the concepts behind these tasks, see [Concepts]({{% ref "/docs/concepts/_index.md" %}}).

## Guide map

Work through the function workflow in roughly this order:

* [Create an environment]({{% ref "function/environments.en.md" %}}) — register a language runtime (NodeJS, Python, Go, and more) so Fission can run your code.
* [Create a function]({{% ref "function/functions.en.md" %}}) — deploy code, add an HTTP route, and test, update, and inspect functions.
* [Package source code]({{% ref "function/package.en.md" %}}) — build functions from source archives or ship pre-built deployment packages.
* [OCI image packages]({{% ref "function/oci-packages.md" %}}) — ship function code as an OCI image instead of an archive, with cache-friendly cold starts.
* [Control function execution]({{% ref "function/executor.en.md" %}}) — choose an executor (poolmgr, newdeploy, or container) and tune scaling, concurrency, and cold starts.
* [Run a container as a function]({{% ref "function/container-functions.md" %}}) — turn any existing container image into a Fission function.
* [Access secrets and ConfigMaps]({{% ref "function/access-secret-cfgmap-in-function.en.md" %}}) — read Kubernetes Secrets and ConfigMaps from inside a function.
* [Access URL parameters]({{% ref "function/accessing-url-params.md" %}}) — read path parameters from REST-style routes.
* [Canary deployments]({{% ref "function/canary-deployments.md" %}}) — roll out a new function version gradually and roll back automatically on failure.

Durable and asynchronous execution:

* [Asynchronous invocation]({{% ref "function/async-invocation.md" %}}) — invoke a function fire-and-forget with a durable id, background retries, a dead-letter queue, and result destinations.
* [Workflows]({{% ref "workflows/_index.md" %}}) — orchestrate several functions as one durable, resumable state machine with parallelism, retries, and durable waits.

Operational and advanced topics:

* [Stream function responses]({{% ref "function/streaming.md" %}}) — return SSE, chunked, or WebSocket responses incrementally for LLM tokens, chat, and long-running calls.
* [Expose functions as MCP tools]({{% ref "function/mcp-tools.md" %}}) — let LLM agents discover and invoke functions over the Model Context Protocol.
* [Expose functions with the Gateway API]({{% ref "gateway-api/_index.md" %}}) — route external traffic through a Kubernetes Gateway (the successor to Ingress).
* [Multi-namespace tenancy]({{% ref "multi-namespace-tenancy.md" %}}) — onboard and offboard namespaces at runtime with `fission tenant enable`/`disable`, each isolated by its own keys and RBAC.
* [Pull from a private registry]({{% ref "function/private-registry.md" %}}) — authenticate image pulls with an `imagePullSecret` when an environment image lives in a private registry.
* [Use a URL as an archive source]({{% ref "function/url-as-archive-source.md" %}}) — embed a remote URL directly in a package archive instead of uploading the file, for faster, more portable package creation.
* [Enable Istio on Fission]({{% ref "function/enabling-istio-on-fission.md" %}}) — install Fission alongside the Istio service mesh with sidecar injection enabled.

For reproducible, version-controlled deployments, also read about the [spec-based workflow]({{% ref "/docs/usage/spec/_index.md" %}}) and how to [deploy from CI/CD]({{% ref "cicd.md" %}}).
