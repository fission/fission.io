---
title: fission topic publish
slug: fission_topic_publish
url: /docs/reference/fission-cli/fission_topic_publish/
---
## fission topic publish

Publish an event to a topic (statestore direct, or a broker via egress)

```
fission topic publish [flags]
```

### Options

```
      --topic string          Topic name
      --data string           Event payload to publish
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --content-type string   Content type the payload travels with (consuming triggers replay it) (default "application/json")
      --mqtype string         Message queue provider: statestore (built-in, namespace-scoped), or a broker type with an egress head (kafka — broker topics are cluster-flat, like kafka mqtriggers) (default "statestore")
  -h, --help                  help for publish
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission topic](/docs/reference/fission-cli/fission_topic/)	 - Publish to and inspect RFC-0027 eventing topics

