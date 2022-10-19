---
title: fission timetrigger showschedule
slug: fission_timetrigger_showschedule
url: /docs/reference/fission-cli/fission_timetrigger_showschedule/
---
## fission timetrigger showschedule

Show schedule for cron spec

```
fission timetrigger showschedule [flags]
```

### Options

```
      --cron string   Time trigger cron spec with each asterisk representing respectively second, minute, hour, the day of the month, month and day of the week. Also supports readable formats like '@every 5m', '@hourly'
      --round int     Get next N rounds of invocation time (default 1)
  -h, --help          help for showschedule
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission timetrigger](/docs/reference/fission-cli/fission_timetrigger/)	 - Create, update and manage time triggers

