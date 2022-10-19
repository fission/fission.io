---
title: fission environment pods
slug: fission_environment_pods
url: /docs/reference/fission-cli/fission_environment_pods/
---
## fission environment pods

List pods currently maintained by an environment

### Synopsis

List pods currently maintained by an environment

```
fission environment pods [flags]
```

### Options

```
      --name string           Environment name
      --executortype string   Executor type of pod in environment; one of 'poolmgr', 'newdeploy', 'container'
  -h, --help                  help for pods
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission environment](/docs/reference/fission-cli/fission_environment/)	 - Create, update and manage environments

