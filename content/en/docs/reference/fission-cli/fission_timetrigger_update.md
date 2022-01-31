---
title: fission timetrigger update
slug: fission_timetrigger_update
---
## fission timetrigger update

Update a time trigger

```
fission timetrigger update [flags]
```

### Options

```
      --name string               Time Trigger name
      --function string           Function name
      --cron string               Time trigger cron spec with each asterisk representing respectively second, minute, hour, the day of the month, month and day of the week. Also supports readable formats like '@every 5m', '@hourly'
      --triggerNamespace string   --triggerns |:|: Namespace for trigger object (default "default")
  -h, --help                      help for update
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission timetrigger](/docs/reference/fission-cli/fission_timetrigger/)	 - Create, update and manage time triggers

