---
title: fission watch delete
slug: fission_watch_delete
url: /docs/reference/fission-cli/fission_watch_delete/
---
## fission watch delete

Delete a kube watcher

```
fission watch delete [flags]
```

### Options

```
      --name string       Watch name
      --ignorenotfound    Treat "resource not found" as a successful delete.
      --function string   Function name
  -h, --help              help for delete
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

