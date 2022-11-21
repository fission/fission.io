---
title: fission canary update
slug: fission_canary_update
url: /docs/reference/fission-cli/fission_canary_update/
---
## fission canary update

Update parameters of a canary config

```
fission canary update [flags]
```

### Options

```
      --name string                 Name for the canary config
      --increment-step int          --step |:|: Weight increment step for function (default 20)
      --increment-interval string   --internal |:|: Weight increment interval, string representation of time.Duration, ex : 1m, 2h, 2d (default "2m")
      --failure-threshold int       --threshold |:|: Threshold in percentage beyond which the new version of the function is considered unstable (default 10)
  -h, --help                        help for update
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

