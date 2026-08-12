---
title: fission function describe
slug: fission_function_describe
url: /docs/reference/fission-cli/fission_function_describe/
---
## fission function describe

Describe a function's health in one view (summary, conditions, build, pods)

```
fission function describe [flags]
```

### Options

```
      --name string      Function name
      --version string   Describe a specific pinned FunctionVersion's snapshot instead of the live function
  -h, --help             help for describe
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

