---
title: fission canary create
slug: fission_canary_create
url: /docs/reference/fission-cli/fission_canary_create/
---
## fission canary create

Create a canary config

### Synopsis

Create a canary config that gradually shifts HTTP traffic from an old
target to a new one, watching the new target's Prometheus error rate and
rolling back automatically if it crosses --threshold.

Two modes, selected by what --httptrigger references:

  function-weights mode (classic): the trigger's function reference type is
  "function-weights" and --newfn/--oldfn name two FUNCTIONS already present
  in its weights map. The controller steps HTTPTrigger.FunctionWeights.

  alias mode (RFC-0025): the trigger references a FunctionAlias (created via
  'fission alias create'). --newfn/--oldfn then name two FunctionVersions
  (see 'fission fn versions') of the alias's function — not functions. The
  controller steps the FunctionAlias's Weight/SecondaryVersion instead,
  leaving the alias's primary Version pinned at --oldfn until the rollout
  either promotes (repoints the alias at --newfn) or rolls back.

Example (alias mode):

  fission alias create --function orders --name prod --version orders-v3
  fission canary create --name orders-canary --httptrigger prod-route \
    --newfn orders-v4 --oldfn orders-v3 --increment-step 20 --increment-interval 2m --failure-threshold 10


```
fission canary create [flags]
```

### Options

```
      --name string                 Name for the canary config
      --httptrigger string          Http trigger that this config references
      --newfunction string          --newfn |:|: New version of the function
      --oldfunction string          --oldfn |:|: Old stable version of the function
      --increment-step int          --step |:|: Weight increment step for function (default 20)
      --increment-interval string   --internal |:|: Weight increment interval, string representation of time.Duration, ex : 1m, 2h, 2d (default "2m")
      --failure-threshold int       --threshold |:|: Threshold in percentage beyond which the new version of the function is considered unstable (default 10)
  -h, --help                        help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission canary](/docs/reference/fission-cli/fission_canary/)	 - Create, Update and manage canary configs

