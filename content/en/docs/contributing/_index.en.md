---
title: "Contributing to Fission"
linkTitle: Contributing
weight: 7
description: >
  Set up a development environment, build and deploy Fission from source, and open your first pull request.
---

Thanks for helping make Fission better 😍!

Fission is a community project, and contributions are welcome across the board: code, documentation, feature proposals, issue triage, samples, and content.
This page gets you from a fresh clone to a running, hand-built cluster and your first pull request.

Before you start, please read the [code of conduct](https://github.com/fission/.github/blob/main/CODE_OF_CONDUCT.md).
By participating, you agree to uphold it.

## Where the code lives

Fission is split across a few repositories.
Pick the one that matches what you want to change.

| Repository | What it holds |
| :--- | :--- |
| [fission/fission](https://github.com/fission/fission) | Core platform: router, executor, builder manager, storage service, triggers, webhook, and the `fission` CLI. |
| [fission/environments](https://github.com/fission/environments) | Language runtimes and builder images (NodeJS, Python, Ruby, Go, PHP, Bash, and more). |
| [fission/keda-connectors](https://github.com/fission/keda-connectors) | Message-queue connectors that bridge KEDA-scaled triggers to function invocations. |
| [fission/fission.io](https://github.com/fission/fission.io) | This documentation site (Hugo + Docsy). |
| [fission/examples](https://github.com/fission/examples) | Sample functions in several languages. |

## Choose something to work on

The easiest way to start is to browse the open [issues](https://github.com/fission/fission/issues) and find something you'd like to take on.
Filter by the [good first issue](https://github.com/fission/fission/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) label for self-contained tasks that are friendly to newcomers.

If you pick up an issue, leave a comment saying so, so others don't duplicate your work.
For a large change or a new feature, open an issue first and discuss the design before writing code.

### Get help

We're happy to help you get unstuck.

- Drop by the [Slack channel](/slack) — the fastest place to ask questions.
- Say hi on [Twitter](https://twitter.com/fissionio).

## Set up a development environment

You'll build the Fission images yourself and deploy them to a local Kubernetes cluster.

### Prerequisites

- The [Go compiler](https://golang.org/) and tools.
  Fission {{< release-version >}} builds with Go 1.26.4 (see `go.mod`).
- [Docker](https://docs.docker.com/install) for building images locally.
  Docker Desktop is recommended on Mac and Windows.
- A Kubernetes cluster, version 1.32 or newer.
  Any of the following works:
  - [Kind](https://kind.sigs.k8s.io/) (preferred for local development)
  - [Minikube](https://github.com/kubernetes/minikube)
  - A managed cluster such as GKE, EKS, or AKS
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/) and [Helm](https://helm.sh/).
- [GoReleaser](https://goreleaser.com/install/) to build the Go binaries.
- [Skaffold](https://skaffold.dev/docs/install/) to drive the local build-and-deploy loop.
- A working understanding of core Fission concepts such as [environments]({{% ref "/docs/concepts/environments.md" %}}) and [functions]({{% ref "/docs/concepts/functions.md" %}}) helps a lot.

{{% notice info %}}
The `fission/fission` repository's `CONTRIBUTING.md` points back to this page.
This is the authoritative contributor guide.
{{% /notice %}}

### Build and deploy with Skaffold

The repository ships a Skaffold configuration with a `kind` profile for local clusters.
The general flow is: build the binaries, create the CRDs, then let Skaffold build images and deploy the Helm chart.

{{< tabs >}}
{{< tab "Kind cluster" >}}

```console
kind create cluster
kubectl create ns fission
make skaffold-prebuild   # cross-builds the Linux binaries with GoReleaser
make create-crds         # applies crds/v1 to the cluster
skaffold run -p kind
```

To redeploy after a code change, rebuild the binaries and run Skaffold again:

```console
make skaffold-prebuild
skaffold run -p kind
```

{{< /tab >}}
{{< tab "Cloud cluster (GKE/EKS/AKS)" >}}

Point your kubecontext at the target cluster, set your image registry, then run Skaffold:

```console
skaffold config set default-repo <your-registry>   # e.g. your Docker Hub handle
skaffold run
```

{{< /tab >}}
{{< /tabs >}}

{{% notice info %}}
Skaffold no longer passes `--force`, which previously caused redeploy issues.
For changes that need a pod restart, restart the affected pods manually.
{{% /notice %}}

### Verify the installation

Check that the Helm release is installed:

```console
helm list -n fission
```

Then confirm the Fission components are running:

```console
kubectl get pods -n fission
```

You should see pods for the router, executor, builder manager, storage service, kubewatcher, timer, message-queue trigger, webhook, and logger.

{{% notice info %}}
There is no `controller` pod.
The old Controller REST API server has been deprecated and removed from the architecture — the CLI and other clients now talk directly to the Kubernetes API server and Fission CRDs.
{{% /notice %}}

Finally, validate the install end to end:

```console
fission check
```

## Run the checks and tests

The `Makefile` wraps the common developer tasks.
Run these before opening a pull request so CI passes on the first try.

| Target | What it does |
| :--- | :--- |
| `make code-checks` | Runs `golangci-lint` over the codebase. |
| `make test-run` | Runs lint plus the unit/integration test script (`hack/runtests.sh`). |
| `make build-fission-cli` | Builds the `fission` CLI binary for your platform via GoReleaser. |
| `make check` | Convenience target: `test-run`, then `build-fission-cli`, then `clean`. |
| `make license-check` | Fails if any source file is missing its SPDX license header (run `make license` to add them). |

### Generated code and references

Several artifacts are generated, not hand-edited.
If you change the API types, CLI commands, or webhook annotations, regenerate the affected outputs:

| Target | Regenerates |
| :--- | :--- |
| `make codegen` | Deep-copy and client code for the CRD types. |
| `make generate-crds` | The CRD manifests under `crds/v1`. |
| `make generate-webhooks` | The admission webhook configuration from the `+kubebuilder:webhook` markers. |
| `make generate-cli-docs` | The CLI reference pages. |
| `make generate-crd-ref-docs` | The CRD reference page in this docs site. |
| `make all-generators` | Runs the code, CRD, and CLI/CRD-reference generators together (`codegen`, `generate-crds`, `generate-cli-docs`, `generate-crd-ref-docs`); run `make generate-webhooks` separately when webhook markers change. |

{{% notice warning %}}
The CLI, CRD, and metrics reference pages on this site are generated by these targets.
Edit the source in `fission/fission` and regenerate — do not hand-edit the generated Markdown.
{{% /notice %}}

## Understand the code structure

A quick map of `fission/fission` so you know where to look.

### `cmd/`

Entry points and Dockerfiles for each runtime component.
The logic here is thin; the real work lives in `pkg/`.

| Component | Form | Role |
| :--- | :--- | :--- |
| `fission-bundle` | Docker image | Single binary for every server-side component; the flag you pass decides which one it becomes. |
| `fetcher` | Docker image | Fetches source/deployment archives and specializes environment pods. |
| `fission-cli` | CLI binary | The `fission` command you run as a user. |
| `preupgradechecks` | Docker image | Pre-install and upgrade safety checks. |
| `reporter` | Docker image | Anonymous usage analytics. |

`fission-bundle` runs different services depending on its flags, for example:

```console
/fission-bundle --routerPort 8888       # runs the Router
/fission-bundle --executorPort 8888     # runs the Executor
/fission-bundle --kubewatcher           # runs the Kubernetes watcher
/fission-bundle --webhookPort 9443      # runs the admission webhook
```

The Helm chart wires the right flags and environment variables for each Deployment.

### `pkg/`

Core logic, organized by component — for example, all executor behavior lives in `pkg/executor`, the router in `pkg/router`, and so on.

As of {{< release-version >}}, the executor's environment and function controllers are built on [controller-runtime](https://github.com/kubernetes-sigs/controller-runtime) reconcilers (see `pkg/executor/envreconciler` and `pkg/executor/funcreconciler`).
They watch the Fission CRDs and the Kubernetes workloads they own, self-heal on drift, and use a cleanup finalizer (`fission.io/function-cleanup`) so teardown is reliable.

### Custom Resource Definitions

Fission's CRDs (API group `fission.io/v1`) define Kubernetes-style APIs for Fission entities: Function, Environment, Package, HTTPTrigger, TimeTrigger, MessageQueueTrigger, KubernetesWatchTrigger, and CanaryConfig.
The Go types live in [pkg/apis/core/v1/types.go](https://github.com/fission/fission/blob/master/pkg/apis/core/v1/types.go), and the generated manifests under [crds/v1](https://github.com/fission/fission/tree/master/crds).
Many constraints (valid executor types, scale bounds, checksum types) are enforced as CEL validation rules on the CRDs at the API server.

### Charts

The `fission-all` Helm chart under `charts/` deploys the whole platform; it's also what the Skaffold flow installs.

### Environments

Each language runtime lives in [fission/environments](https://github.com/fission/environments) and is fairly self-contained.
If you're adding or improving a runtime, that's the repository to work in.
You can browse the current versions on the [environments page](/environments/).

## Contribute to the docs

This site is a [Hugo](https://gohugo.io) static site using the [Docsy](https://github.com/google/docsy) theme, in the [fission/fission.io](https://github.com/fission/fission.io) repository.
Content lives under `content/en/`.

To preview your changes locally:

```console
npm install      # installs the PostCSS toolchain
hugo server      # serves the site at http://localhost:1313/
```

A few conventions to follow:

- Write one sentence per line within paragraphs.
  CommonMark renders single newlines as spaces, so the page looks identical but diffs stay surgical.
- Never hardcode a Fission version in page text.
  Use the `{{</* release-version */>}}` and `{{</* chart-version */>}}` shortcodes instead.
- Use the `ref` shortcode for internal links so broken links fail the build.
- When you move or rename a page, add a redirect in `netlify.toml` to keep old URLs working.

## Open a pull request

1. Fork the repository and create a branch off `master` (or `main` for this docs site).
2. Make your change, keeping commits focused and the history readable.
3. Run `make check` (for `fission/fission`) so lint and tests pass locally.
4. Sign off your commits if the repository requires it, and reference the issue you're addressing.
5. Push your branch and open a pull request with a clear description of the what and the why.
6. Respond to review feedback; maintainers will guide you through any required changes.

CI runs the same checks you ran locally, so a green local run usually means a green pull request.

## Related

- [Architecture overview]({{% ref "/docs/architecture/_index.md" %}})
- [Installation guide]({{% ref "/docs/installation/_index.en.md" %}})
- [CLI reference]({{% ref "/docs/reference/fission-cli/_index.md" %}})
