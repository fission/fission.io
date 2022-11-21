---
title: fission mqtrigger create
slug: fission_mqtrigger_create
url: /docs/reference/fission-cli/fission_mqtrigger_create/
---
## fission mqtrigger create

Create a message queue trigger

```
fission mqtrigger create [flags]
```

### Options

```
      --function string        Function name
      --topic string           Message queue Topic the trigger listens on
      --name string            Message queue trigger name
      --mqtype string          For mqtype "fission" => kafka
                               					 For mqtype "keda" => kafka, aws-sqs-queue, aws-kinesis-stream, gcp-pubsub, stan, nats-jetstream, rabbitmq, redis (default "kafka")
      --resptopic string       Topic that the function response is sent on (response discarded if unspecified)
      --errortopic string      Topic that the function error messages are sent to (errors discarded if unspecified
      --maxretries int         Maximum number of times the function will be retried upon failure
  -c, --contenttype string     -c |:|: Content type of messages that publish to the topic (default "application/json")
      --spec                   Save to the spec directory instead of creating on cluster
      --dry                    View the generated specs
      --pollinginterval int    Interval to check the message source for up/down scaling operation of consumers (default 30)
      --cooldownperiod int     The period to wait after the last trigger reported active before scaling the consumer back to 0 (default 300)
      --minreplicacount int    Minimum number of replicas of consumers to scale down to
      --maxreplicacount int    Maximum number of replicas of consumers to scale up to (default 100)
      --secret string          Name of secret object
      --metadata stringArray   Metadata needed for connecting to source system in format: --metadata key1=value1 --metadata key2=value2
      --mqtkind string         Kind of Message Queue Trigger, e.g. fission, keda (default "keda")
  -h, --help                   help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission mqtrigger](/docs/reference/fission-cli/fission_mqtrigger/)	 - Create, update and manage message queue triggers

