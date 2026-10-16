---
title: fission workflow runs describe
slug: fission_workflow_runs_describe
url: /docs/reference/fission-cli/fission_workflow_runs_describe/
---
## fission workflow runs describe

Answer "where did this run stop": phase, active state, last error, attempts

```
fission workflow runs describe [flags]
```

### Options

```
      --name string   Name of the workflow run
  -h, --help          help for describe
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow runs](/docs/reference/fission-cli/fission_workflow_runs/)	 - List and inspect workflow runs (executions)

