---
title: fission function create
slug: fission_function_create
url: /docs/reference/fission-cli/fission_function_create/
---
## fission function create

Create a function (and optionally, an HTTP route to it)

```
fission function create [flags]
```

### Options

```
      --name string                        Function name
      --env string                         Environment name for function
      --entrypoint string                  --entry |:|: Entry point for environment v2 to load with
      --pkgname string                     --pkg |:|: Name of the existing package (--deploy and --src and --env will be ignored), should be in the same namespace as the function
      --executortype string                Executor type for execution; one of 'poolmgr', 'newdeploy' (default "poolmgr")
      --configmap stringArray              Function access to configmap, should be present in the same namespace as the function. You can provide multiple configmaps using multiple --configmap flags. In case of fn update the configmaps will be replaced by the provided list of configmaps.
      --secret stringArray                 Function access to secret, should be present in the same namespace as the function. You can provide multiple secrets using multiple --secrets flags. In the case of fn update the secrets will be replaced by the provided list of secrets.
  -e, --env-var stringArray                -e |:|: Per-function environment variable as KEY=VALUE; repeatable. On fn update the provided list replaces the function's env vars. (--env keeps meaning the Environment name.)
      --env-from-secret stringArray        Project a same-namespace Secret into the function's environment: 'name' for the whole object, 'name/key' for one key (variable named after the key), 'name/key:ENV' to rename it; repeatable. On fn update the provided list replaces the previous one.
      --env-from-configmap stringArray     Project a same-namespace ConfigMap into the function's environment: 'name' for the whole object, 'name/key' for one key (variable named after the key), 'name/key:ENV' to rename it; repeatable. On fn update the provided list replaces the previous one.
      --specializationtimeout int          --st |:|: Timeout for executor to wait for function pod creation (default 120)
      --fntimeout int                      --ft |:|: Maximum time for a request to wait for the response from the function (default 60)
      --idletimeout int                    The length of time (in seconds) that a function is idle before pod(s) are eligible for recycling (default 120)
      --concurrency poolmgr                --con |:|: Maximum number of pods specialized concurrently to serve requests (Only valid for executortype; poolmgr) (default 500)
      --requestsperpod poolmgr             --rpp |:|: Maximum number of concurrent requests that can be served by a specialized pod (Only valid for executortype; poolmgr) (default 1)
      --streaming                          Enable streaming (SSE/chunked/WebSocket) responses for this function; the response is flushed incrementally and not cut by the function timeout
      --streamingprotocol string           Streaming protocol when --streaming is set; one of 'auto', 'sse', 'chunked', 'websocket' (default "auto")
      --streamingidletimeout int           Idle timeout (seconds) for a streaming response before it is aborted; reset on each chunk (default 60)
      --streamingmaxduration int           Hard ceiling (seconds) on total streaming response lifetime; 0 means no ceiling (the idle timeout governs)
      --expose-as-mcp                      Advertise this function as a Model Context Protocol (MCP) tool on the MCP server
      --tool-description string            Agent-facing tool description (required with --expose-as-mcp)
      --tool-input-schema string           Path to a JSON Schema file describing the tool's arguments; advertised verbatim as the MCP tool inputSchema
      --tool-name string                   Override the advertised MCP tool name (defaults to <namespace>-<function name>)
      --state                              Opt the function into the keyed-state API
      --state-keyspace string              State keyspace name (defaults to the function name; explicit so a rename keeps the data)
      --state-max-keys int                 Max live keys in the keyspace (0 = platform default)
      --state-max-value-bytes int          Max size of one state value in bytes (0 = platform default)
      --state-ttl duration                 Default TTL applied to state writes without an explicit TTL (0 = keys do not expire)
      --state-sticky-source string         Sticky routing key source: header or queryparam
      --state-sticky-name string           Header or query-parameter name holding the sticky routing key
      --async-retry-max-attempts int       Async delivery attempt budget before dead-lettering
      --async-max-age duration             Max time an async invocation may wait for successful delivery before it is dead-lettered
      --async-on-success string            Same-namespace function to invoke with the result after a successful async delivery; empty clears it
      --async-on-failure string            Same-namespace function to invoke with the result after a permanent async failure; empty clears it
      --async-on-success-topic string      Statestore topic to publish the result envelope to after a successful async delivery; empty clears it
      --async-on-failure-topic string      Statestore topic to publish the result envelope to after a permanent async failure; empty clears it
      --onceonly poolmgr                   --yolo |:|: Specifies if specialized pod will serve exactly one request in its lifetime (Only valid for executortype; poolmgr)
      --labels string                      Comma separated labels to apply to the function. E.g. --labels="environment=dev,application=analytics"
      --annotation stringArray             Annotation to apply to the function. To mention multiple annotations --annotation="abc.com/team=dev" --annotation="foo=bar"
      --retainpods int                     Number of pods to retain after pods specialization.
      --provisioned-concurrency int        Number of warm specialized pods to maintain eagerly (poolmgr only). 0 (default)=no provisioned concurrency
      --versioning fission fn publish      Opt the function into immutable version snapshots and named aliases; one of 'auto' (mint a version on every runtime-affecting update), 'manual' (mint only on fission fn publish), or 'off' (disable, update only)
      --retain-versions int                Number of unaliased versions to keep per function before older ones are garbage collected (requires --versioning auto|manual, or an existing versioning config); disambiguates from --retainpods, which retains specialized pods rather than function versions
      --provisioned-schedule stringArray   name=<window-name>;start=<cron(0 9 * * *)>;duration=<10h(time.Duration)>;target=<number of pods>
      --code string                        URL or local path for single file source code
      --sourcearchive stringArray          --source |:|: --src |:|: URL or local paths for source archive
      --deployarchive stringArray          --deploy |:|: URL or local paths for binary archive
      --srcchecksum string                 SHA256 checksum of source archive when providing URL
      --deploychecksum string              SHA256 checksum of deploy archive when providing URL
      --insecure                           Skip generating SHA256 checksum for file integrity validation
      --oci string                         Pre-built OCI image reference containing the deployment code (registry/repo:tag[@digest])
      --buildcmd string                    Package build command for builder to run with
      --url string                         URL pattern (supports {var} and {var:regexp} path templates) [DEPRECATED for 'fn create', use 'route create' instead]
      --prefix string                      Prefix with which functions are exposed. NOTE: Prefix takes precedence over URL/RelativeURL [DEPRECATED for 'fn create', use 'route create' instead]
      --method stringArray                 HTTP Methods: GET,POST,PUT,DELETE,HEAD. To mention single method: --method GET and for multiple methods --method GET --method POST. [DEPRECATED for 'fn create', use 'route create' instead] (default [GET])
      --mincpu int                         Minimum CPU to be assigned to pod (In millicore, minimum 1)
      --maxcpu int                         Maximum CPU to be assigned to pod (In millicore, minimum 1)
      --minmemory int                      Minimum memory to be assigned to pod (In megabyte)
      --maxmemory int                      Maximum memory to be assigned to pod (In megabyte)
      --minscale int                       Minimum number of pods (Uses resource inputs to configure HPA) (default 1)
      --maxscale int                       Maximum number of pods (Uses resource inputs to configure HPA) (default 1)
      --targetcpu int                      Target average CPU usage percentage across pods for scaling (default 80)
      --spec                               Save to the spec directory instead of creating on cluster
      --dry                                View the generated specs
  -h, --help                               help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

