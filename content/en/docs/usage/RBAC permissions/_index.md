---
title: "Adding RBAC Permissions"
linkTitle: RBAC permissions
draft: false
weight: 60
---

Fission supports Kubernetes RBAC through which we can decide specific action the user can perform. By default all task in Fission are performed by `default` service account. But user can create their own account and provide them the permission which fits according to user role.

## Setup & pre-requisites

You will need a Kubernetes cluster with Fission installed (Please check [installation page]({{% ref "../../installation/" %}}) for details).
You have a account named - fission-user

## Creating Role

User can perform mutliple actions using Fission CLI. And below is the clusterrole which allows user to perform all task which Fission CLI provides.

```fission-user-role.yaml```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fission-user
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - secrets
  verbs:
  - get
- apiGroups:
  - ""
  resources:
  - pods
  - pods/log
  verbs:
  - list
  - get
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - list
- apiGroups:
  - ""
  resources:
  - pods/portforward
  verbs:
  - list
  - create 

- apiGroups:
  - fission.io
  resources:
  - canaryconfigs
  - environments
  - functions
  - httptriggers
  - kuberneteswatchtriggers
  - messagequeuetriggers
  - packages
  - timetriggers
  verbs:
  - list
  - get
  - create
  - update
  - delete
```

We also need to create corresponding rolebinding to create binding for the account and user.

```fission-user-rolebinding.yaml```

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: fission-user1
subjects:
  - kind: ServiceAccount
    name: fission-user
roleRef:
  kind: ClusterRole
  name: fission-user
  apiGroup: rbac.authorization.k8s.io


```

## Example

Lets create a role using above mentioned `fission-user-role.yaml`

```bash
kubectl apply -f fission-user-role.yaml 
clusterrole.rbac.authorization.k8s.io/fission-user configured
```

Similarly we create a rolebinding.yaml

```bash
kubectl apply -f charts/fission-all/templates/serviceAccount/rolebinding.yaml 
clusterrolebinding.rbac.authorization.k8s.io/fission-user created
```

Now we need to set our current-context to use the service account.
In the example we have used a kind cluster.

```bash
kubectl config set-credentials fission-user \
  --client-certificate=/path/to/certificate.crt \
  --client-key=/path/to/key.key
```

```bash
kubectl config set-context fission-user-context --cluster=kind-kind --user=fission-user
Context "fission-user" created.

kubectl config use-context fission-user
Switched to context "fission-user".
```

## Testing

With the above setting Fission CLI will use fission-user to perform all actions. Let's create an environment and a Fission function using [create function]({{% ref "../function/functions/" %}})-

``` bash
$ fission env create --name node --image fission/node-env -n default
poolsize setting default to 3
environment 'node' created

$ fission fn create --name hello --code hello.js --env node
Package 'hello-a2318569-0d2d-4b63-826d-6d4d2665be50' created
function 'hello' created
```

## Conclusion

Depending on the users we can create different Cluster Roles and assign it to users.
