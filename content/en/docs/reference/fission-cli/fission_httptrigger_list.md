---
title: fission httptrigger list
slug: fission_httptrigger_list
url: /docs/reference/fission-cli/fission_httptrigger_list/
---
## fission httptrigger list

List HTTP triggers

### Synopsis

List all HTTP triggers in a namespace if specified, else, list HTTP triggers across all namespaces

```
fission httptrigger list [flags]
```

### Options

```
      --function string   Name of the function for trigger(s)
  -A, --all-namespaces    -A |:|: Fetch resources from all namespaces
  -h, --help              help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission httptrigger](/docs/reference/fission-cli/fission_httptrigger/)	 - Create, update and manage HTTP triggers

