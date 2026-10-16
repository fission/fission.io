---
title: fission workflow update
slug: fission_workflow_update
url: /docs/reference/fission-cli/fission_workflow_update/
---
## fission workflow update

Update a workflow from a manifest

### Synopsis

Update a workflow from a manifest. --name overrides the manifest's metadata.name.

```
fission workflow update [flags]
```

### Options

```
  -f, --file string   -f |:|: Path to a Workflow manifest (kind: Workflow) or a bare WorkflowSpec YAML
      --name string   Name of the workflow
  -h, --help          help for update
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission workflow](/docs/reference/fission-cli/fission_workflow/)	 - Create, update and manage workflows

