---
title: fission canary wait
slug: fission_canary_wait
url: /docs/reference/fission-cli/fission_canary_wait/
---
## fission canary wait

Wait for a canary config to reach a status condition

```
fission canary wait [flags]
```

### Options

```
      --name string        Name for the canary config
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

* [fission canary](/docs/reference/fission-cli/fission_canary/)	 - Create, Update and manage canary configs

