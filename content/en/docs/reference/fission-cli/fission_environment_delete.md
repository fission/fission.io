---
title: fission environment delete
slug: fission_environment_delete
url: /docs/reference/fission-cli/fission_environment_delete/
---
## fission environment delete

Delete an environment

```
fission environment delete [flags]
```

### Options

```
      --name string           Environment name
      --envNamespace string   --envns |:|: Namespace for environment object (default "default")
      --ignorenotfound        Treat "resource not found" as a successful delete.
  -f, --force                 -f |:|: Force delete env even if one or more functions exist
  -h, --help                  help for delete
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission environment](/docs/reference/fission-cli/fission_environment/)	 - Create, update and manage environments

