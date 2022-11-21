---
title: fission watch list
slug: fission_watch_list
url: /docs/reference/fission-cli/fission_watch_list/
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

* [fission watch](/docs/reference/fission-cli/fission_watch/)	 - Create, update and manage kube watcher

