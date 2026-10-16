---
title: fission topic peek
slug: fission_topic_peek
url: /docs/reference/fission-cli/fission_topic_peek/
---
## fission topic peek

Show the most recent events on a statestore topic

```
fission topic peek [flags]
```

### Options

```
      --topic string       Topic name
  -n, --namespace string   -n |:|: If present, the namespace scope for this CLI request
      --limit int          Maximum events to peek (default 10)
  -h, --help               help for peek
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission topic](/docs/reference/fission-cli/fission_topic/)	 - Publish to and inspect RFC-0027 eventing topics

