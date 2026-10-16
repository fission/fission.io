---
title: fission workflow runs graph
slug: fission_workflow_runs_graph
url: /docs/reference/fission-cli/fission_workflow_runs_graph/
---
## fission workflow runs graph

Render a run's state machine with each state colored by what the run did

### Synopsis

Render a run's state machine as a mermaid diagram, coloring each state by what this run did: succeeded, active, failed, or never reached. Drawn against the spec snapshot the run is executing, so it stays accurate even if the workflow was edited or deleted since.

```
fission workflow runs graph [flags]
```

### Options

```
      --name string   Name of the workflow run
      --open          Render the diagram in a browser (served locally; the graph never leaves your machine)
  -h, --help          help for graph
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow runs](/docs/reference/fission-cli/fission_workflow_runs/)	 - List and inspect workflow runs (executions)

