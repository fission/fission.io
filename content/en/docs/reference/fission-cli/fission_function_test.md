---
title: fission function test
slug: fission_function_test
url: /docs/reference/fission-cli/fission_function_test/
---
## fission function test

Test a function

```
fission function test [flags]
```

### Options

```
      --name string          Function name
      --method stringArray   HTTP Methods: GET,POST,PUT,DELETE,HEAD. To mention single method: --method GET and for multiple methods --method GET --method POST. [DEPRECATED for 'fn create', use 'route create' instead] (default [GET])
  -H, --header stringArray   -H |:|: Request headers
  -b, --body string          -b |:|: Request body
  -q, --query stringArray    -q |:|: Request query parameters: -q key1=value1 -q key2=value2
  -t, --timeout duration     -t |:|: Length of time to wait for the response. If set to zero or negative number, no timeout is set (default 1m0s)
      --dbtype string        Log database type, e.g. influxdb (currently influxdb and kubernetes logs are supported) (default "kubernetes")
      --subpath string       Sub Path to check if function internally supports routing
  -h, --help                 help for test
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

