---
title: fission spec apply
slug: fission_spec_apply
url: /docs/fission-cli/fission_spec_apply/
---
## fission spec apply

Create, update, or delete resources from application specification

```
fission spec apply [flags]
```

### Options

```
      --specdir string      Directory to store specs, defaults to ./specs
      --specignore string   File containing specs to be ingored inside --specdir, defaults to .specignore
      --delete              Allow apply to delete resources that no longer exist in the specification
      --wait                Wait for package builds
      --watch               Watch local files for change, and re-apply specs as necessary
      --validation string   Turns server side validations of Fission objects on/off
  -h, --help                help for apply
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission spec](/docs/fission-cli/fission_spec/)	 - Manage a declarative application specification

