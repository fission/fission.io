---
title: "Run and Inspect"
weight: 20
description: >
  Create, run, and manage workflows from the CLI — start runs, see where a run stopped with the runs commands, and visualize the state machine in a local viewer.
---

**Manage a workflow definition with `fission workflow`, start executions with `workflow run`, and trace each execution with the `workflow runs` subgroup.**

This page assumes you have a manifest — see [Authoring workflows]({{% ref "authoring.md" %}}) — and that workflows are [enabled]({{% ref "_index.md" %}}#prerequisites).

## Manage the definition

`fission workflow` is the definition lifecycle.
It mirrors the other Fission resources:

```bash
fission workflow create -f workflow.yaml
fission workflow update -f workflow.yaml
fission workflow list
fission workflow delete --name order-pipeline
```

## Start a run

`workflow run` creates a `WorkflowRun` and prints its name.
Pass input as inline JSON or `@path/to/file.json`:

```bash
$ fission workflow run --name order-pipeline --input @inputs/happy.json
Run started: order-pipeline-7k2p9
```

Each `run` is an independent execution with its own state and history.
The definition is unchanged.

## Inspect runs

The `runs` subgroup operates on executions.
Every command takes `--name <run>` (the run name printed by `workflow run`), except `runs list`:

```bash
# All runs, or just this workflow's
fission workflow runs list
fission workflow runs list --workflow order-pipeline

# Where did this run stop, and why?
fission workflow runs describe --name order-pipeline-7k2p9

# The full event log; --io also shows step input/output payloads
fission workflow runs history --name order-pipeline-7k2p9
fission workflow runs history --name order-pipeline-7k2p9 --io

# Stop a running execution
fission workflow runs cancel --name order-pipeline-7k2p9
```

`runs describe` is the "where is it / where did it stop" view: the phase, the active or final state, and the failure reason if it failed.
`runs history` is the underlying event log — the durable record the engine resumes from.

## Visualize

`workflow graph` renders a workflow's state machine as a diagram.
`--name` reads a stored workflow; `-f` reads a manifest that has not been applied yet:

```bash
# Print a mermaid state diagram
fission workflow graph --name order-pipeline
fission workflow graph -f workflow.yaml

# Open it in a local day/night viewer
fission workflow graph --name order-pipeline --open
```

`workflow runs graph --name <run>` draws the same diagram but overlays a specific run's status.
Each state is colored by what that run actually did, so the picture *is* the answer to "where did this run stop":

```bash
fission workflow runs graph --name order-pipeline-7k2p9 --open
```

{{% notice info %}}
`--open` serves the diagram from an ephemeral local web server and renders it in your own browser — the workflow never leaves your machine.
In a run overlay, states that only route (a `Choice`) emit no step events and are labeled "not tracked" rather than colored as a status.
{{% /notice %}}

## Related

- [Authoring workflows]({{% ref "authoring.md" %}}) — the manifest these commands operate on.
- [Examples]({{% ref "examples.md" %}}) — runnable workflows with sample inputs.
- [Workflow CLI reference]({{% ref "/docs/reference/fission-cli/fission_workflow.md" %}}) — every command and flag.
