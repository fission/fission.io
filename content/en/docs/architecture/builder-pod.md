---
title: "Builder Pod"
weight: 7
description: >
  Where a function's source is compiled into a deployment archive
---

The builder pod is the per-environment workload that compiles a source archive into a deployment archive used by the [function pod]({{% ref "/docs/architecture/function-pod.md" %}}).

{{% notice info %}}
A builder pod exists only for environments that declare a builder image.
The [builder manager]({{% ref "/docs/architecture/buildermgr.md" %}}) creates one builder Deployment per such environment; deploy-only packages never touch a builder pod.
{{% /notice %}}

Each builder pod runs two containers that share a volume:

- **Builder container** — compiles the function source into an executable artifact; this container is language-specific and comes from the environment's builder image.
- **Fetcher** — a sidecar that downloads the source archive from [StorageSvc]({{% ref "/docs/architecture/storagesvc.md" %}}), verifies its checksum, and uploads the resulting deployment archive back to StorageSvc after the build.

## Build pipeline

```mermaid
sequenceDiagram
  participant bm as Builder Manager
  participant fetcher as Fetcher
  participant builder as Builder Container
  participant storage as StorageSvc
  bm->>fetcher: fetch source archive
  fetcher->>storage: download source archive
  fetcher->>fetcher: verify checksum, write to shared volume
  bm->>builder: build (build command)
  builder->>builder: read source, compile to deployment archive
  builder->>builder: write artifact to shared volume
  bm->>fetcher: upload deployment archive
  fetcher->>storage: upload deployment archive
  fetcher-->>bm: archive URL + checksum
```

The build command is taken from the package's `spec.buildcmd` when set, otherwise from the environment's `builder.command`.
The shared volume is how the fetcher hands the source to the builder and the builder hands the artifact back to the fetcher.
The fetcher exposes its API on port `8000` and the builder container on port `8001`.

## Security: no service-account token in the builder container

As of Fission {{< release-version >}} the builder pod no longer auto-mounts the `fission-builder` ServiceAccount token into every container.
The pod sets `automountServiceAccountToken: false`, and the token is re-mounted only on the fetcher sidecar via a projected volume — the user-supplied builder container does not receive it (GHSA-8wcj-mfrc-jx5q).
This prevents untrusted build code from reading the builder ServiceAccount credentials.

## Related

- [Builder Manager]({{% ref "/docs/architecture/buildermgr.md" %}}) — orchestrates the build and updates package status.
- [StorageSvc]({{% ref "/docs/architecture/storagesvc.md" %}}) — stores the source and deployment archives.
- [Function Pod]({{% ref "/docs/architecture/function-pod.md" %}}) — consumes the deployment archive at runtime.
