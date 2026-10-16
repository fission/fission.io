---
title: fission function dlq redrive
slug: fission_function_dlq_redrive
url: /docs/reference/fission-cli/fission_function_dlq_redrive/
---
## fission function dlq redrive

Re-enqueue dead-lettered async invocations for another delivery

```
fission function dlq redrive [flags]
```

### Options

```
      --id string      Durable invocation id of a dead-lettered async invocation
      --all            Apply to every dead-lettered invocation
      --queue string   Dead-letter queue to operate on: empty for async invocations, or a broker egress queue (mq-egress-<type>, e.g. mq-egress-kafka)
  -h, --help           help for redrive
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function dlq](/docs/reference/fission-cli/fission_function_dlq/)	 - Inspect and manage the async invocation dead-letter queue

