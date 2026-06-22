---
title: fission function run-local
slug: fission_function_run-local
url: /docs/reference/fission-cli/fission_function_run-local/
---
## fission function run-local

Alpha: Run a function locally in Docker (RFC-0018)

### Synopsis

Alpha: Run a function locally in Docker — no cluster round-trip. For poolmgr/newdeploy (--executor, default poolmgr) it runs the environment runtime image (from --env or --image) and replays the specialize contract over --code (single file) or --deploy (a pre-built directory for multi-file apps); for --executor=container it runs the user's own --image server directly. Either way it invokes the function the same way the cluster does.

```
fission function run-local [flags]
```

### Options

```
      --name string                 Function name
      --executortype string         Executor type for execution; one of 'poolmgr', 'newdeploy' (default "poolmgr")
      --code string                 URL or local path for single file source code
      --deployarchive stringArray   --deploy |:|: URL or local paths for binary archive
      --env string                  Environment name for function
      --image string                Name of the Docker image to be deployed as a function. Valid only when executorType is set to 'container'
      --env-version int             Environment API version of the runtime image when running locally with --image (ignored when --env resolves it) (default 2)
      --entrypoint string           --entry |:|: Entry point for environment v2 to load with
      --port int                    Port where the application is running (default 8888)
      --method stringArray          HTTP Methods: GET,POST,PUT,DELETE,HEAD. To mention single method: --method GET and for multiple methods --method GET --method POST. [DEPRECATED for 'fn create', use 'route create' instead] (default [GET])
  -H, --header stringArray          -H |:|: Request headers
  -b, --body string                 -b |:|: Request body
      --subpath string              Sub Path to check if function internally supports routing
      --keep                        Keep the local function container and mount running after the invocation instead of tearing it down
  -w, --watch                       -w |:|: Serve the function locally and re-specialize on source change (hot reload); env executors only
  -e, --env-var stringArray         -e |:|: Set a runtime env var KEY=VALUE in the local container (repeatable)
      --env-from string             Read runtime env vars from a file (one KEY=VALUE per line); -e overrides
      --secret stringArray          Function access to secret, should be present in the same namespace as the function. You can provide multiple secrets using multiple --secrets flags. In the case of fn update the secrets will be replaced by the provided list of secrets.
      --configmap stringArray       Function access to configmap, should be present in the same namespace as the function. You can provide multiple configmaps using multiple --configmap flags. In case of fn update the configmaps will be replaced by the provided list of configmaps.
      --debug-port int              Publish an additional container port for a debugger (delve/debugpy) to attach to
      --build                       Compile the source with the environment builder image before running (compiled environments)
      --builder-image string        Builder image to use with --build when running cluster-less (defaults to the environment's builder image)
      --buildcmd string             Package build command for builder to run with
  -h, --help                        help for run-local
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

