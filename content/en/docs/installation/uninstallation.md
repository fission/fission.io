---
title: "Uninstalling Fission"
linkTitle: Uninstallation
weight: 71
description: >
  Uninstallation guide for Fission
---
If you want to completely uninstall Fission from your cluster, the following command will help you do that.
This might be required in situations where in you want to uninstall the current version and [install Fission](/docs/installation/) as a fresh instance.

```bash
helm uninstall <release name>
```

> Get the release name by running `helm list` and replace with the actual `<release name>`

The above command will *only delete the installed services*. Custom resources that were created by Fission will need to be **manually deleted**.

Get a list of fission CRDs

```bash
kubectl get crd | grep "fission.io"
```

```bash
NAME                                       CREATED AT
canaryconfigs.fission.io                   2022-01-17T05:47:28Z
environments.fission.io                    2022-01-17T05:47:29Z
functions.fission.io                       2022-01-17T05:47:29Z
httptriggers.fission.io                    2022-01-17T05:47:29Z
kuberneteswatchtriggers.fission.io         2022-01-17T05:47:29Z
messagequeuetriggers.fission.io            2022-01-17T05:47:29Z
packages.fission.io                        2022-01-17T05:47:30Z
timetriggers.fission.io                    2022-01-17T05:47:30Z

```

Delete individual CRD, replace `<crd-name>` with the actual CRD name

```bash
kubectl get <crd-name> -o name | xargs -n1 kubectl delete
```
