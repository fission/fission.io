---
title: fission workflow runs
slug: fission_workflow_runs
url: /docs/reference/fission-cli/fission_workflow_runs/
---
## fission workflow runs

List and inspect workflow runs (executions)

### Options

```
  -h, --help   help for runs
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow](/docs/reference/fission-cli/fission_workflow/)	 - Create, update and manage workflows
* [fission workflow runs cancel](/docs/reference/fission-cli/fission_workflow_runs_cancel/)	 - Request cancellation of a workflow run (in-flight steps drain)
* [fission workflow runs describe](/docs/reference/fission-cli/fission_workflow_runs_describe/)	 - Answer "where did this run stop": phase, active state, last error, attempts
* [fission workflow runs graph](/docs/reference/fission-cli/fission_workflow_runs_graph/)	 - Render a run's state machine with each state colored by what the run did
* [fission workflow runs history](/docs/reference/fission-cli/fission_workflow_runs_history/)	 - Show a run's full step-level event history
* [fission workflow runs list](/docs/reference/fission-cli/fission_workflow_runs_list/)	 - List workflow runs

