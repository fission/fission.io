---
title: fission watch list
slug: fission_watch_list
url: /docs/fission-cli/fission_watch_list/
---
## fission watch list

List kube watchers

### Synopsis

List all kube watchers in a namespace if specified, else, list kube watchers across all namespaces

```
fission watch list [flags]
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

* [fission watch](/docs/fission-cli/fission_watch/)	 - Create, update and manage kube watcher

