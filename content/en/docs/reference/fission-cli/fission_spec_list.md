---
title: fission spec list
slug: fission_spec_list
url: /docs/reference/fission-cli/fission_spec_list/
---
## fission spec list

List all the resources that were created through this spec

```
fission spec list [flags]
```

### Options

```
      --deployid string     --id |:|: Deployment ID for the spec deployment config
      --specdir string      Directory to store specs, defaults to ./specs
      --specignore string   File containing specs to be ignored inside --specdir, defaults to .specignore
  -A, --all-namespaces      -A |:|: Fetch resources from all namespaces
  -h, --help                help for list
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission spec](/docs/reference/fission-cli/fission_spec/)	 - Manage a declarative application specification

