---
title: fission watch wait
slug: fission_watch_wait
url: /docs/reference/fission-cli/fission_watch_wait/
---
## fission watch wait

Wait for a kube watcher to reach a status condition

```
fission watch wait [flags]
```

### Options

```
      --name string        Watch name
      --for string         Condition to wait for, e.g. condition=Ready or condition=Ready=False
      --timeout duration   Maximum time to wait for the condition before giving up (default 1m0s)
  -h, --help               help for wait
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission watch](/docs/reference/fission-cli/fission_watch/)	 - Create, update and manage kube watcher

