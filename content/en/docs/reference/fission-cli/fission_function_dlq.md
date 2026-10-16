---
title: fission function dlq
slug: fission_function_dlq
url: /docs/reference/fission-cli/fission_function_dlq/
---
## fission function dlq

Inspect and manage the async invocation dead-letter queue

### Options

```
  -h, --help   help for dlq
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions
* [fission function dlq list](/docs/reference/fission-cli/fission_function_dlq_list/)	 - List dead-lettered async invocations
* [fission function dlq purge](/docs/reference/fission-cli/fission_function_dlq_purge/)	 - Permanently delete every dead-lettered async invocation
* [fission function dlq redrive](/docs/reference/fission-cli/fission_function_dlq_redrive/)	 - Re-enqueue dead-lettered async invocations for another delivery
* [fission function dlq show](/docs/reference/fission-cli/fission_function_dlq_show/)	 - Show the full envelope of one dead-lettered async invocation

