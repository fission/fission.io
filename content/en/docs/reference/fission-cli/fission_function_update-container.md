---
title: fission function update-container
slug: fission_function_update-container
url: /docs/reference/fission-cli/fission_function_update-container/
---
## fission function update-container

Alpha: Update a function running a container

```
fission function update-container [flags]
```

### Options

```
      --name string              Function name
      --image string             Name of the Docker image to be deployed as a function. Valid only when executorType is set to 'container'
      --port int                 Port where the application is running (default 8888)
      --command string           Command to be passed to the container. If not specified , the ones defined in the image are used
      --args string              Args to be passed to the command on the container. If not specified , the ones defined in the image are used
      --secret stringArray       Function access to secret, should be present in the same namespace as the function. You can provide multiple secrets using multiple --secrets flags. In the case of fn update the secrets will be replaced by the provided list of secrets.
      --configmap stringArray    Function access to configmap, should be present in the same namespace as the function. You can provide multiple configmaps using multiple --configmap flags. In case of fn update the configmaps will be replaced by the provided list of configmaps.
      --fntimeout int            --ft |:|: Maximum time for a request to wait for the response from the function (default 60)
      --idletimeout int          The length of time (in seconds) that a function is idle before pod(s) are eligible for recycling (default 120)
      --labels string            Comma separated labels to apply to the function. E.g. --labels="environment=dev,application=analytics"
      --annotation stringArray   Annotation to apply to the function. To mention multiple annotations --annotation="abc.com/team=dev" --annotation="foo=bar"
      --mincpu int               Minimum CPU to be assigned to pod (In millicore, minimum 1)
      --maxcpu int               Maximum CPU to be assigned to pod (In millicore, minimum 1)
      --minmemory int            Minimum memory to be assigned to pod (In megabyte)
      --maxmemory int            Maximum memory to be assigned to pod (In megabyte)
      --minscale int             Minimum number of pods (Uses resource inputs to configure HPA) (default 1)
      --maxscale int             Maximum number of pods (Uses resource inputs to configure HPA) (default 1)
      --targetcpu int            Target average CPU usage percentage across pods for scaling (default 80)
      --spec                     Save to the spec directory instead of creating on cluster
  -h, --help                     help for update-container
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission function](/docs/reference/fission-cli/fission_function/)	 - Create, update and manage functions

