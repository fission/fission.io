---
title: fission workflow runs history
slug: fission_workflow_runs_history
url: /docs/reference/fission-cli/fission_workflow_runs_history/
---
## fission workflow runs history

Show a run's full step-level event history

```
fission workflow runs history [flags]
```

### Options

```
      --name string   Name of the workflow run
      --io            Include step input/output payloads (dereferences spilled documents)
  -h, --help          help for history
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow runs](/docs/reference/fission-cli/fission_workflow_runs/)	 - List and inspect workflow runs (executions)

