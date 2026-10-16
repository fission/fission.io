---
title: fission function dlq list
slug: fission_function_dlq_list
url: /docs/reference/fission-cli/fission_function_dlq_list/
---
## fission function dlq list

List dead-lettered async invocations

```
fission function dlq list [flags]
```

### Options

```
  -n, --namespace string   -n |:|: If present, the namespace scope for this CLI request
      --limit int          Maximum number of dead-lettered invocations to list (default 100)
  -o, --output string      -o |:|: Output format: wide, json or yaml (default: table)
      --queue string       Dead-letter queue to operate on: empty for async invocations, or a broker egress queue (mq-egress-<type>, e.g. mq-egress-kafka)
  -h, --help               help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function dlq](/docs/reference/fission-cli/fission_function_dlq/)	 - Inspect and manage the async invocation dead-letter queue

