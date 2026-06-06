---
title: "Controller"
weight: 13
description: >
  Deprecated REST API server — clients now talk directly to the Kubernetes API server and Fission CRDs.
---

{{% notice warning %}}
The Controller is deprecated and is no longer part of the Fission architecture.
It was deprecated in 1.18.0 and removed from the default install in 1.20.0.
This page is kept for reference and migration guidance only.
{{% /notice %}}

The Controller was a standalone REST API server that the Fission CLI used to talk to.
It exposed CRUD endpoints for Fission resources and proxied requests to internal services.

Every Fission resource has always been stored as a [Kubernetes Custom Resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/), so the Controller was an extra hop in front of the Kubernetes API server.
That hop has been removed.

## What replaced it

The Fission CLI and all Fission components now talk to the Kubernetes API server directly.
You create, read, update, and delete Fission resources as native CRDs, and the API server handles authentication, authorization (RBAC), and validation.

Validation that the Controller used to perform now runs at the API server through [CEL rules]({{% ref "webhook.md" %}}) on the CRDs and a focused [admission webhook]({{% ref "webhook.md" %}}).

The Helm chart no longer has a `controller.enabled` flag — the component was removed entirely, not merely disabled by default.

## Migration

If you have tooling or scripts that called the old Controller REST endpoints, switch them to the Kubernetes API.

- Use the `fission` CLI for everyday operations.
  It speaks to the Kubernetes API server using your kubeconfig.
- Use `kubectl` (or any Kubernetes client) to manage Fission resources as CRDs directly — for example `kubectl get functions.fission.io` or `kubectl apply -f function.yaml`.
- Apply Kubernetes RBAC to Fission CRDs to control who can manage which resources.

## Related

- [Architecture overview]({{% ref "_index.md" %}}) — the current set of Fission components.
- [Admission Webhook]({{% ref "webhook.md" %}}) — how Fission resources are validated today.
- [Reconcilers]({{% ref "reconcilers.md" %}}) — how components act on the CRDs you create.
