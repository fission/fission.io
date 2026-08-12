---
title: fission function dlq show
slug: fission_function_dlq_show
url: /docs/reference/fission-cli/fission_function_dlq_show/
---
## fission function dlq show

Show the full envelope of one dead-lettered async invocation

```
fission function dlq show [flags]
```

### Options

```
      --id string      Durable invocation id of a dead-lettered async invocation
      --queue string   Dead-letter queue to operate on: empty for async invocations, or a broker egress queue (mq-egress-<type>, e.g. mq-egress-kafka)
  -h, --help           help for show
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function dlq](/docs/reference/fission-cli/fission_function_dlq/)	 - Inspect and manage the async invocation dead-letter queue

