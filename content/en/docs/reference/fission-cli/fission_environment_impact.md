---
title: fission environment impact
slug: fission_environment_impact
url: /docs/reference/fission-cli/fission_environment_impact/
---
## fission environment impact

Show functions and aliases affected by this environment, and their env-drift status

### Synopsis

List every function that references this environment and, for each of its aliases, whether the alias's resolved version was published under an environment generation the live environment has since moved past (RFC-0025 env drift) — the batch, ahead-of-an-update view of `fission fn describe`'s per-alias EnvDrift condition.

```
fission environment impact [flags]
```

### Options

```
      --name string     Environment name
  -o, --output string   -o |:|: Output format: wide, json or yaml (default: table)
  -h, --help            help for impact
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission environment](/docs/reference/fission-cli/fission_environment/)	 - Create, update and manage environments

