---
title: fission httptrigger list
slug: fission_httptrigger_list
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
      --triggerNamespace string   --triggerns |:|: Namespace for trigger object (default "default")
      --function string           Name of the function for trigger(s)
  -h, --help                      help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission httptrigger](/docs/fission-cli/fission_httptrigger/)	 - Create, update and manage HTTP triggers

