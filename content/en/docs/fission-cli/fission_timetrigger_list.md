---
title: fission timetrigger list
slug: fission_timetrigger_list
url: /docs/fission-cli/fission_timetrigger_list/
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
      --triggerNamespace string   --triggerns |:|: Namespace for trigger object (default "default")
  -h, --help                      help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission timetrigger](/docs/fission-cli/fission_timetrigger/)	 - Create, update and manage time triggers

