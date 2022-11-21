---
title: fission spec init
slug: fission_spec_init
url: /docs/reference/fission-cli/fission_spec_init/
---
## fission spec init

Create an initial declarative application specification

```
fission spec init [flags]
```

### Options

```
      --name string       Name for the app, applied to resources as a Kubernetes annotation
      --deployid string   --id |:|: Deployment ID for the spec deployment config
      --specdir string    Directory to store specs, defaults to ./specs
  -h, --help              help for init
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

