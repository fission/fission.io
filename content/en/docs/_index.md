---
title: "Fission"
linkTitle: Docs
weight: 20
description: >
  Serverless Functions for Kubernetes
---

## What is Fission?

Fission is a fast, open source serverless framework for Kubernetes with a focus on developer productivity and high performance.
You write a function in your language of choice, and Fission runs it on Kubernetes without you building containers or managing deployments.
Docker and Kubernetes are abstracted away under normal operation, though you can use both to extend Fission when you need to.

Fission keeps a pool of warm containers ready, so functions typically cold-start in around 100msec.
It supports NodeJS, Python, Go, Ruby, PHP, Bash, and any custom container image, with language-specific runtimes isolated in components called _environments_.

## Learning path

These docs are organized as a path from your first function to production operation.
Follow them in order, or jump to the section you need.

- **[Getting Started]({{% ref "/docs/getting-started/_index.md" %}})** — install Fission and run your first function in five minutes.
- **[Concepts]({{% ref "/docs/concepts/_index.md" %}})** — the mental model: functions, environments, packages, and triggers, and how they fit together.
- **[Installation]({{% ref "/docs/installation/_index.en.md" %}})** — production installs, managed-cluster options, authentication, and installing without Helm.
- **[Usage]({{% ref "/docs/usage/_index.en.md" %}})** — task guides for building functions in each language, wiring triggers, observability, and shipping with specs.
- **[Architecture]({{% ref "/docs/architecture/_index.md" %}})** — how the router, executor, builder, and other components work together inside the cluster.
- **[Reference]({{% ref "/docs/reference/_index.md" %}})** — generated reference for the Fission CLI, custom resources, metrics, and a glossary of terms.

## Examples and community

Browse ready-to-run functions in the [Fission Examples repo](https://github.com/fission/examples/).
Have a question or want to contribute?
[Join the Fission Slack](/slack).
