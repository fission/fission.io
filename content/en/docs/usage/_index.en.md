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
* [Control function execution]({{% ref "function/executor.en.md" %}}) — choose an executor (poolmgr, newdeploy, or container) and tune scaling, concurrency, and cold starts.
* [Run a container as a function]({{% ref "function/container-functions.md" %}}) — turn any existing container image into a Fission function.
* [Access secrets and ConfigMaps]({{% ref "function/access-secret-cfgmap-in-function.en.md" %}}) — read Kubernetes Secrets and ConfigMaps from inside a function.
* [Access URL parameters]({{% ref "function/accessing-url-params.md" %}}) — read path parameters from REST-style routes.
* [Canary deployments]({{% ref "function/canary-deployments.md" %}}) — roll out a new function version gradually and roll back automatically on failure.

Operational and advanced topics:

* [Pull from a private registry]({{% ref "function/private-registry.md" %}})
* [Use a URL as an archive source]({{% ref "function/url-as-archive-source.md" %}})
* [Enable Istio on Fission]({{% ref "function/enabling-istio-on-fission.md" %}})

For reproducible, version-controlled deployments, also read about the [spec-based workflow]({{% ref "/docs/usage/spec/_index.md" %}}).
