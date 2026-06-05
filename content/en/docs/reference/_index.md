---
title: "Reference"
weight: 9
description: >
  Generated reference material: the Fission CLI, custom resources, metrics, and a glossary of terms.
---

This section is the lookup desk for Fission.
Most pages here are generated directly from the {{< release-version >}} source, so they track the product exactly rather than describing how it once behaved.

Reach for reference material when you already know what you want to do and just need the precise flag, field, or metric name.
For task walkthroughs and explanations, start in [Usage]({{% ref "/docs/usage/_index.en.md" %}}) or [Concepts]({{% ref "/docs/concepts/_index.md" %}}) instead.

## What you'll find here

- **[Fission CLI]({{% ref "/docs/reference/fission-cli/_index.md" %}})** — every `fission` command, subcommand, and flag.
  These pages are generated from the CLI's own help output, so they always match the binary you installed.
- **[CRD reference]({{% ref "/docs/reference/crd-reference.md" %}})** — the full field-level schema for every Fission custom resource (Function, Environment, Package, and the trigger kinds), generated from the Go API types.
- **[Metrics reference]({{% ref "/docs/reference/metrics-reference.md" %}})** — the Prometheus metrics each Fission component exposes, with labels and descriptions.
- **[Glossary]({{% ref "/docs/reference/glossary.md" %}})** — short definitions for the terms used across these docs, from *archive* to *time trigger*.

{{% notice info %}}
The CLI, CRD, and metrics pages are auto-generated from the Fission source.
Edit the product, not these pages — they are regenerated on every release.
{{% /notice %}}
