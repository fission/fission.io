---
title: fission timetrigger list
slug: fission_timetrigger_list
url: /docs/reference/fission-cli/fission_timetrigger_list/
---
## fission timetrigger list

List time triggers

### Synopsis

List all time triggers in a namespace if specified, else, list time triggers across all namespaces

```
fission timetrigger list [flags]
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

* [fission timetrigger](/docs/reference/fission-cli/fission_timetrigger/)	 - Create, update and manage time triggers

