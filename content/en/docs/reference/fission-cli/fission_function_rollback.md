---
title: fission function rollback
slug: fission_function_rollback
url: /docs/reference/fission-cli/fission_function_rollback/
---
## fission function rollback

Roll a function alias back to a previous FunctionVersion (RFC-0025)

### Synopsis

Repoint a FunctionAlias at a previously resolved FunctionVersion: by default the alias's previous target (Status.History's last entry), or an explicit --to version. Always a full repoint — clears Weight/SecondaryVersion, so a rollback issued mid-canary stops the traffic split rather than only rolling back the primary target. Refuses to touch an alias managed by `fission spec` (Git) unless --detach. For a one-off repoint to a version you already know, see `fission alias update --version --wait` instead.

```
fission function rollback [flags]
```

### Options

```
      --name string           Function name
      --alias string          FunctionAlias to roll back
      --to string             Explicit FunctionVersion name to roll back to (default: the alias's previous target, Status.History's last entry)
      --detach fission spec   Strip fission spec (Git) ownership annotations from the alias so a future `spec apply` does not revert the rollback
      --wait                  Wait for the alias to resolve to the rollback target (see --timeout)
      --timeout duration      Maximum time to wait for the condition before giving up (default 1m0s)
  -h, --help                  help for rollback
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

