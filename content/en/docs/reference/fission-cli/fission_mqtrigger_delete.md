---
title: fission mqtrigger delete
slug: fission_mqtrigger_delete
url: /docs/reference/fission-cli/fission_mqtrigger_delete/
---
## fission mqtrigger delete

Delete a message queue trigger

```
fission mqtrigger delete [flags]
```

### Options

```
      --name string      Message queue trigger name
      --ignorenotfound   Treat "resource not found" as a successful delete.
  -h, --help             help for delete
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission mqtrigger](/docs/reference/fission-cli/fission_mqtrigger/)	 - Create, update and manage message queue triggers

