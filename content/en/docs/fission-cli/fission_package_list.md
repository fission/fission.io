---
title: fission package list
slug: fission_package_list
url: /docs/fission-cli/fission_package_list/
---
## fission package list

List packages

### Synopsis

List all packages in a namespace if specified, else, list packages across all namespaces

```
fission package list [flags]
```

### Options

```
      --orphan                Orphan packages that are not referenced by any function
      --status string         Filter packages by status
      --pkgNamespace string   --pkgns |:|: Namespace for package object (default "default")
  -h, --help                  help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission package](/docs/fission-cli/fission_package/)	 - Create, update and manage packages

