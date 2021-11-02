---
title: fission canary list
slug: fission_canary_list
url: /docs/fission-cli/fission_canary_list/
---
## fission canary list

List canary configs

### Synopsis

List all canary configs in a namespace if specified, else, list canary configs across all namespaces

```
fission canary list [flags]
```

### Options

```
      --canaryNamespace string   --canaryns |:|: Namespace for canary config object (default "default")
  -h, --help                     help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission canary](/docs/fission-cli/fission_canary/)	 - Create, Update and manage canary configs

