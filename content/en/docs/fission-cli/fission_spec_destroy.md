---
title: fission spec destroy
slug: fission_spec_destroy
url: /docs/fission-cli/fission_spec_destroy/
---
## fission spec destroy

Delete all Fission resources in the application specification

```
fission spec destroy [flags]
```

### Options

```
      --specdir string      Directory to store specs, defaults to ./specs
      --specignore string   File containing specs to be ignored inside --specdir, defaults to .specignore
  -h, --help                help for destroy
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission spec](/docs/fission-cli/fission_spec/)	 - Manage a declarative application specification

