---
title: fission httptrigger wait
slug: fission_httptrigger_wait
url: /docs/reference/fission-cli/fission_httptrigger_wait/
---
## fission httptrigger wait

Wait for an HTTP trigger to reach a status condition

```
fission httptrigger wait [flags]
```

### Options

```
      --name string        HTTP trigger name
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

* [fission httptrigger](/docs/reference/fission-cli/fission_httptrigger/)	 - Create, update and manage HTTP triggers

