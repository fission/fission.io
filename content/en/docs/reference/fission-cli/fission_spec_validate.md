---
title: fission spec validate
slug: fission_spec_validate
url: /docs/reference/fission-cli/fission_spec_validate/
---
## fission spec validate

Validate declarative application specification

```
fission spec validate [flags]
```

### Options

```
      --specdir string      Directory to store specs, defaults to ./specs
      --specignore string   File containing specs to be ignored inside --specdir, defaults to .specignore
      --allowconflicts      If true, spec apply will be forced even if conflicting resources exist
  -h, --help                help for validate
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

