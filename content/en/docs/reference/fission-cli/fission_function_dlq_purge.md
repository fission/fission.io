---
title: fission function dlq purge
slug: fission_function_dlq_purge
url: /docs/reference/fission-cli/fission_function_dlq_purge/
---
## fission function dlq purge

Permanently delete every dead-lettered async invocation

```
fission function dlq purge [flags]
```

### Options

```
      --queue string   Dead-letter queue to operate on: empty for async invocations, or an RFC-0027 broker egress queue (mq-egress-<type>, e.g. mq-egress-kafka)
  -h, --help           help for purge
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function dlq](/docs/reference/fission-cli/fission_function_dlq/)	 - Inspect and manage the async invocation dead-letter queue

