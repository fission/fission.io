---
title: fission function state delete
slug: fission_function_state_delete
url: /docs/reference/fission-cli/fission_function_state_delete/
---
## fission function state delete

Delete a key from a function's state keyspace

```
fission function state delete [flags]
```

### Options

```
      --name string        Function name
      --key string         State key to operate on
  -n, --namespace string   -n |:|: If present, the namespace scope for this CLI request
      --if-version int     Compare-and-swap version precondition (0 = create-only for set; unset = unconditional)
  -h, --help               help for delete
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function state](/docs/reference/fission-cli/fission_function_state/)	 - Inspect and manage a function's keyed state (RFC-0023)

