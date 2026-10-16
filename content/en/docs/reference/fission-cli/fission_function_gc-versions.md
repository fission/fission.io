---
title: fission function gc-versions
slug: fission_function_gc-versions
url: /docs/reference/fission-cli/fission_function_gc-versions/
---
## fission function gc-versions

Sweep a function's old FunctionVersions down to its retain floor (RFC-0025)

### Synopsis

Runs one on-demand retention-GC sweep, the same engine the buildermgr-hosted controller runs automatically. Never deletes a version referenced by any FunctionAlias, or the newest/only version, however low --keep is set.

```
fission function gc-versions [flags]
```

### Options

```
      --name string   Function name
      --keep int      Override the retain count for this sweep (default: the function's Spec.Versioning.Retain, or 10)
  -h, --help          help for gc-versions
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

