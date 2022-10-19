---
title: fission function list
slug: fission_function_list
url: /docs/reference/fission-cli/fission_function_list/
---
## fission function list

List functions

### Synopsis

List all functions in a namespace if specified, else, list functions across all namespaces

```
fission function list [flags]
```

### Options

```
  -A, --all-namespaces   -A |:|: Fetch resources from all namespaces
  -h, --help             help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

