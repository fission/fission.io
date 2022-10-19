---
title: fission token create
slug: fission_token_create
url: /docs/reference/fission-cli/fission_token_create/
---
## fission token create

Create a JWT token for function invocation

```
fission token create [flags]
```

### Options

```
      --username string   Username to generate token for function invocation
      --password string   Password to generate token for function invocation
      --authuri string    Relative URI path to generate token
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

* [fission token](/docs/reference/fission-cli/fission_token/)	 - Create a JWT token for function invocation

