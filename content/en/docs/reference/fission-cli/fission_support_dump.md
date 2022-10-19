---
title: fission support dump
slug: fission_support_dump
url: /docs/reference/fission-cli/fission_support_dump/
---
## fission support dump

Collect & dump all necessary information for troubleshooting

```
fission support dump [flags]
```

### Options

```
      --nozip           Save dump information into multiple files instead of single zip file
  -o, --output string   -o |:|: Output directory to save dump archive/files (default "fission-dump")
  -h, --help            help for dump
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission support](/docs/reference/fission-cli/fission_support/)	 - Collect diagnostic information for support

