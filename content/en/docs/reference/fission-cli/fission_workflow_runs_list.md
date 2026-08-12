---
title: fission workflow runs list
slug: fission_workflow_runs_list
url: /docs/reference/fission-cli/fission_workflow_runs_list/
---
## fission workflow runs list

List workflow runs

```
fission workflow runs list [flags]
```

### Options

```
      --workflow string   Only show runs of this workflow
  -A, --all-namespaces    -A |:|: Fetch resources from all namespaces
  -o, --output string     -o |:|: Output format: wide, json or yaml (default: table)
  -h, --help              help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow runs](/docs/reference/fission-cli/fission_workflow_runs/)	 - List and inspect workflow runs (executions)

