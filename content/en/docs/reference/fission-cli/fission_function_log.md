---
title: fission function log
slug: fission_function_log
url: /docs/reference/fission-cli/fission_function_log/
---
## fission function log

Display function logs

```
fission function log [flags]
```

### Options

```
      --name string            Function name
  -f, --follow                 -f |:|: Specify if the logs should be streamed
  -r, --reverse                -r |:|: Specify the log reverse query base on time, it will be invalid if the 'follow' flag is specified. valid for dbtype as loki
      --recordcount int        Get N most recent log records (default 20)
  -d, --detail                 -d |:|: Display detailed information
      --pod string             Function pod name (use the latest pod name if unspecified)
      --dbtype string          Log database type: kubernetes (default) or loki (default "kubernetes")
      --pod-namespace string   Namespace in which function's pod are created. If not specified, function's namespace is used. Note: version <1.18 used fission-function as pod's default ns.
      --all-pods               Get all pod's logs in the function.
      --request-id string      Filter logs to a single invocation by its X-Fission-Request-ID (loki dbtype)
      --trace-id string        Filter logs by trace id (loki dbtype)
      --level string           Filter logs by level, e.g. error (loki dbtype)
      --alias string           Show logs for a specific alias's (e.g. prod) resolved version instead of the live function; mutually exclusive with --version; kubernetes dbtype only
      --version string         Show logs for a specific pinned FunctionVersion instead of the live function; mutually exclusive with --alias; kubernetes dbtype only
  -h, --help                   help for log
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

