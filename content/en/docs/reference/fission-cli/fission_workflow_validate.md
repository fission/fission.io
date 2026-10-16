---
title: fission workflow validate
slug: fission_workflow_validate
url: /docs/reference/fission-cli/fission_workflow_validate/
---
## fission workflow validate

Validate a workflow manifest offline (graph, expressions), plus referenced-function existence against the cluster unless --offline

```
fission workflow validate [flags]
```

### Options

```
  -f, --file string   -f |:|: Path to a Workflow manifest (kind: Workflow) or a bare WorkflowSpec YAML
      --name string   Name of the workflow
      --offline       Skip cluster checks (e.g. referenced-function existence)
  -h, --help          help for validate
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow](/docs/reference/fission-cli/fission_workflow/)	 - Create, update and manage workflows

