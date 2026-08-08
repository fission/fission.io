---
title: fission alias list
slug: fission_alias_list
url: /docs/reference/fission-cli/fission_alias_list/
---
## fission alias list

List function aliases

### Synopsis

List all function aliases in a namespace if specified, else, list function aliases across all namespaces

```
fission alias list [flags]
```

### Options

```
      --function string   Function this alias points at
  -A, --all-namespaces    -A |:|: Fetch resources from all namespaces
  -o, --output string     -o |:|: Output format: wide, json or yaml (default: table)
  -h, --help              help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission alias](/docs/reference/fission-cli/fission_alias/)	 - Create, update and manage function aliases

