---
title: fission workflow run
slug: fission_workflow_run
url: /docs/reference/fission-cli/fission_workflow_run/
---
## fission workflow run

Start one execution of a workflow

```
fission workflow run [flags]
```

### Options

```
      --name string    Name of the workflow
      --input string   Run input as inline JSON, or @path/to/file.json
  -h, --help           help for run
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow](/docs/reference/fission-cli/fission_workflow/)	 - Create, update and manage workflows

