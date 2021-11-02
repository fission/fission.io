---
title: fission mqtrigger list
slug: fission_mqtrigger_list
url: /docs/fission-cli/fission_mqtrigger_list/
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

* [fission mqtrigger](/docs/fission-cli/fission_mqtrigger/)	 - Create, update and manage message queue triggers

