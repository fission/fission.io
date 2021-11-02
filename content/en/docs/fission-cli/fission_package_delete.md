---
title: fission package delete
slug: fission_package_delete
url: /docs/fission-cli/fission_package_delete/
---
## fission package delete

Delete a package

```
fission package delete [flags]
```

### Options

```
      --name string           Package name
  -f, --force                 -f |:|: Force update a package even if it is used by one or more functions
      --orphan                Orphan packages that are not referenced by any function
      --pkgNamespace string   --pkgns |:|: Namespace for package object (default "default")
  -h, --help                  help for delete
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission package](/docs/fission-cli/fission_package/)	 - Create, update and manage packages

