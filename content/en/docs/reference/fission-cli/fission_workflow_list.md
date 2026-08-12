---
title: fission workflow list
slug: fission_workflow_list
url: /docs/reference/fission-cli/fission_workflow_list/
---
## fission workflow list

List workflows

### Synopsis

List all workflows in a namespace if specified, else, list workflows across all namespaces

```
fission workflow list [flags]
```

### Options

```
  -A, --all-namespaces   -A |:|: Fetch resources from all namespaces
  -o, --output string    -o |:|: Output format: wide, json or yaml (default: table)
  -h, --help             help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow](/docs/reference/fission-cli/fission_workflow/)	 - Create, update and manage workflows

