---
title: fission alias wait
slug: fission_alias_wait
url: /docs/reference/fission-cli/fission_alias_wait/
---
## fission alias wait

Wait for a function alias to reach a status condition

### Synopsis

Wait for a FunctionAlias to reach a status condition, e.g. `fission alias wait --name prod --for condition=Resolved` after an `alias create`/`alias update`/`fn rollback`, so a caller (CI, a script) can tell when the alias resolver has actually converged on the new target rather than racing it. FunctionAlias's only condition type is Resolved.

```
fission alias wait [flags]
```

### Options

```
      --name string        Name for the function alias
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

* [fission alias](/docs/reference/fission-cli/fission_alias/)	 - Create, update and manage function aliases

