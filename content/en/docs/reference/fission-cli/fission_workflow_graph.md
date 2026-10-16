---
title: fission workflow graph
slug: fission_workflow_graph
url: /docs/reference/fission-cli/fission_workflow_graph/
---
## fission workflow graph

Render a workflow's state machine as a mermaid diagram

```
fission workflow graph [flags]
```

### Options

```
      --name string   Name of the workflow
  -f, --file string   -f |:|: Path to a Workflow manifest (kind: Workflow) or a bare WorkflowSpec YAML
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

* [fission workflow](/docs/reference/fission-cli/fission_workflow/)	 - Create, update and manage workflows

