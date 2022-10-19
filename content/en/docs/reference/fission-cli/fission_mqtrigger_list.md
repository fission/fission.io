---
title: fission mqtrigger list
slug: fission_mqtrigger_list
url: /docs/reference/fission-cli/fission_mqtrigger_list/
---
## fission mqtrigger list

List message queue triggers

### Synopsis

List all message queue triggers in a namespace if specified, else, list message queue triggers across all namespaces

```
fission mqtrigger list [flags]
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

* [fission mqtrigger](/docs/reference/fission-cli/fission_mqtrigger/)	 - Create, update and manage message queue triggers

