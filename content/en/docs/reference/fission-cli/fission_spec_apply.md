---
title: fission spec apply
slug: fission_spec_apply
url: /docs/reference/fission-cli/fission_spec_apply/
---
## fission spec apply

Create, update, or delete resources from application specification

```
fission spec apply [flags]
```

### Options

```
      --specdir string      Directory to store specs, defaults to ./specs
      --specignore string   File containing specs to be ignored inside --specdir, defaults to .specignore
      --delete              Allow apply to delete resources that no longer exist in the specification
      --wait                Wait for package builds
      --watch               Watch local files for change, and re-apply specs as necessary
      --validation string   Turns server side validations of Fission objects on/off
      --commitlabel         Apply commit label to the resources
      --allowconflicts      If true, spec apply will be forced even if conflicting resources exist
      --force-namespace     --force |:|: If true, resources will be created in namespace provided by (--namespace flag ) even if spec file contains some other namespace
  -h, --help                help for apply
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

