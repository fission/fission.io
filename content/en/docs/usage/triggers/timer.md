---
title: "Timer Triggers"
date: 2019-12-17T14:38:24+08:00
weight: 4
description: >
  Invoke functions on a cron schedule with timer triggers using fission timer create, supporting cron specs and descriptors like @every.
---

A **time trigger invokes a function on a cron schedule** — once, or repeatedly.
Use it for periodic jobs such as cleanups, report generation, or polling an external system.

The `timer` component evaluates your schedule using server time and POSTs to your function through the router when each scheduled moment arrives.

## Cron format

Schedules are written as [robfig/cron specifications](https://pkg.go.dev/github.com/robfig/cron).
Fission accepts the standard five fields and an optional leading seconds field, so a spec is either:

```text
┌───────────── second (optional, 0 - 59)
│ ┌───────────── minute (0 - 59)
│ │ ┌───────────── hour (0 - 23)
│ │ │ ┌───────────── day of month (1 - 31)
│ │ │ │ ┌───────────── month (1 - 12)
│ │ │ │ │ ┌───────────── day of week (0 - 6)
│ │ │ │ │ │
* * * * * *
```

Friendlier descriptors such as `@every 1m`, `@hourly`, and `@daily` are also supported.

## Create a time trigger

Run a function every 30 minutes:

```bash
$ fission timer create --name halfhourly --function hello --cron "0 */30 * * * *"
trigger 'halfhourly' created
Current Server Time: 2019-12-17T08:33:28Z
Next 1 invocation: 2019-12-17T09:00:00Z
```

Or use a descriptor instead of a cron field list:

```bash
$ fission timer create --name minute --function hello --cron "@every 1m"
trigger 'minute' created
Current Server Time: 2019-12-17T08:33:43Z
Next 1 invocation: 2019-12-17T08:34:43Z
```

## List time triggers

List your triggers to see their function and cron spec:

```bash
$ fission timer list
NAME       CRON           FUNCTION_NAME
halfhourly 0 */30 * * * * hello
minute     @every 1m      hello
```

## Test a schedule

Use `showschedule` to preview the upcoming invocations for a cron spec without creating a trigger.
This is the quickest way to check that a spec means what you think it does.

```bash
$ fission timer showschedule --cron "0 30 * * * *" --round 5
Current Server Time: 2018-06-12T05:07:41Z
Next 1 invocation: 2018-06-12T05:30:00Z
Next 2 invocation: 2018-06-12T06:30:00Z
Next 3 invocation: 2018-06-12T07:30:00Z
Next 4 invocation: 2018-06-12T08:30:00Z
Next 5 invocation: 2018-06-12T09:30:00Z
```

{{% notice info %}}
Schedules are evaluated against the **server's** time, not your laptop's.
The times printed above come from the Fission cluster.
{{% /notice %}}

## Related

- [Triggers overview]({{% ref "_index.md" %}})
- [HTTP Trigger]({{% ref "http-trigger.md" %}})
