---
title: fission function update
slug: fission_function_update
url: /docs/reference/fission-cli/fission_function_update/
---
## fission function update

Update a function

```
fission function update [flags]
```

### Options

```
      --name string                 Function name
      --env string                  Environment name for function
      --entrypoint string           --entry |:|: Entry point for environment v2 to load with
      --pkgname string              --pkg |:|: Name of the existing package (--deploy and --src and --env will be ignored), should be in the same namespace as the function
      --executortype string         Executor type for execution; one of 'poolmgr', 'newdeploy' (default "poolmgr")
      --secret stringArray          Function access to secret, should be present in the same namespace as the function. You can provide multiple secrets using multiple --secrets flags. In the case of fn update the secrets will be replaced by the provided list of secrets.
      --configmap stringArray       Function access to configmap, should be present in the same namespace as the function. You can provide multiple configmaps using multiple --configmap flags. In case of fn update the configmaps will be replaced by the provided list of configmaps.
      --specializationtimeout int   --st |:|: Timeout for executor to wait for function pod creation (default 120)
      --fntimeout int               --ft |:|: Maximum time for a request to wait for the response from the function (default 60)
      --idletimeout int             The length of time (in seconds) that a function is idle before pod(s) are eligible for recycling (default 120)
      --concurrency int             --con |:|: Maximum number of pods specialized concurrently to serve requests (default 500)
      --requestsperpod int          --rpp |:|: Maximum number of concurrent requests that can be served by a specialized pod (default 1)
      --onceonly                    --yolo |:|: Specifies if specialized pod will serve exactly one request in its lifetime
      --labels string               Comma separated labels to apply to the function. E.g. --labels="environment=dev,application=analytics"
      --annotation stringArray      Annotation to apply to the function. To mention multiple annotations --annotation="abc.com/team=dev" --annotation="foo=bar"
      --retainpods int              Number of pods to retain after pods specialization.
      --code string                 URL or local path for single file source code
      --sourcearchive stringArray   --source |:|: --src |:|: URL or local paths for source archive
      --deployarchive stringArray   --deploy |:|: URL or local paths for binary archive
      --srcchecksum string          SHA256 checksum of source archive when providing URL
      --deploychecksum string       SHA256 checksum of deploy archive when providing URL
      --insecure                    Skip generating SHA256 checksum for file integrity validation
      --buildcmd string             Package build command for builder to run with
  -f, --force                       -f |:|: Force update a package even if it is used by one or more functions
      --mincpu int                  Minimum CPU to be assigned to pod (In millicore, minimum 1)
      --maxcpu int                  Maximum CPU to be assigned to pod (In millicore, minimum 1)
      --minmemory int               Minimum memory to be assigned to pod (In megabyte)
      --maxmemory int               Maximum memory to be assigned to pod (In megabyte)
      --minscale int                Minimum number of pods (Uses resource inputs to configure HPA) (default 1)
      --maxscale int                Maximum number of pods (Uses resource inputs to configure HPA) (default 1)
      --targetcpu int               Target average CPU usage percentage across pods for scaling (default 80)
      --spec                        Save to the spec directory instead of creating on cluster
  -h, --help                        help for update
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

