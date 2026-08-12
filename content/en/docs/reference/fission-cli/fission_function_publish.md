---
title: fission function publish
slug: fission_function_publish
url: /docs/reference/fission-cli/fission_function_publish/
---
## fission function publish

Publish the function's current spec as an immutable version

### Synopsis

Publish the function's current spec as an immutable FunctionVersion snapshot (RFC-0025); idempotent -- called again with an unchanged spec and package digest, it returns the existing newest version instead of minting a duplicate. --output/-o accepts: (default table) prints "created <name>" or "unchanged <name>"; "name" prints only the bare FunctionVersion name, one line, for scripting (mirrors kubectl's -o name); "json"/"yaml" marshal the full FunctionVersion object; "wide" renders the same as the default table (no extra columns).

```
fission function publish [flags]
```

### Options

```
      --name string          Function name
      --description string   Human-readable description recorded on the minted FunctionVersion
      --wait                 Wait for the function's referenced package build to finish before publishing (see --timeout)
      --timeout duration     Maximum time to wait for the condition before giving up (default 1m0s)
  -o, --output string        -o |:|: Output format: wide, json or yaml (default: table)
  -h, --help                 help for publish
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

