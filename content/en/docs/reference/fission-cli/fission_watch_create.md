---
title: fission watch create
slug: fission_watch_create
url: /docs/reference/fission-cli/fission_watch_create/
---
## fission watch create

Create a kube watcher

```
fission watch create [flags]
```

### Options

```
      --function string   Function name
      --name string       Watch name
      --type string       Type of resource to watch (Pod, Service, etc.) (default "pod")
      --spec              Save to the spec directory instead of creating on cluster
      --dry               View the generated specs
  -h, --help              help for create
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

