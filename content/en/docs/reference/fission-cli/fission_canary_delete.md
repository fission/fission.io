---
title: fission canary delete
slug: fission_canary_delete
url: /docs/reference/fission-cli/fission_canary_delete/
---
## fission canary delete

Delete a canary config

```
fission canary delete [flags]
```

### Options

```
      --name string      Name for the canary config
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

* [fission canary](/docs/reference/fission-cli/fission_canary/)	 - Create, Update and manage canary configs

