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
  -r, --reverse                -r |:|: Specify the log reverse query base on time, it will be invalid if the 'follow' flag is specified. valid for dbtype as influxdb
      --recordcount int        Get N most recent log records (default 20)
  -d, --detail                 -d |:|: Display detailed information
      --pod string             Function pod name (use the latest pod name if unspecified)
      --dbtype string          Log database type, e.g. influxdb (currently influxdb and kubernetes logs are supported) (default "kubernetes")
      --pod-namespace string   Namespace in which function's pod are created. If not specified, function's namespace is used. Note: version <1.18 used fission-function as pod's default ns.
      --all-pods               Get all pod's logs in the function.
  -h, --help                   help for log
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

