---
title: "Compatibility"
weight: 70
description: >
  Kubernetes and KEDA versions supported by each Fission release
---

**This page maps each Fission release to the Kubernetes and KEDA versions it is built and tested against.**
Use it to confirm your cluster meets a release's floor before you [install]({{% ref "_index.en.md" %}}) or [upgrade]({{% ref "upgrade.md" %}}).

## Kubernetes compatibility

Each Fission release pins a `k8s.io/api` version in its `go.mod`; the minor of that dependency tracks the Kubernetes server version Fission is built against.
The **Tested with** column lists the `kindest/node` images each release's CI runs its end-to-end suite on, which is the most reliable signal of what works in practice.

| Fission version | Built against (`k8s.io/api`) | Tested with (kind) | Minimum Kubernetes |
| --------------- | ---------------------------- | ------------------ | ------------------ |
| {{< release-version >}} | v0.36 | 1.32, 1.34, 1.36 | **1.32** |
| v1.24.0 | v0.35 | 1.28, 1.32, 1.34 | 1.28 |
| v1.23.0 | v0.35 | 1.28, 1.32, 1.34 | 1.28 |
| v1.22.0 | v0.34 | 1.28, 1.32, 1.34 | 1.28 |
| v1.21.0 | v0.32 | 1.28, 1.30, 1.32 | 1.28 |
| v1.20.0 | v0.28 | 1.23, 1.25, 1.27 | 1.23 |
| v1.19.0 | v0.25 | 1.19, 1.20, 1.21 | 1.19 |
| v1.18.0 | v0.25 | 1.19, 1.20, 1.21 | 1.19 |
| v1.17.0 | v0.25 | 1.19, 1.20, 1.21 | 1.19 |

{{% notice info %}}
Starting with {{< release-version >}} the chart enforces `kubeVersion: ">=1.32.0-0"`, so `helm install` fails fast on an older cluster.
Earlier releases did not carry a `kubeVersion` constraint; the **Minimum Kubernetes** column above is the oldest version that release's CI exercised.
{{% /notice %}}

## KEDA compatibility

Fission's [KEDA-backed message-queue triggers]({{% ref "../usage/triggers/message-queue-trigger-kind-keda/_index.md" %}}) require a compatible KEDA install in the cluster.
From v1.21.0 onward, KEDA is a direct Go dependency of Fission and the table below reflects the version each release builds and tests against.

| Fission version | KEDA version |
| --------------- | ------------ |
| {{< release-version >}} | v2.20 |
| v1.24.0 | v2.19 |
| v1.23.0 | v2.18 |
| v1.22.0 | v2.18 |
| v1.21.0 | v2.16 |

For releases before v1.21.0, the KEDA integration shipped through connector images rather than a pinned Go dependency.
Check the [release notes]({{% ref "../releases/_index.en.md" %}}) for the exact connector tags those versions used.

{{% notice info %}}
To see the exact connector image tags bundled with your installed chart, run:

```console
helm show values --version {{< chart-version >}} fission-charts/fission-all
```
{{% /notice %}}

## Language environments

Each language environment (NodeJS, Python, Ruby, Go, PHP, Java/JVM, Bash) is versioned independently of Fission itself.
Track the current image tags on the [environments page](/environments/).

## Related

- [Installing Fission]({{% ref "_index.en.md" %}})
- [Upgrade Guide]({{% ref "upgrade.md" %}})
- [Release notes]({{% ref "../releases/_index.en.md" %}})
