---
title: fission package update
slug: fission_package_update
url: /docs/reference/fission-cli/fission_package_update/
---
## fission package update

Update a package

```
fission package update [flags]
```

### Options

```
      --name string                 Package name
      --env string                  Environment name
      --code string                 URL or local path for single file source code
      --sourcearchive stringArray   --source |:|: --src |:|: URL or local paths for source archive
      --deployarchive stringArray   --deploy |:|: URL or local paths for binary archive
      --srcchecksum string          SHA256 checksum of source archive when providing URL
      --deploychecksum string       SHA256 checksum of deploy archive when providing URL
      --insecure                    Skip generating SHA256 checksum for file integrity validation
      --buildcmd string             Build command for builder to run with
  -f, --force                       -f |:|: Force update a package even if it is used by one or more functions
  -h, --help                        help for update
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

