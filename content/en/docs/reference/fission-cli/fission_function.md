---
title: fission function
slug: fission_function
url: /docs/reference/fission-cli/fission_function/
---
## fission function

Create, update and manage functions

### Options

```
  -h, --help   help for function
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission](/docs/reference/fission-cli/fission/)	 - Serverless framework for Kubernetes
* [fission function create](/docs/reference/fission-cli/fission_function_create/)	 - Create a function (and optionally, an HTTP route to it)
* [fission function delete](/docs/reference/fission-cli/fission_function_delete/)	 - Delete a function
* [fission function describe](/docs/reference/fission-cli/fission_function_describe/)	 - Describe a function's health in one view (summary, conditions, build, pods)
* [fission function dlq](/docs/reference/fission-cli/fission_function_dlq/)	 - Inspect and manage the async invocation dead-letter queue
* [fission function gc-versions](/docs/reference/fission-cli/fission_function_gc-versions/)	 - Sweep a function's old FunctionVersions down to its retain floor (RFC-0025)
* [fission function get](/docs/reference/fission-cli/fission_function_get/)	 - Get function source code
* [fission function getmeta](/docs/reference/fission-cli/fission_function_getmeta/)	 - Get function metadata
* [fission function list](/docs/reference/fission-cli/fission_function_list/)	 - List functions
* [fission function log](/docs/reference/fission-cli/fission_function_log/)	 - Display function logs
* [fission function pods](/docs/reference/fission-cli/fission_function_pods/)	 - List pods currently used by a function
* [fission function publish](/docs/reference/fission-cli/fission_function_publish/)	 - Publish the function's current spec as an immutable version
* [fission function rollback](/docs/reference/fission-cli/fission_function_rollback/)	 - Roll a function alias back to a previous FunctionVersion (RFC-0025)
* [fission function run-container](/docs/reference/fission-cli/fission_function_run-container/)	 - Alpha: Run a container image as a function
* [fission function run-local](/docs/reference/fission-cli/fission_function_run-local/)	 - Alpha: Run a function locally in Docker (RFC-0018)
* [fission function state](/docs/reference/fission-cli/fission_function_state/)	 - Inspect and manage a function's keyed state (RFC-0023)
* [fission function test](/docs/reference/fission-cli/fission_function_test/)	 - Test a function
* [fission function tools](/docs/reference/fission-cli/fission_function_tools/)	 - List functions exposed as MCP (Model Context Protocol) tools
* [fission function update](/docs/reference/fission-cli/fission_function_update/)	 - Update a function
* [fission function update-container](/docs/reference/fission-cli/fission_function_update-container/)	 - Alpha: Update a function running a container
* [fission function versions](/docs/reference/fission-cli/fission_function_versions/)	 - List a function's published versions
* [fission function wait](/docs/reference/fission-cli/fission_function_wait/)	 - Wait for a function to reach a status condition

