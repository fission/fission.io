---
title: fission environment list
slug: fission_environment_list
url: /docs/reference/fission-cli/fission_environment_list/
---
## fission environment list

List environments

### Synopsis

List all environments in a namespace if specified, else, list environments across all namespaces

```
fission environment list [flags]
```

### Options

```
      --envNamespace string   --envns |:|: Namespace for environment object (default "default")
  -h, --help                  help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission environment](/docs/reference/fission-cli/fission_environment/)	 - Create, update and manage environments

