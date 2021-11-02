---
title: fission timetrigger create
slug: fission_timetrigger_create
url: /docs/fission-cli/fission_timetrigger_create/
---
## fission timetrigger create

Create a time trigger

```
fission timetrigger create [flags]
```

### Options

```
      --name string          Time Trigger name
      --function string      Function name
      --cron string          Time trigger cron spec with each asterisk representing respectively second, minute, hour, the day of the month, month and day of the week. Also supports readable formats like '@every 5m', '@hourly'
      --fnNamespace string   --fns |:|: Namespace for function object (default "default")
      --spec                 Save to the spec directory instead of creating on cluster
      --dry                  View the generated specs
  -h, --help                 help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission timetrigger](/docs/fission-cli/fission_timetrigger/)	 - Create, update and manage time triggers

