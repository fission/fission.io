---
title: fission httptrigger delete
slug: fission_httptrigger_delete
---
## fission httptrigger delete

Delete an HTTP trigger

```
fission httptrigger delete [flags]
```

### Options

```
      --name string               HTTP trigger name
      --function string           Name of the function for trigger(s)
      --triggerNamespace string   --triggerns |:|: Namespace for trigger object (default "default")
  -h, --help                      help for delete
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission httptrigger](/docs/fission-cli/fission_httptrigger/)	 - Create, update and manage HTTP triggers

