---
title: "Create Environment"
draft: false
weight: 1
---

## Create an environment

You can create an environment on your cluster from an image for that language.

Optionally, you can specify CPU and memory resource limits.
You can also specify the number of initially pre-warmed pods, which is called the poolsize.

```bash
$ fission env create --name node \
                     --image ghcr.io/fission/node-env \
                     --mincpu 40 --maxcpu 80 \
                     --minmemory 64 --maxmemory 128 \
                     --poolsize 4
```

In case of the pool based executor, the resources specified for environment are used for function pod as well.
In case of new deployment executor, you can override the resources when you create a function.

## Using a builder

When you create an environment, you can specify a builder image and builder command which will be used for building from source code.
You can override the build command when creating a function.
For more details on builder and packages, check out examples in [Functions]({{% ref "functions.en.md" %}}) and [Packages]({{% ref "package.en.md" %}}).

```bash
$ fission env create --name python \
                     --image ghcr.io/fission/python-env \
                     --builder ghcr.io/fission/python-builder
```

## Viewing environment information

You can list the environments or view information of an individual environment:

```bash
$ fission env list
NAME UID                                  IMAGE                  POOLSIZE MINCPU MAXCPU MINMEMORY MAXMEMORY
node ac84d62e-001f-11e8-85c9-42010aa00010 ghcr.io/fission/node-env 4        40m    80m    64Mi      128Mi

$ fission env get --name node
NAME UID                                  IMAGE
node ac84d62e-001f-11e8-85c9-42010aa00010 ghcr.io/fission/node-env

$ kubectl get environment.fission.io -o yaml
# Full YAML of Fission environment object
```
