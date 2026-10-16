---
title: fission function state set
slug: fission_function_state_set
url: /docs/reference/fission-cli/fission_function_state_set/
---
## fission function state set

Set a key in a function's state keyspace

```
fission function state set [flags]
```

### Options

```
      --name string        Function name
      --key string         State key to operate on
      --value string       Value to store
  -n, --namespace string   -n |:|: If present, the namespace scope for this CLI request
      --ttl duration       Time-to-live for the written key (e.g. 300s, 1h); 0 uses the keyspace default
      --if-version int     Compare-and-swap version precondition (0 = create-only for set; unset = unconditional)
  -h, --help               help for set
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function state](/docs/reference/fission-cli/fission_function_state/)	 - Inspect and manage a function's keyed state (RFC-0023)

