---
title: "RBAC Permissions for Fission CLI"
linkTitle: RBAC permissions
draft: false
weight: 60
---

{{< notice info >}}
RBAC permission in Fisson CLI is available from Fission version-1.18.0
{{< /notice >}}

Fission CLI supports Kubernetes RBAC through which we can decide specific action the user can perform. Fission Admin can create user's account and provide them with the permission that fits the user role.

## Setup & pre-requisites for RBAC permission in Fission CLI

You will need a Kubernetes cluster with Fission installed (Please check [installation page]({{% ref "../../installation/" %}}) for details).
You should have a account - in this tutorial we have named it as - fission-user

## Creating Role for Fission CLI User

User can perform mutliple actions using Fission CLI. And below is the clusterrole which allows user to perform all task which Fission CLI provides.

In the below file comments describe the use of each permission in format-

` # <fission CLI command1> <subcommand1>,<subcommand2>; <fission CLI command 1> <subcommand1>,<subcommand2>; `

eg,

`# function- create,delete` means the resource permission is required for Fission CLI in,

- `fission function create` &
- `fission function delete`
  commands

```fission-user-role.yaml``` file

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fission-user
rules:
# Function - create,update, run-container,update-container
# Spec -apply, destroy
- apiGroups:
  - ""
  resources:
  - configmaps
  - secrets
  verbs:
  - get

# functions - log, pod 
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

# Fission -version
# function - test, create, update
# archive - download, geturl, list, upload, delete
# package - create, update
# timetrigger - create, update, test
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
  verbs:
  - list # canary -list
  - get # canary - get, update
  - create # canary - create
  - update # canary - update
  - delete #canary - delete

- apiGroups:
  - fission.io
  resources:
  - environments
  verbs:
  - list # environments -list, create;spec-list,apply,destroy ;fission dump
  - get # environments - get, update, pod; function - create
  - create # environments - create;spec-apply,destroy
  - update # environments - update;spec-apply,destroy
  - delete # environments - delete;spec-apply,destroy

- apiGroups:
  - fission.io
  resources:
  - functions
  verbs:
  - list #  function- list, update; environement - delete;package-list, update, delete;spec-list,apply,destroy ;fission dump
  - get # function- get, create, getmeta, log, pod, run-container, update-container, update; httptrigger- create, update; mqtrigger - create, update
  - create # function - create, run-container; spec-apply,destroy
  - update # function- update-container, update; package-update;spec-apply,destroy
  - delete # function -delete; spec-apply,destroy

- apiGroups:
  - fission.io
  resources:
  - packages
  verbs:
  - list # canary -list; package-delete,list; spec-list,apply,destroy; fission dump
  - get # function - create, get,update; package-delete,get,info,rebuild,update; spec-apply,destroy
  - create # canary - create;function-create; package-create;spec-apply,destroy
  - update # canary - update; function - update; package- rebuild,update;spec-apply,destroy
  - delete #canary - delete;package-delete;spec-apply,destroy

- apiGroups:
  - fission.io
  resources:
  - httptriggers
  verbs:
  - list # httptrigger- create,delete,list,update; spec-list,apply,destroy; fission dump
  - get # canary - get; httptrigger- create,get,list,update, 
  - create # function -create;httptrigger- create; spec-apply,destroy
  - update # httptrigger- update; spec-apply,destroy
  - delete # httptrigger-delete; spec-apply,destroy

- apiGroups:
  - fission.io
  resources:
  - kuberneteswatchtriggers
  verbs:
  - list # watch -list; spec-list,apply,destroy; fission dump
  - create # watch - create; spec-apply,destroy
  - delete # watch - delete; spec-apply,destroy

- apiGroups:
  - fission.io
  resources:
  - messagequeuetriggers
  verbs:
  - list # mqtrigger -list; spec-list, apply, destroy; fission dump
  - get # mqtrigger - get, update
  - create # mqtrigger - create; spec-apply,destroy
  - update # mqtrigger - update; spec-apply,destroy
  - delete # mqtrigger - delete; spec-apply,destroy

- apiGroups:
  - fission.io
  resources:
  - timetriggers
  verbs:
  - list # timetrigger -list; spec-list, apply, destroy; fission dump
  - get # timetrigger - get, update; spec-list, apply, destroy
  - create # timetrigger - create; spec-list, apply, destroy
  - update # timetrigger - update; spec-list, apply, destroy
  - delete #timetrigger - delete; spec-list, apply, destroy
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

## Implementing Role on Fission CLI User

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

## Testing Fission CLI commands using fission-user

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

The above mentioned `fission-user-role.yaml` file clearly mentions which commands uses what permission. Depending on the users we can create different Cluster Roles and assign it to users and provide specific accesses to them.
