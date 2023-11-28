---
title: fission environment create
slug: fission_environment_create
url: /docs/reference/fission-cli/fission_environment_create/
---
## fission environment create

Create an environment

```
fission environment create [flags]
```

### Options

```
      --name string               Environment name
      --image string              Environment image URL
      --poolsize int              Size of the pool (default 3)
      --builder string            Environment builder image URL
      --buildcmd string           Build command for environment builder to build source package
      --mincpu int                Minimum CPU to be assigned to pod (In millicore, minimum 1)
      --maxcpu int                Maximum CPU to be assigned to pod (In millicore, minimum 1)
      --minmemory int             Minimum memory to be assigned to pod (In megabyte)
      --maxmemory int             Maximum memory to be assigned to pod (In megabyte)
      --graceperiod int           --period |:|: Grace time (in seconds) for pod to perform connection draining before termination (only non-negative values considered)
      --version int               Environment API version (1 means v1 interface) (default 1)
      --imagepullsecret string    Secret for Kubernetes to pull an image from a private registry
      --keeparchive               Keep the archive instead of extracting it into a directory (mainly for the JVM environment because .jar is one kind of zip archive)
      --externalnetwork           Allow pod to access external network (only works when istio feature is enabled)
      --labels string             Comma separated labels to apply to the function. E.g. --labels="environment=dev,application=analytics"
      --annotation stringArray    Annotation to apply to the function. To mention multiple annotations --annotation="abc.com/team=dev" --annotation="foo=bar"
      --spec                      Save to the spec directory instead of creating on cluster
      --dry                       View the generated specs
      --builder-env stringArray   Environment variable to be set in the builder container
      --runtime-env stringArray   Environment variable to be set in the runtime container
  -h, --help                      help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission environment](/docs/reference/fission-cli/fission_environment/)	 - Create, update and manage environments

