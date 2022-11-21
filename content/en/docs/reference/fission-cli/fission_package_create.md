---
title: fission package create
slug: fission_package_create
url: /docs/reference/fission-cli/fission_package_create/
---
## fission package create

Create a package

```
fission package create [flags]
```

### Options

```
      --env string                  Environment name
      --name string                 Package name
      --code string                 URL or local path for single file source code
      --sourcearchive stringArray   --source |:|: --src |:|: URL or local paths for source archive
      --deployarchive stringArray   --deploy |:|: URL or local paths for binary archive
      --srcchecksum string          SHA256 checksum of source archive when providing URL
      --deploychecksum string       SHA256 checksum of deploy archive when providing URL
      --insecure                    Skip generating SHA256 checksum for file integrity validation
      --buildcmd string             Build command for builder to run with
      --spec                        Save to the spec directory instead of creating on cluster
      --dry                         View the generated specs
  -h, --help                        help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission package](/docs/reference/fission-cli/fission_package/)	 - Create, update and manage packages

