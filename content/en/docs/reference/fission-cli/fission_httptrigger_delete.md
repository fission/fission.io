---
title: fission httptrigger delete
slug: fission_httptrigger_delete
url: /docs/reference/fission-cli/fission_httptrigger_delete/
---
## fission httptrigger delete

Delete an HTTP trigger

```
fission httptrigger delete [flags]
```

### Options

```
      --name string       HTTP trigger name
      --function string   Name of the function for trigger(s)
      --ignorenotfound    Treat "resource not found" as a successful delete.
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

* [fission httptrigger](/docs/reference/fission-cli/fission_httptrigger/)	 - Create, update and manage HTTP triggers

