---
title: "Fission CRD Reference"
weight: 8
description: >
  Fission Custom Resources Definition(CRD) Reference
---
# API Reference

## Packages
- [fission.io/v1](#fissioniov1)


## fission.io/v1


Package v1 contains API Schema definitions for the fission.io v1 API group

### Resource Types
- [CanaryConfig](#canaryconfig)
- [Environment](#environment)
- [FissionTenant](#fissiontenant)
- [FissionTenantList](#fissiontenantlist)
- [Function](#function)
- [FunctionAlias](#functionalias)
- [FunctionAliasList](#functionaliaslist)
- [FunctionVersion](#functionversion)
- [FunctionVersionList](#functionversionlist)
- [HTTPTrigger](#httptrigger)
- [KubernetesWatchTrigger](#kuberneteswatchtrigger)
- [MessageQueueTrigger](#messagequeuetrigger)
- [Package](#package)
- [TimeTrigger](#timetrigger)
- [Workflow](#workflow)
- [WorkflowList](#workflowlist)
- [WorkflowRun](#workflowrun)
- [WorkflowRunList](#workflowrunlist)



#### AliasTargetRecord



AliasTargetRecord is one entry in FunctionAliasStatus.History: a
previously resolved target, kept for audit / rollback visibility.



_Appears in:_
- [FunctionAliasStatus](#functionaliasstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `version` _string_ |  |  |  |
| `packageDigest` _string_ |  |  |  |
| `switchedAt` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ |  |  |  |


#### AllowedFunctionsPerContainer

_Underlying type:_ _string_

AllowedFunctionsPerContainer defaults to 'single'. Related to Fission Workflows



_Appears in:_
- [EnvironmentSpec](#environmentspec)



#### Archive



Archive contains or references a collection of sources or
binary files.
The CEL rule below deliberately never references self.literal: any
access to a byte-format field (even has()) makes the apiserver convert
its base64 value for CEL using URL-safe decoding, which rejects any
standard-base64 payload containing '/' or '+' — in practice every
zipped literal archive. The literal/oci combination is instead
rejected by the webhook (Archive.Validate), with the same message.



_Appears in:_
- [PackageSpec](#packagespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[ArchiveType](#archivetype)_ | Type defines how the package is specified: literal, URL, or OCI.<br />Available value:<br /> - literal<br /> - url<br /> - oci |  | Enum: [ literal url oci] <br /> |
| `literal` _integer array_ | Literal contents of the package. Can be used for<br />encoding packages below TODO (256 KB?) size. |  |  |
| `url` _string_ | URL references a package. |  |  |
| `checksum` _[Checksum](#checksum)_ | Checksum ensures the integrity of packages<br />referenced by URL. Ignored for literals. |  |  |
| `oci` _[OCIArchive](#ociarchive)_ | OCI references an OCI image holding the deployment code.<br />Mutually exclusive with Literal and URL. Supported only on<br />PackageSpec.Deployment; PackageSpec.Validate rejects it on Source<br />(source archives feed the builder, which has no OCI pull path). |  |  |


#### ArchiveType

_Underlying type:_ _string_

ArchiveType is literal, url, or oci, indicating whether the
package is specified in the Archive struct or externally.



_Appears in:_
- [Archive](#archive)

| Field | Description |
| --- | --- |
| `literal` | ArchiveTypeLiteral means the package contents are specified in the Literal field of<br />resource itself.<br /> |
| `url` | ArchiveTypeUrl means the package contents are at the specified URL.<br /> |
| `oci` | ArchiveTypeOCI means the package contents are the filesystem of an<br />OCI image referenced in the OCI field of the resource.<br /> |




#### BuildStatus

_Underlying type:_ _string_

BuildStatus indicates the current build status of a package.



_Appears in:_
- [PackageStatus](#packagestatus)



#### Builder



Builder is the setting for environment builder.
Bounded podspec / container safety rules — see the matching Runtime block above.



_Appears in:_
- [EnvironmentSpec](#environmentspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `image` _string_ | Image for containing the language compilation environment. |  |  |
| `command` _string_ | (Optional) Default build command to run for this build environment. |  |  |
| `container` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#container-v1-core)_ | (Optional) Container allows the modification of the deployed builder<br />container using the Kubernetes Container spec. Fission overrides<br />the following fields:<br />- Name<br />- Image; set to the Builder.Image<br />- Command; set to the Builder.Command<br />- TerminationMessagePath<br />- ImagePullPolicy<br />- ReadinessProbe |  |  |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#podspec-v1-core)_ | PodSpec will store the spec of the pod that will be applied to the pod created for the builder |  |  |


#### CanaryConfig



CanaryConfig is for canary deployment of two functions.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `CanaryConfig` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[CanaryConfigSpec](#canaryconfigspec)_ |  |  |  |
| `status` _[CanaryConfigStatus](#canaryconfigstatus)_ |  |  |  |


#### CanaryConfigSpec



CanaryConfigSpec defines the canary configuration spec



_Appears in:_
- [CanaryConfig](#canaryconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `trigger` _string_ | HTTP trigger that this config references |  |  |
| `newfunction` _string_ | New version of the function |  |  |
| `oldfunction` _string_ | Old stable version of the function |  |  |
| `weightincrement` _integer_ | Weight increment step for function |  |  |
| `duration` _string_ | Weight increment interval, string representation of time.Duration, ex : 1m, 2h, 2d (default: "2m") |  |  |
| `failurethreshold` _integer_ | Threshold in percentage beyond which the new version of the function is considered unstable |  |  |
| `failureType` _[FailureType](#failuretype)_ |  |  |  |


#### CanaryConfigStatus



CanaryConfigStatus represents canary config status



_Appears in:_
- [CanaryConfig](#canaryconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `status` _string_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ | Conditions represent the latest observations of the canary's state. |  |  |


#### Checksum



Checksum of package contents when the contents are stored
outside the Package struct. Type is the checksum algorithm;
"sha256" is the only currently supported one. Sum is hex
encoded.



_Appears in:_
- [Archive](#archive)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[ChecksumType](#checksumtype)_ |  |  |  |
| `sum` _string_ |  |  |  |


#### ChecksumType

_Underlying type:_ _string_

ChecksumType specifies the checksum algorithm, such as
sha256, used for a checksum.



_Appears in:_
- [Checksum](#checksum)

| Field | Description |
| --- | --- |
| `sha256` |  |


#### ConfigMapReference



ConfigMapReference is a reference to a kubernetes configmap.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `namespace` _string_ |  |  |  |
| `name` _string_ |  |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |
| `mountPath` _string_ | MountPath redirects this configmap's file projection from the<br />default /configs/<namespace>/<name>; relative to the /configs root.<br />See SecretReference.MountPath for the constraint rationale. |  |  |


#### DestinationRef



DestinationRef routes an async invocation's result to exactly one target: a
Function (invoked async through the same machinery, depth-capped) or a Topic
(published to a message queue). Exactly one of Function/Topic must be set.
Topic destinations on the built-in statestore provider are supported
(RFC-0027); broker types are rejected by the webhook until the egress phase
lands.



_Appears in:_
- [InvocationConfig](#invocationconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `function` _[FunctionReference](#functionreference)_ | Function is a same-namespace function destination, invoked asynchronously<br />with the result envelope as its body (depth-capped to stop runaway chains). |  |  |
| `topic` _[TopicRef](#topicref)_ | Topic publishes the result envelope to a message-queue topic. |  |  |


#### Environment



Environment is environment for building and running user functions.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `Environment` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[EnvironmentSpec](#environmentspec)_ |  |  |  |
| `status` _[EnvironmentStatus](#environmentstatus)_ |  |  |  |


#### EnvironmentReference



EnvironmentReference is a reference to an environment. It is used by both
FunctionSpec.Environment and PackageSpec.Environment.



_Appears in:_
- [FunctionSpec](#functionspec)
- [PackageSpec](#packagespec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `namespace` _string_ |  |  |  |
| `name` _string_ | Name of the referenced environment. Optional + omitempty: an unset<br />reference is omitted and its Pattern skipped (a container function has<br />no environment; a Package with an unset environment is admitted and<br />fails later with a clear builder error — the fission CLI still rejects<br />it). When set, it must be a DNS-1123 label. |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |


#### EnvironmentSpec



EnvironmentSpec contains with builder, runtime and some other related environment settings.



_Appears in:_
- [Environment](#environment)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `version` _integer_ | Version is the Environment API version<br />Version "1" allows user to run code snippet in a file, and<br />it's supported by most of the environments except tensorflow-serving.<br />Version "2" supports downloading and compiling user function if source archive is not empty.<br />Version "3" is almost the same with v2, but you're able to control the size of pre-warm pool of the environment. |  | Maximum: 3 <br />Minimum: 1 <br /> |
| `runtime` _[Runtime](#runtime)_ | Runtime is configuration for running function, like container image etc. |  |  |
| `builder` _[Builder](#builder)_ | (Optional) Builder is configuration for builder manager to launch environment builder to build source code into<br />deployable binary. |  |  |
| `allowedFunctionsPerContainer` _[AllowedFunctionsPerContainer](#allowedfunctionspercontainer)_ | (Optional) defaults to 'single'. Fission workflow uses<br />'infinite' to load multiple functions in one function pod.<br />Available value:<br />- single<br />- infinite |  | Enum: [single infinite] <br /> |
| `allowAccessToExternalNetwork` _boolean_ | Istio default blocks all egress traffic for safety.<br />To enable accessibility of external network for builder/function pod, set to 'true'.<br />(Optional) defaults to 'false' |  |  |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#resourcerequirements-v1-core)_ | The request and limit CPU/MEM resource setting for poolmanager to set up pods in the pre-warm pool.<br />(Optional) defaults to no limitation. |  |  |
| `poolsize` _integer_ | The initial pool size for environment |  | Minimum: 0 <br /> |
| `terminationGracePeriod` _integer_ | The grace time for pod to perform connection draining before termination. The unit is in seconds.<br />A terminating function pod keeps serving for the WHOLE grace window<br />(the preStop hook sleeps through it, then the kubelet kills the pod),<br />so this value is exactly how long every teardown — idle reap, env<br />update roll, upgrade, node drain — takes per pod. 90s covers endpoint<br />propagation (seconds) plus the 60s default function timeout with<br />margin, mirroring the router's own 75s-drain/90s-grace posture; set<br />it per environment for functions with longer request timeouts.<br />The CRD default below is what makes the documented default true for<br />API-created Environments: nil means "use the default" and the<br />apiserver fills an absent field with 90 at serving time.<br />The *pointer* is what makes an EXPLICIT 0 ("no drain window, kill<br />instantly") expressible from typed Go clients: on the previous<br />int64 field, omitempty marshalled 0 as absent and the apiserver<br />served it back as 90, so raw YAML was the only way to say 0.<br />In-process readers must use EffectiveTerminationGracePeriod()<br />(env_validation.go), which mirrors the CRD default for objects<br />that never crossed the apiserver.<br />(Optional) defaults to 90 seconds | 90 | Minimum: 0 <br /> |
| `keeparchive` _boolean_ | KeepArchive is used by fetcher to determine if the extracted archive<br />or unarchived file should be placed, which is then used by specialize handler.<br />(This is mainly for the JVM environment because .jar is one kind of zip archive.) |  |  |
| `imagepullsecret` _string_ | ImagePullSecret is the secret for Kubernetes to pull an image from a<br />private registry. |  |  |


#### EnvironmentStatus



EnvironmentStatus describes the observed state of an Environment.



_Appears in:_
- [Environment](#environment)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### ExecutionStrategy



ExecutionStrategy specifies low-level parameters for function execution,
such as the number of instances.

MinScale affects the cold start behavior for a function. If MinScale is 0 then the
deployment is created on first invocation of function and is good for requests of
asynchronous nature. If MinScale is greater than 0 then MinScale number of pods are
created at the time of creation of function. This ensures faster response during first
invocation at the cost of consuming resources.

MaxScale is the maximum number of pods that function will scale to based on TargetCPUPercent
and resources allocated to the function pod.



_Appears in:_
- [InvokeStrategy](#invokestrategy)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `ExecutorType` _[ExecutorType](#executortype)_ | ExecutorType is the executor type of function used. Defaults to "poolmgr".<br />Available value:<br /> - poolmgr<br /> - newdeploy<br /> - container |  |  |
| `MinScale` _integer_ | This is only for newdeploy to set up minimum replicas of deployment. |  |  |
| `MaxScale` _integer_ | This is only for newdeploy to set up maximum replicas of deployment. |  |  |
| `TargetCPUPercent` _integer_ | Deprecated: use hpaMetrics instead.<br />This is only for executor type newdeploy and container to set up target CPU utilization of HPA.<br />Applicable for executor type newdeploy and container. |  |  |
| `SpecializationTimeout` _integer_ | This is the timeout setting for executor to wait for pod specialization. |  |  |
| `hpaMetrics` _[MetricSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#metricspec-v2-autoscaling) array_ | hpaMetrics is the list of metrics used to determine the desired replica count of the Deployment<br />created for the function.<br />Applicable for executor type newdeploy and container. |  |  |
| `hpaBehavior` _[HorizontalPodAutoscalerBehavior](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#horizontalpodautoscalerbehavior-v2-autoscaling)_ | hpaBehavior is the behavior of HPA when scaling in up/down direction.<br />Applicable for executor type newdeploy and container. |  |  |


#### ExecutorType

_Underlying type:_ _string_

ExecutorType is the primary executor for an environment



_Appears in:_
- [ExecutionStrategy](#executionstrategy)

| Field | Description |
| --- | --- |
| `poolmgr` |  |
| `newdeploy` |  |
| `container` |  |


#### FailureType

_Underlying type:_ _string_

FailureType refers to the type of failure



_Appears in:_
- [CanaryConfigSpec](#canaryconfigspec)

| Field | Description |
| --- | --- |
| `status-code` | failure type currently supported is http status code. This could be extended<br />in the future.<br /> |


#### FissionTenant



FissionTenant onboards a Kubernetes namespace for Fission. It is the
cluster-scoped source of truth the tenant-lifecycle controller reconciles
into the live resource-namespace set (and, in later phases, per-namespace
RBAC, service accounts, and auth keys). Setting the label
fission.io/enabled=true on a Namespace is sugar the controller
materializes into one of these. See docs/multiple-namespace/prd.md.



_Appears in:_
- [FissionTenantList](#fissiontenantlist)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `FissionTenant` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[FissionTenantSpec](#fissiontenantspec)_ |  |  |  |
| `status` _[FissionTenantStatus](#fissiontenantstatus)_ |  |  |  |


#### FissionTenantList



FissionTenantList is a list of FissionTenants.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `FissionTenantList` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `items` _[FissionTenant](#fissiontenant) array_ |  |  |  |


#### FissionTenantSpec



FissionTenantSpec declares which namespace Fission manages and, optionally,
where that tenant's function and builder workloads run.



_Appears in:_
- [FissionTenant](#fissiontenant)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `namespace` _string_ | Namespace is the Kubernetes namespace this tenant onboards. It is the<br />immutable join key to the live Namespace. |  | MaxLength: 63 <br />MinLength: 1 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |
| `functionNamespace` _string_ | FunctionNamespace, if set, is where this tenant's function pods and<br />Services run; empty means they run in spec.namespace. Generalizes the<br />deprecated cluster-global FISSION_FUNCTION_NAMESPACE to a per-tenant<br />mapping. |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |
| `builderNamespace` _string_ | BuilderNamespace, if set, is where this tenant's builder pods run;<br />empty means they run in spec.namespace. |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |


#### FissionTenantStatus



FissionTenantStatus reports the controller's progress onboarding the tenant.



_Appears in:_
- [FissionTenant](#fissiontenant)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ | ObservedGeneration is the spec generation the controller last reconciled. |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ | Conditions are the latest observations of the tenant's state:<br />RBACProvisioned, ServiceAccountsReady, AuthKeyProvisioned, WatchActive,<br />and the Ready rollup. |  |  |


#### Function



Function is function runs within environment runtime with given package and secrets/configmaps.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `Function` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[FunctionSpec](#functionspec)_ |  |  |  |
| `status` _[FunctionStatus](#functionstatus)_ |  |  |  |


#### FunctionAlias



FunctionAlias is a mutable, named pointer at one (or, during a weighted
rollout, two) FunctionVersion(s) of a Function (RFC-0025). Aliases are
what triggers reference in production; moving an alias is how a rollout
or rollback happens without touching the trigger.



_Appears in:_
- [FunctionAliasList](#functionaliaslist)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `FunctionAlias` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[FunctionAliasSpec](#functionaliasspec)_ |  |  |  |
| `status` _[FunctionAliasStatus](#functionaliasstatus)_ |  |  |  |


#### FunctionAliasList



FunctionAliasList is a list of FunctionAliases.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `FunctionAliasList` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `items` _[FunctionAlias](#functionalias) array_ |  |  |  |


#### FunctionAliasSpec



Repo convention (types.go:755,778,955): guard BOTH absent and explicit-empty on optional strings.



_Appears in:_
- [FunctionAlias](#functionalias)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `functionName` _string_ |  |  | MaxLength: 63 <br /> |
| `version` _string_ | Version pins by FunctionVersion name (imperative path). XOR PackageDigest. |  |  |
| `packageDigest` _string_ | PackageDigest pins declaratively (GitOps): resolved asynchronously to<br />the FunctionVersion that recorded this digest; eventually consistent. |  | Pattern: `^sha256:[a-f0-9]\{64\}$` <br /> |
| `weight` _integer_ | Weight (0-100) served by the primary target; nil = 100%. |  | Maximum: 100 <br />Minimum: 0 <br /> |
| `secondaryVersion` _string_ | SecondaryVersion receives 100-Weight. Name-pinned only. |  |  |


#### FunctionAliasStatus



FunctionAliasStatus describes the observed state of a FunctionAlias.



_Appears in:_
- [FunctionAlias](#functionalias)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `resolvedVersion` _string_ | ResolvedVersion is the FunctionVersion name this alias currently<br />resolves to (always name-pinned, even when Spec.PackageDigest<br />declares the target declaratively). |  |  |
| `history` _[AliasTargetRecord](#aliastargetrecord) array_ | History is a bounded tail of previously resolved targets, most<br />recent last. |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### FunctionPackageRef



FunctionPackageRef includes the reference to the package also the entrypoint of package.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `packageref` _[PackageRef](#packageref)_ | Package reference |  |  |
| `functionName` _string_ | FunctionName specifies a specific function within the package. This allows<br />functions to share packages, by having different functions within the same<br />package.<br />Fission itself does not interpret this path. It is passed verbatim to<br />build and runtime environments.<br />This is optional: if unspecified, the environment has a default name. |  |  |


#### FunctionReference



FunctionReference refers to a function



_Appears in:_
- [DestinationRef](#destinationref)
- [HTTPTriggerSpec](#httptriggerspec)
- [KubernetesWatchTriggerSpec](#kuberneteswatchtriggerspec)
- [MessageQueueTriggerSpec](#messagequeuetriggerspec)
- [TimeTriggerSpec](#timetriggerspec)
- [WorkflowBranchState](#workflowbranchstate)
- [WorkflowState](#workflowstate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[FunctionReferenceType](#functionreferencetype)_ | Type indicates whether this function reference is by name or selector. For now,<br />the only supported reference type is by "name".  Future reference types:<br />  * Function by label or annotation<br />  * Branch or tag of a versioned function<br />  * A "rolling upgrade" from one version of a function to another<br />Available value:<br />- name<br />- function-weights |  | Enum: [name function-weights] <br /> |
| `name` _string_ | Name of the function. Bounded to a DNS-1123 label length: the CEL<br />rule on this type needs the schema bound so the apiserver's cost<br />estimator can price the regex — without it, embedding the type<br />under a map (WorkflowSpec.States) blows the per-CRD cost budget. |  | MaxLength: 63 <br /> |
| `alias` _string_ | Alias, when set, targets a FunctionAlias by name instead of the live<br />Function directly (RFC-0025): the alias is a movable pointer that the<br />router resolves at request time to whatever FunctionVersion it<br />currently points at, so repointing the alias (e.g. for a canary<br />rollout or a rollback) redirects traffic without touching this<br />reference. Valid only when Type is "name"; mutually exclusive with<br />Version. Empty (the default) preserves today's behavior: route<br />straight to the live Function. |  | MaxLength: 63 <br /> |
| `version` _string_ | Version, when set, pins this reference to one FunctionVersion CR by<br />name (RFC-0025) — an immutable published snapshot that never moves,<br />unlike Alias. Valid only when Type is "name"; mutually exclusive<br />with Alias. Empty (the default) preserves today's behavior: route<br />straight to the live Function. |  | MaxLength: 63 <br /> |
| `functionweights` _object (keys:string, values:integer)_ | Function Reference by weight. this map contains function name as key and its weight<br />as the value. This is for canary upgrade purpose. |  |  |


#### FunctionReferenceType

_Underlying type:_ _string_

FunctionReferenceType refers to type of Function



_Appears in:_
- [FunctionReference](#functionreference)



#### FunctionSpec



FunctionSpec describes the contents of the function.
Bounded podspec safety rules — CEL admission gate for the simple pod-level
invariants. Per-container SecurityContext checks stay in the webhook
(ValidatePodSpecSafety) because iterating containers exceeds the CEL cost
budget; the rules here cover only the bounded, cheap cases. The has()
guards on each scalar are required: PodSpec's bool/string fields are
json:"...,omitempty" so a zero/empty value is OMITTED from the object,
and CEL errors with "no such key" if the rule accesses an absent field.



_Appears in:_
- [Function](#function)
- [FunctionVersionSpec](#functionversionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `environment` _[EnvironmentReference](#environmentreference)_ | Environment is the build and runtime environment that this function is<br />associated with. An Environment with this name should exist, otherwise the<br />function cannot be invoked. |  |  |
| `package` _[FunctionPackageRef](#functionpackageref)_ | Reference to a package containing deployment and optionally the source. |  |  |
| `secrets` _[SecretReference](#secretreference) array_ | Reference to a list of secrets. |  |  |
| `configmaps` _[ConfigMapReference](#configmapreference) array_ | Reference to a list of configmaps. |  |  |
| `env` _[EnvVar](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#envvar-v1-core) array_ | Env lists per-function environment variables set on the function's<br />runtime container: literals, plus key-level references into<br />same-namespace Secrets/ConfigMaps via valueFrom (secretKeyRef /<br />configMapKeyRef only — fieldRef and resourceFieldRef are rejected at<br />admission because poolmgr's specialize-time injection cannot honor<br />pod-level field refs portably; RFC-0030 §1). Function Env wins over<br />EnvFrom, which wins over the environment podspec's merged env.<br />Platform-reserved names (FISSION_*, RESOURCE_VERSION_COUNT, and the<br />interpreter/proxy-hijack set) are denied at admission and enforced<br />at injection. Additive and backward compatible. |  |  |
| `envFrom` _[EnvFromSource](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#envfromsource-v1-core) array_ | EnvFrom projects whole same-namespace Secrets/ConfigMaps into the<br />function's environment, with an optional prefix; later sources win<br />over earlier ones (Kubernetes semantics), and function Env literals<br />win over all EnvFrom keys.<br />Two phase-1 limits, both inherent to native (kubelet) injection:<br />the kubelet expands envFrom BEFORE container env, so a name the<br />environment podspec sets as a literal still beats an EnvFrom-supplied<br />key of the same name; and reserved platform names appearing as data<br />keys of a referenced object are not filtered (they are unknowable at<br />admission and mutable afterwards) — they are only shadowed by the<br />platform vars actually present on the container. Key-level filtering<br />and full precedence arrive with the poolmgr phase, which resolves<br />values itself. Additive and backward compatible. |  |  |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#resourcerequirements-v1-core)_ | cpu and memory resources as per K8S standards<br />This is only for newdeploy to set up resource limitation<br />when creating deployment for a function. |  |  |
| `InvokeStrategy` _[InvokeStrategy](#invokestrategy)_ | InvokeStrategy is a set of controls which affect how function executes |  |  |
| `functionTimeout` _integer_ | FunctionTimeout provides a maximum amount of duration within which a request for<br />a particular function execution should be complete.<br />This is optional. If not specified default value will be taken as 60s |  |  |
| `idletimeout` _integer_ | IdleTimeout specifies the length of time that a function is idle before the<br />function pod(s) are eligible for deletion. If no traffic to the function<br />is detected within the idle timeout, the executor will then recycle the<br />function pod(s) to release resources. |  |  |
| `streaming` _[StreamingConfig](#streamingconfig)_ | Streaming opts this function into the router's streaming invocation path:<br />incremental flushing, an idle/max timeout split, and a router-driven pod<br />keepalive for the connection's lifetime. When nil (the default) the function<br />uses the classic buffered, retry-on-transient-error proxy path with a single<br />FunctionTimeout deadline. Additive and backward compatible. |  |  |
| `tool` _[ToolConfig](#toolconfig)_ | Tool, when non-nil, advertises this function as a Model Context Protocol<br />(MCP) tool on the fission-bundle --mcpPort server. The MCP server watches<br />Function CRDs and hot-updates its tool list from this field. Presence is<br />the on switch (like Streaming): nil (the default) means the function is<br />never advertised as a tool. Additive and backward compatible. |  |  |
| `state` _[StateConfig](#stateconfig)_ | State, when non-nil, opts this function into the RFC-0023 keyed-state<br />API: a scoped statesvc keyspace backed by the RFC-0021 statestore, with<br />a per-function token injected at specialization time. Presence is the<br />on switch (like Streaming and Tool): nil (the default) means exactly<br />today's behavior. Additive and backward compatible. |  |  |
| `invocation` _[InvocationConfig](#invocationconfig)_ | Invocation, when non-nil, tunes RFC-0024 asynchronous invocation<br />(X-Fission-Invoke-Mode: async) for this function: the durable retry policy<br />and the maximum event age before an undelivered invocation is<br />dead-lettered. A function without it still accepts async mode with platform<br />defaults; this field only tunes them. Additive and backward compatible. |  |  |
| `concurrency` _integer_ | Maximum number of pods to be specialized which will serve requests<br />This is optional. If not specified default value will be taken as 500 |  |  |
| `requestsPerPod` _integer_ | RequestsPerPod indicates the maximum number of concurrent requests that can be served by a specialized pod<br />This is optional. If not specified default value will be taken as 1 |  |  |
| `onceOnly` _boolean_ | OnceOnly specifies if specialized pod will serve exactly one request in its lifetime and would be garbage collected after serving that one request<br />This is optional. If not specified default value will be taken as false |  |  |
| `retainPods` _integer_ | RetainPods specifies the number of specialized pods that should be retained after serving requests<br />This is optional. If not specified default value will be taken as 0 |  |  |
| `provisionedConcurrency` _[ProvisionedConcurrencyConfig](#provisionedconcurrencyconfig)_ | ProvisionedConcurrency, when non-nil, opts this function into eager<br />pre-warming of specialized pods (RFC-0026). The executor's provisioner<br />keeps at least the configured Target specialized pods warm, published to<br />the function's headless Service, and exempt from the idle reaper. nil<br />(the default) is the classic on-demand cold-start path. Additive and<br />backward compatible. Only valid when<br />InvokeStrategy.ExecutionStrategy.ExecutorType is poolmgr. |  |  |
| `versioning` _[VersioningConfig](#versioningconfig)_ | Versioning, when non-nil, opts this function into RFC-0025 immutable<br />version snapshots and named aliases. Presence is the on switch (like<br />Streaming and Tool): nil (the default) means exactly today's mutable<br />in-place behavior. Additive and backward compatible. |  |  |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#podspec-v1-core)_ | Podspec specifies podspec to use for executor type container based functions<br />Different arguments mentioned for container based function are populated inside a pod. |  |  |


#### FunctionStatus



FunctionStatus describes the observed state of a Function.



_Appears in:_
- [Function](#function)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ | ObservedGeneration reflects the .metadata.generation that the<br />controller observed when it last updated the status. |  |  |
| `provisionedReady` _integer_ | ProvisionedReady is the number of warm specialized pods the provisioner<br />is currently maintaining for this function (RFC-0026). Only meaningful<br />when Spec.ProvisionedConcurrency is non-nil. Reported by the executor's<br />provisioner on each reconcile pass. |  |  |
| `provisionedTarget` _integer_ | ProvisionedTarget is the effective target the provisioner is currently<br />aiming for (base Target, or a schedule-window override in PR 2). Lets<br />`fission fn get` show "3/5 provisioned pods ready". |  |  |
| `provisionedSpecTarget` _integer_ | ProvisionedSpecTarget is the raw Target from spec (before the namespace<br />cap clamp). When ProvisionedSpecTarget > ProvisionedTarget, the<br />provisioner clamped the target to the namespace cap<br />(executor.provisionedConcurrency.maxPerFunction) and the Provisioned<br />condition carries reason ProvisionedClamped. Lets `fission fn get`<br />show the spec-vs-effective divergence. |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ | Conditions represent the latest observations of the function's state. |  |  |


#### FunctionVersion



FunctionVersion is an immutable snapshot of a Function's spec at publish
time (RFC-0025). Versions are minted by the version-control loop (auto
mode) or `fission fn publish` (manual mode) and are never mutated after
creation — only garbage collected once unreferenced by any FunctionAlias
and beyond the retain floor. FunctionVersion carries no Status: its
content is fixed at creation, so there is nothing to reconcile.



_Appears in:_
- [FunctionVersionList](#functionversionlist)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `FunctionVersion` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[FunctionVersionSpec](#functionversionspec)_ |  |  |  |


#### FunctionVersionList



FunctionVersionList is a list of FunctionVersions.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `FunctionVersionList` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `items` _[FunctionVersion](#functionversion) array_ |  |  |  |


#### FunctionVersionSpec



FunctionVersionSpec is the immutable snapshot recorded by one publish.



_Appears in:_
- [FunctionVersion](#functionversion)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `functionName` _string_ |  |  | MaxLength: 63 <br /> |
| `functionUID` _[UID](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#uid-types-pkg)_ | FunctionUID and FunctionGeneration pin the executor identity of this<br />snapshot: (UID, Generation) is the pool/cache key (crd.CacheKeyUG),<br />so a version is a generation pin, not a new identity. |  |  |
| `functionGeneration` _integer_ |  |  |  |
| `sequence` _integer_ |  |  | Minimum: 1 <br /> |
| `snapshot` _[FunctionSpec](#functionspec)_ | Snapshot is the function spec at publish time with Versioning<br />zeroed (never nested) and, for legacy packages, PackageRef<br />repointed at the version-owned snapshot Package. |  |  |
| `packageDigest` _string_ | PackageDigest pins content: the OCI digest or sha256:<archive checksum>. |  |  |
| `envObservedGeneration` _integer_ | Environment observation at publish time (observational, not pinning). |  |  |
| `envRuntimeImage` _string_ |  |  |  |
| `publishedAt` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ |  |  |  |


#### GatewayParentRef



GatewayParentRef references a Gateway (and optionally a specific listener)
that the generated HTTPRoute attaches to. It mirrors the subset of
gateway.networking.k8s.io ParentReference that Fission needs.



_Appears in:_
- [GatewayRouteConfig](#gatewayrouteconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | Name of the parent Gateway. |  |  |
| `namespace` _string_ | Namespace of the parent Gateway. Defaults to the router's namespace<br />when empty. A non-empty, different namespace needs a ReferenceGrant. |  |  |
| `sectionName` _string_ | SectionName selects a specific listener on the Gateway. Empty attaches<br />to all compatible listeners. |  |  |
| `port` _integer_ | Port narrows attachment to a specific Gateway listener port. |  | Maximum: 65535 <br />Minimum: 1 <br /> |


#### GatewayRouteConfig



GatewayRouteConfig is the Gateway-API-specific portion of a RouteConfig.



_Appears in:_
- [RouteConfig](#routeconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `parentRefs` _[GatewayParentRef](#gatewayparentref) array_ | ParentRefs are the Gateways the generated HTTPRoute attaches to. The<br />referenced Gateways are owned by the cluster operator (Fission does<br />not create Gateways or GatewayClasses). A cross-namespace parentRef<br />requires a ReferenceGrant in the Gateway's namespace. |  |  |


#### HTTPTrigger



HTTPTrigger is the trigger invokes user functions when receiving HTTP requests.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `HTTPTrigger` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[HTTPTriggerSpec](#httptriggerspec)_ |  |  |  |
| `status` _[HTTPTriggerStatus](#httptriggerstatus)_ |  |  |  |


#### HTTPTriggerCorsConfig



HTTPTriggerCorsConfig is the per-HTTPTrigger CORS allowlist.
It is consumed by the router public listener to attach a CORS
middleware to the trigger's route. Triggers without a CorsConfig
receive no Access-Control-* response headers and therefore deny
cross-origin browser reads at the Same-Origin Policy layer.



_Appears in:_
- [HTTPTriggerSpec](#httptriggerspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `allowOrigins` _string array_ | AllowOrigins is the list of allowed origins (scheme + host +<br />port). Use ["*"] to allow any origin. Mixing "*" with<br />AllowCredentials=true is a configuration error and is<br />rejected by validation; browsers refuse the response in that<br />combination. |  |  |
| `allowMethods` _string array_ | AllowMethods is the list of HTTP methods echoed in the<br />Access-Control-Allow-Methods preflight response. When empty<br />the trigger's existing Methods field is used. |  |  |
| `allowHeaders` _string array_ | AllowHeaders is the list of request headers the browser is<br />allowed to send, echoed in Access-Control-Allow-Headers. |  |  |
| `exposeHeaders` _string array_ | ExposeHeaders is the list of response headers exposed to<br />the browser, set in Access-Control-Expose-Headers. |  |  |
| `allowCredentials` _boolean_ | AllowCredentials sets Access-Control-Allow-Credentials.<br />When true, AllowOrigins MUST NOT contain "*". |  |  |
| `maxAge` _string_ | MaxAge is the preflight cache lifetime as parsed by<br />time.ParseDuration. Empty means the header is omitted. |  |  |


#### HTTPTriggerSpec



HTTPTriggerSpec is for router to expose user functions at the given URL path.



_Appears in:_
- [HTTPTrigger](#httptrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `host` _string_ | Deprecated: the original idea of this field is not for setting Ingress.<br />Since we have IngressConfig now, remove Host after couple releases. |  | Pattern: `^([a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*)?$` <br /> |
| `relativeurl` _string_ | RelativeURL is the exposed URL for external client to access a function with. |  |  |
| `prefix` _string_ | Prefix with which functions are exposed.<br />NOTE: Prefix takes precedence over URL/RelativeURL.<br />Note that it does not treat slashes specially ("/foobar/" will be matched by<br />the prefix "/foobar"). |  |  |
| `keepPrefix` _boolean_ | When function is exposed with Prefix based path,<br />keepPrefix decides whether to keep or trim prefix in URL while invoking function. |  |  |
| `method` _string_ | Use Methods instead of Method. This field is going to be deprecated in a future release<br />HTTP method to access a function. |  | Enum: [ GET HEAD POST PUT PATCH DELETE CONNECT OPTIONS TRACE] <br /> |
| `methods` _string array_ | HTTP methods to access a function |  | items:Enum: [GET HEAD POST PUT PATCH DELETE CONNECT OPTIONS TRACE] <br /> |
| `invocationMode` _string_ | InvocationMode, when "async", forces every request to this trigger into<br />RFC-0024 asynchronous invocation even without the X-Fission-Invoke-Mode<br />header (webhooks from third parties cannot set headers). "" (the default)<br />leaves the per-request header in control. |  | Enum: [ async] <br /> |
| `functionref` _[FunctionReference](#functionreference)_ | FunctionReference is a reference to the target function. |  |  |
| `createingress` _boolean_ | If CreateIngress is true, router will create an ingress definition.<br />Deprecated: the Kubernetes Ingress API is frozen. Use RouteConfig<br />(with Provider "gateway") to expose functions through the Gateway API<br />instead. CreateIngress + IngressConfig keep working for the<br />deprecation window but will be removed in a future release. |  |  |
| `ingressconfig` _[IngressConfig](#ingressconfig)_ | IngressConfig for router to set up Ingress.<br />Deprecated: superseded by RouteConfig. See CreateIngress. |  |  |
| `routeConfig` _[RouteConfig](#routeconfig)_ | RouteConfig declares how the router exposes this trigger through an<br />external route provider (Ingress or the Gateway API). It is the<br />provider-neutral successor to CreateIngress + IngressConfig: when set<br />it takes precedence over those fields. Leave nil to expose the<br />function only through the router's own URL. |  |  |
| `corsConfig` _[HTTPTriggerCorsConfig](#httptriggercorsconfig)_ | CorsConfig configures CORS response headers for browser<br />callers of this trigger. When nil, the router emits no<br />Access-Control-* headers and the browser's Same-Origin<br />Policy enforces cluster isolation from cross-origin pages<br />(the deny-by-default behaviour). Set this field to<br />allowlist specific origins for SPAs that legitimately<br />call this trigger cross-origin. |  |  |


#### HTTPTriggerStatus



HTTPTriggerStatus describes the observed state of an HTTPTrigger.



_Appears in:_
- [HTTPTrigger](#httptrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### IngressConfig



IngressConfig is for router to set up Ingress.
Deprecated: superseded by RouteConfig. The Kubernetes Ingress API is
frozen; use RouteConfig with Provider "gateway" for new triggers.



_Appears in:_
- [HTTPTriggerSpec](#httptriggerspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `annotations` _object (keys:string, values:string)_ | Annotations will be added to metadata when creating Ingress. |  |  |
| `path` _string_ | Path is for path matching. The format of path<br />depends on what ingress controller you used. |  |  |
| `host` _string_ | Host is for ingress controller to apply rules. If<br />host is empty or "*", the rule applies to all<br />inbound HTTP traffic. |  |  |
| `tls` _string_ | TLS is for user to specify a Secret that contains<br />TLS key and certificate. The domain name in the<br />key and crt must match the value of Host field. |  |  |


#### InvocationConfig



InvocationConfig tunes RFC-0024 asynchronous invocation for a function.
Presence of the enclosing FunctionSpec.Invocation is optional — a function
without it still accepts async mode (X-Fission-Invoke-Mode: async) with
platform defaults; this struct only tunes them. Field bounds are validated in
Go (InvocationConfig.Validate, run at admission via validateForAdmission),
not CEL, because metav1.Duration CEL rules are unproven in this CRD.
An external dead-letter target is a later RFC-0024 phase.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `retry` _[RetryPolicy](#retrypolicy)_ | Retry is the durable delivery retry policy. The zero value means platform<br />defaults (a bounded exponential backoff over DefaultMaxAttempts attempts). |  |  |
| `maxAge` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | MaxAge caps how long an invocation may wait for successful delivery,<br />measured from its enqueue time; once exceeded it is dead-lettered with<br />reason "expired". nil means the platform default. Must be > 0 when set. |  |  |
| `onSuccess` _[DestinationRef](#destinationref)_ | OnSuccess, when set, invokes a destination with a Lambda-shaped result<br />envelope after the invocation is delivered successfully (2xx). |  |  |
| `onFailure` _[DestinationRef](#destinationref)_ | OnFailure, when set, invokes a destination with the result envelope after<br />the invocation permanently fails (a non-retryable 4xx, the retry budget<br />spent, or MaxAge exceeded). |  |  |


#### InvokeStrategy



InvokeStrategy is a set of controls over how the function executes.
It affects the performance and resource usage of the function.

An InvokeStrategy is of one of two types: ExecutionStrategy, which controls low-level
parameters such as which ExecutorType to use, when to autoscale, minimum and maximum
number of running instances, etc. A higher-level AbstractInvokeStrategy will also be
supported; this strategy would specify the target request rate of the function,
the target latency statistics, and the target cost (in terms of compute resources).



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `ExecutionStrategy` _[ExecutionStrategy](#executionstrategy)_ | ExecutionStrategy specifies low-level parameters for function execution,<br />such as the number of instances. |  |  |
| `StrategyType` _[StrategyType](#strategytype)_ | StrategyType is the strategy type of function.<br />Now it only supports 'execution'. |  |  |


#### KubernetesWatchTrigger



KubernetesWatchTrigger watches kubernetes resource events and invokes functions.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `KubernetesWatchTrigger` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[KubernetesWatchTriggerSpec](#kuberneteswatchtriggerspec)_ |  |  |  |
| `status` _[KubernetesWatchTriggerStatus](#kuberneteswatchtriggerstatus)_ |  |  |  |


#### KubernetesWatchTriggerSpec



KubernetesWatchTriggerSpec defines spec of KuberenetesWatchTrigger



_Appears in:_
- [KubernetesWatchTrigger](#kuberneteswatchtrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `namespace` _string_ |  |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |
| `type` _string_ | Type of resource to watch (Pod, Service, etc.) |  |  |
| `labelselector` _object (keys:string, values:string)_ | Resource labels |  |  |
| `functionref` _[FunctionReference](#functionreference)_ | The reference to a function for kubewatcher to invoke with<br />when receiving events. |  |  |


#### KubernetesWatchTriggerStatus



KubernetesWatchTriggerStatus describes the observed state of a KubernetesWatchTrigger.



_Appears in:_
- [KubernetesWatchTrigger](#kuberneteswatchtrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### MessageQueueTrigger



MessageQueueTrigger invokes functions when messages arrive to certain topic that trigger subscribes to.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `MessageQueueTrigger` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[MessageQueueTriggerSpec](#messagequeuetriggerspec)_ |  |  |  |
| `status` _[MessageQueueTriggerStatus](#messagequeuetriggerstatus)_ |  |  |  |


#### MessageQueueTriggerSpec



MessageQueueTriggerSpec defines a binding from a topic in a
message queue to a function.



_Appears in:_
- [MessageQueueTrigger](#messagequeuetrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `functionref` _[FunctionReference](#functionreference)_ | The reference to a function for message queue trigger to invoke with<br />when receiving messages from subscribed topic. |  |  |
| `messageQueueType` _[MessageQueueType](#messagequeuetype)_ | Type of message queue (NATS, Kafka, AzureQueue) |  |  |
| `topic` _string_ | Subscribed topic |  |  |
| `respTopic` _string_ | Topic for message queue trigger to sent response from function. |  |  |
| `errorTopic` _string_ | Topic to collect error response sent from function |  |  |
| `maxRetries` _integer_ | Maximum times for message queue trigger to retry |  |  |
| `contentType` _string_ | Content type of payload |  |  |
| `pollingInterval` _integer_ | The period to check each trigger source on every ScaledObject, and scale the deployment up or down accordingly |  |  |
| `cooldownPeriod` _integer_ | The period to wait after the last trigger reported active before scaling the deployment back to 0 |  |  |
| `minReplicaCount` _integer_ | Minimum number of replicas KEDA will scale the deployment down to |  |  |
| `maxReplicaCount` _integer_ | Maximum number of replicas KEDA will scale the deployment up to |  |  |
| `metadata` _object (keys:string, values:string)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `secret` _string_ | Secret name |  |  |
| `mqtkind` _string_ | Kind of Message Queue Trigger to be created, by default its fission |  |  |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#podspec-v1-core)_ | (Optional) Podspec allows modification of deployed runtime pod with Kubernetes PodSpec<br />The merging logic is briefly described below and detailed MergePodSpec function<br />- Volumes mounts and env variables for function and fetcher container are appended<br />- All additional containers and init containers are appended<br />- Volume definitions are appended<br />- Lists such as tolerations, ImagePullSecrets, HostAliases are appended<br />- Structs are merged and variables from pod spec take precedence |  |  |


#### MessageQueueTriggerStatus



MessageQueueTriggerStatus describes the observed state of a MessageQueueTrigger.



_Appears in:_
- [MessageQueueTrigger](#messagequeuetrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### MessageQueueType

_Underlying type:_ _string_

MessageQueueType refers to Type of message queue



_Appears in:_
- [MessageQueueTriggerSpec](#messagequeuetriggerspec)
- [TopicRef](#topicref)



#### OCIArchive



OCIArchive references an OCI image whose flattened filesystem
contains the deployment code (RFC-0001). The environment runtime
image stays the pod's main container; only how the code reaches
the shared volume changes.



_Appears in:_
- [Archive](#archive)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `image` _string_ | Image is a fully qualified OCI reference: registry/repo:tag[@digest]. |  | MinLength: 1 <br /> |
| `imagePullSecrets` _[LocalObjectReference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#localobjectreference-v1-core) array_ | ImagePullSecrets are resolved when pulling the image. The<br />fetcher-pull path passes them to the in-fetcher keychain; the<br />image-volume path sets them on pod.Spec.ImagePullSecrets.<br />They must exist in the namespace the function pods run in —<br />the function's own namespace, or the configured function<br />namespace for default-namespace functions. |  |  |
| `subPath` _string_ | SubPath points at the deployment root inside the image<br />filesystem, as a clean relative path; empty means the image<br />root. It must be a directory: the image-volume path mounts it<br />via the pod volumeMount subPath, and kubelets reject file<br />subpaths on image volumes. |  |  |
| `digest` _string_ | Digest is an optional content hash validated on pull. |  | Pattern: `^sha256:[a-f0-9]\{64\}$` <br /> |


#### Package



Package Think of these as function-level images.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `Package` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[PackageSpec](#packagespec)_ |  |  |  |
| `status` _[PackageStatus](#packagestatus)_ | Status indicates the build status of package. |  |  |


#### PackageRef



PackageRef is a reference to the package.



_Appears in:_
- [FunctionPackageRef](#functionpackageref)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `namespace` _string_ |  |  |  |
| `name` _string_ | The package reference is optional, so Name is omitempty: when unset it<br />is omitted from the object and the Pattern below is skipped (a function<br />may legitimately have no package). A present name must be a DNS-1123<br />label. A leaf Pattern (cheap structural validation) is used rather than<br />a spec-level CEL matches() (which would exceed the cost budget). |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |
| `resourceversion` _string_ | Including resource version in the reference forces the function to be updated on<br />package update, making it possible to cache the function based on its metadata. |  |  |


#### PackageSpec



PackageSpec includes source/deploy archives and the reference of environment to build the package.



_Appears in:_
- [Package](#package)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `environment` _[EnvironmentReference](#environmentreference)_ | Environment is a reference to the environment for building source archive. |  |  |
| `source` _[Archive](#archive)_ | Source is the archive contains source code and dependencies file.<br />If the package status is in PENDING state, builder manager will then<br />notify builder to compile source and save the result as deployable archive. |  |  |
| `deployment` _[Archive](#archive)_ | Deployment is the deployable archive that environment runtime used to run user function. |  |  |
| `buildcmd` _string_ | BuildCommand is a custom build command that builder used to build the source archive. |  |  |


#### PackageStatus



PackageStatus contains the build status of a package also the build log for examination.



_Appears in:_
- [Package](#package)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `buildstatus` _[BuildStatus](#buildstatus)_ | BuildStatus is the package build status. | pending | Enum: [ pending running succeeded failed none] <br /> |
| `buildlog` _string_ | BuildLog stores build log during the compilation. |  |  |
| `contentHash` _string_ | ContentHash fingerprints the package's INPUT content (RFC-0029 §3):<br />the source archive when one is present, otherwise the deployment<br />archive. A source package's deployment is the build's own product,<br />so folding it in would make every successful build look like a<br />fresh change and rebuild forever.<br />It is what makes a Git-applied Package<br />converge without the CLI: buildermgr compares the spec's current<br />hash against this one to decide whether the content actually<br />changed, rather than relying on the CLI's status->pending poke.<br />It also covers packages that never build. A deploy-only or OCI<br />package settles at BuildStatusNone, so the build-success path that<br />re-stamps referencing Functions never runs for it — exactly the<br />digest-pinned-OCI-in-Git golden path. Keying the re-stamp on this<br />hash instead covers both shapes on one code path.<br />An EMPTY value means "not yet recorded" and must never read as<br />"changed": every package has an empty hash on the first reconcile<br />after this ships, and treating that as a change would rebuild the<br />whole cluster at once. The reconciler seeds it without rebuilding. |  |  |
| `lastUpdateTimestamp` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ | LastUpdateTimestamp will store the timestamp the package was last updated<br />metav1.Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.<br />https://github.com/kubernetes/apimachinery/blob/44bd77c24ef93cd3a5eb6fef64e514025d10d44e/pkg/apis/meta/v1/time.go#L26-L35 |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ | Conditions represent the latest observations of the package's state. |  |  |


#### ProvisionedConcurrencyConfig



ProvisionedConcurrencyConfig opts this function into eager pre-warming of
specialized pods (RFC-0026). Presence is the on switch: nil (the default)
means the function uses the classic on-demand cold-start path. When non-nil,
the executor's provisioner keeps at least Target specialized pods warm and
published to the function's headless Service, exempt from the idle reaper.
Additive and backward compatible.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `target` _integer_ | Target is the base number of warm specialized pods to maintain outside<br />any schedule window. Must be >= 1. Schedule windows may override this<br />(see Windows). Bounded by the namespace cap<br />(executor.provisionedConcurrency.maxPerFunction, default 20). |  | Minimum: 1 <br /> |
| `windows` _[ProvisionedWindow](#provisionedwindow) array_ | Windows is an optional list of schedule windows that override Target<br />during specific time ranges (RFC-0026 PR 2). Empty in PR 1 — base Target<br />is always in effect. Each window: a cron start expression, a duration,<br />and a window-local target (0 means "un-warm" for the window's duration). |  | MaxItems: 32 <br /> |


#### ProvisionedWindow



ProvisionedWindow describes a schedule window that overrides the base
ProvisionedConcurrencyConfig.Target during a time range. The window is
active from the cron-triggered start for Duration; while active, the
effective target is the window's Target (overlapping windows take the max).



_Appears in:_
- [ProvisionedConcurrencyConfig](#provisionedconcurrencyconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `name` _string_ | Name identifies this window within the function's<br />ProvisionedConcurrencyConfig.Windows list. Must be unique within the<br />list (listMapKey=name). |  | MaxLength: 63 <br />MinLength: 1 <br /> |
| `start` _string_ | Start is a cron expression (5-field, robfig/cron, same parser as<br />TimeTrigger) marking when each window instance opens. Prefix with<br />"CRON_TZ=<zone>" (e.g. "CRON_TZ=America/New_York 0 9 * * *") to<br />evaluate the schedule in a fixed timezone. Without a CRON_TZ<br />prefix, the schedule is evaluated in the executor process's local<br />timezone (UTC unless the deployment is configured otherwise) —<br />this is intended behavior, not a default that may change; specify<br />CRON_TZ explicitly if the window must not shift when the<br />executor's local timezone changes. |  | MinLength: 1 <br /> |
| `duration` _string_ | Duration is how long each window instance stays open. Format is Go<br />time.ParseDuration (e.g. "12h", "30m"). Must be > 0. |  | Pattern: `^[0-9]+(ns\|us\|µs\|ms\|s\|m\|h)$` <br /> |
| `target` _integer_ | Target is the effective target while the window is open. 0 means<br />"un-warm" — provisioned pods are drained for the window's duration. |  | Minimum: 0 <br /> |


#### RetryPolicy



RetryPolicy is the async delivery retry policy: the attempt budget and the
exponential-backoff schedule between delivery attempts. All fields are
optional; a nil field takes the platform default.



_Appears in:_
- [InvocationConfig](#invocationconfig)
- [WorkflowBranchState](#workflowbranchstate)
- [WorkflowSpec](#workflowspec)
- [WorkflowState](#workflowstate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `maxAttempts` _integer_ | MaxAttempts is the total number of delivery attempts before the invocation<br />is dead-lettered. nil means DefaultMaxAttempts. Must be >= 1 when set. |  |  |
| `backoffBase` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | BackoffBase is the delay before the first retry; it grows exponentially per<br />attempt up to BackoffCap. nil means the platform default. Must be >= 0. |  |  |
| `backoffCap` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | BackoffCap bounds the per-retry backoff. nil means the platform default.<br />Must be >= 0 and >= BackoffBase when both are set. |  |  |
| `jitter` _boolean_ | Jitter, when non-nil and false, disables the randomized jitter the<br />dispatcher otherwise adds to each backoff to avoid synchronized retries.<br />nil means the platform default (jitter enabled). |  |  |


#### RouteConfig



RouteConfig declares how the router exposes an HTTPTrigger through an
external route provider. It is the provider-neutral successor to the
deprecated CreateIngress + IngressConfig fields: the router routes it to
the matching RouteProvider based on Provider.



_Appears in:_
- [HTTPTriggerSpec](#httptriggerspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `provider` _[RouteProviderType](#routeprovidertype)_ | Provider selects the route provider that reconciles this trigger's<br />external route. "ingress" creates a networking.k8s.io Ingress (the<br />deprecated path); "gateway" creates a gateway.networking.k8s.io<br />HTTPRoute attached to an operator-managed Gateway. The "gateway"<br />provider must be enabled on the router (GATEWAY_API_ENABLED). |  | Enum: [ingress gateway] <br /> |
| `hostnames` _string array_ | Hostnames the route matches. For the gateway provider these become<br />the HTTPRoute hostnames; for the ingress provider only the first is<br />used as the Ingress rule host. Empty matches all hosts. |  |  |
| `path` _string_ | Path is the request path the route matches (must be absolute, start<br />with '/'). Defaults to "/" when empty. |  |  |
| `annotations` _object (keys:string, values:string)_ | Annotations are added to the generated route object (Ingress or<br />HTTPRoute). Use these for implementation-specific configuration<br />understood by your Ingress controller or Gateway implementation. |  |  |
| `tls` _string_ | TLS names a Secret holding the TLS key and certificate. It applies to<br />the ingress provider only; with the gateway provider TLS termination<br />is configured on the Gateway listener and this field is ignored. |  |  |
| `gateway` _[GatewayRouteConfig](#gatewayrouteconfig)_ | Gateway holds Gateway-API-specific configuration. Required (at least<br />one parentRef) when Provider is "gateway", unless the router is<br />configured with a default Gateway parentRef. |  |  |


#### RouteProviderType

_Underlying type:_ _string_

RouteProviderType selects how the router exposes an HTTPTrigger externally.
It is the type of RouteConfig.Provider; the allowed values are the constants
below (also enforced by the field's kubebuilder Enum marker).



_Appears in:_
- [RouteConfig](#routeconfig)

| Field | Description |
| --- | --- |
| `ingress` | RouteProviderIngress creates a networking.k8s.io Ingress (deprecated).<br /> |
| `gateway` | RouteProviderGateway creates a gateway.networking.k8s.io HTTPRoute.<br /> |




#### Runtime



Runtime is the setting for environment runtime.
Bounded podspec / container safety rules — CEL admission gate for the
simple, bounded fields. Per-container PodSpec.containers iteration stays
in the webhook (ValidatePodSpecSafety / ValidateContainerSafety) because
it exceeds the CEL cost budget. The has() guards are required because
json:"...,omitempty" omits zero/empty values from the object.



_Appears in:_
- [EnvironmentSpec](#environmentspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `image` _string_ | Image for containing the language runtime. |  |  |
| `container` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#container-v1-core)_ | (Optional) Container allows the modification of the deployed runtime<br />container using the Kubernetes Container spec. Fission overrides<br />the following fields:<br />- Name<br />- Image; set to the Runtime.Image<br />- TerminationMessagePath<br />- ImagePullPolicy<br />You can set either PodSpec or Container, but not both.<br />kubebuilder:validation:XPreserveUnknownFields=true |  |  |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#podspec-v1-core)_ | (Optional) Podspec allows modification of deployed runtime pod with Kubernetes PodSpec<br />The merging logic is briefly described below and detailed MergePodSpec function<br />- Volumes mounts and env variables for function and fetcher container are appended<br />- All additional containers and init containers are appended<br />- Volume definitions are appended<br />- Lists such as tolerations, ImagePullSecrets, HostAliases are appended<br />- Structs are merged and variables from pod spec take precedence<br />You can set either PodSpec or Container, but not both. |  |  |


#### SecretReference



SecretReference is a reference to a kubernetes secret.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `namespace` _string_ |  |  |  |
| `name` _string_ |  |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` <br /> |
| `mountPath` _string_ | MountPath redirects this secret's file projection from the default<br />/secrets/<namespace>/<name> to the given path, which is relative to<br />the /secrets root (RFC-0030 §4): generic pool pods share a fixed<br />volume set frozen at pool creation, so an arbitrary absolute path is<br />not materializable there, and the container executor applies the<br />same constraint for cross-executor consistency. Empty keeps today's<br /><namespace>/<name> layout, so functions that do not set it are<br />unaffected. No two secrets on one function may RESOLVE to the same<br />directory (an explicit path colliding with another reference's<br />default counts): the final segment written is the object's data<br />key and keys are mutable after admission, so sharing a directory<br />would let one object's later-added key collide with the other's<br />file; the fetcher refuses such a write rather than truncating.<br />Honoured on every executor: poolmgr and newdeploy via the fetcher,<br />the container executor via a native projected volume. Not supported<br />on an allowedFunctionsPerContainer:infinite environment, whose pods<br />share one secrets tree across functions. |  |  |


#### StateConfig



StateConfig declares a function's keyed-state keyspace and quotas
(RFC-0023). Presence of the enclosing FunctionSpec.State is the on switch —
there is no separate enabled flag, so the in-memory zero value and the
stored object never disagree (the same rationale as StreamingConfig).



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `keyspace` _string_ | Keyspace names the durable keyspace this function reads and writes.<br />Defaults to the function name; explicit so a function can be renamed<br />without orphaning its data. The charset deliberately excludes ':' and<br />'#' — ':' is a token-derivation info-string separator and '#' marks the<br />platform-reserved "<keyspace>#meta" quota-accounting sibling. |  | MaxLength: 63 <br />Pattern: `^[a-z0-9]([-a-z0-9.]*[a-z0-9])?$` <br /> |
| `defaultTTL` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | DefaultTTL, when set, is applied to writes that carry no explicit TTL.<br />Must be >= 0; zero (or nil) means keys do not expire by default. |  |  |
| `maxValueBytes` _integer_ | MaxValueBytes caps a single value's size. 0 means the platform default<br />(DefaultStateMaxValueBytes, 256KiB). Blobs belong in object storage. |  | Minimum: 0 <br /> |
| `maxKeys` _integer_ | MaxKeys caps the number of live keys in the keyspace, enforced<br />atomically with each write (quota.tla S3). 0 means the platform<br />default (DefaultStateMaxKeys). |  | Minimum: 0 <br /> |
| `backend` _string_ | Backend selects a named statestore driver for this keyspace. Accepted<br />and validated in v1 but not yet acted on: statesvc serves every<br />keyspace from its single configured driver (per-function backend<br />selection is a documented deferral). |  |  |
| `sticky` _[StickyConfig](#stickyconfig)_ | Sticky, when non-nil, opts the function into sticky routing: the<br />router consistent-hashes the declared request key onto the ready-pod<br />set so one key's requests land on one pod while the pod set is stable.<br />Best-effort (an optimization, never a correctness dependency — S6):<br />durable truth stays behind the state API. |  |  |


#### StickyConfig



StickyConfig declares how the sticky routing key is extracted from a
request. Requests missing the key fall back to the default endpoint pick.



_Appears in:_
- [StateConfig](#stateconfig)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `source` _[StickySource](#stickysource)_ | Source is where to look for the key. |  | Enum: [header queryparam] <br /> |
| `name` _string_ | Name is the header or query-parameter name holding the key,<br />e.g. "X-Session-Id". |  |  |


#### StickySource

_Underlying type:_ _string_

StickySource selects where the router extracts the sticky routing key
from an incoming request.

_Validation:_
- Enum: [header queryparam]

_Appears in:_
- [StickyConfig](#stickyconfig)

| Field | Description |
| --- | --- |
| `header` |  |
| `queryparam` |  |


#### StrategyType

_Underlying type:_ _string_

StrategyType is the strategy to be used for function execution



_Appears in:_
- [InvokeStrategy](#invokestrategy)



#### StreamingConfig



StreamingConfig controls the router's streaming behavior for a function.
Presence is the on switch: a non-nil Streaming enables the streaming path,
nil (the default) is the classic buffered path. There is no separate enabled
flag, so the in-memory zero value and the stored object never disagree.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `protocol` _[StreamingProtocol](#streamingprotocol)_ | Protocol hints how the router proxies the response. | auto | Enum: [auto sse chunked websocket] <br /> |
| `idleTimeoutSeconds` _integer_ | IdleTimeoutSeconds is the maximum time the router waits without bytes flowing<br />from the function before it aborts the stream; reset on every chunk. 0 means<br />use the package default (DefaultStreamIdleSeconds). |  | Minimum: 0 <br /> |
| `maxDurationSeconds` _integer_ | MaxDurationSeconds is an optional hard ceiling on total stream lifetime<br />regardless of activity. 0 (the default) means no ceiling — the idle<br />timeout governs. A streaming function does NOT inherit FunctionTimeout as<br />a ceiling; that total-wall-clock cap is exactly what streaming escapes. |  | Minimum: 0 <br /> |


#### StreamingProtocol

_Underlying type:_ _string_

StreamingProtocol selects how the router treats the upstream response.

_Validation:_
- Enum: [auto sse chunked websocket]

_Appears in:_
- [StreamingConfig](#streamingconfig)

| Field | Description |
| --- | --- |
| `auto` | StreamingAuto flushes immediately and lets the upstream decide the framing<br />(SSE, chunked, or a WebSocket Upgrade); the safe default.<br /> |
| `sse` |  |
| `chunked` |  |
| `websocket` |  |


#### TimeTrigger



TimeTrigger invokes functions based on given cron schedule.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `TimeTrigger` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[TimeTriggerSpec](#timetriggerspec)_ |  |  |  |
| `status` _[TimeTriggerStatus](#timetriggerstatus)_ |  |  |  |


#### TimeTriggerSpec



TimeTriggerSpec invokes the specific function at a time or
times specified by a cron string.



_Appears in:_
- [TimeTrigger](#timetrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `cron` _string_ | Cron schedule |  |  |
| `functionref` _[FunctionReference](#functionreference)_ | The reference to function. Alias is read from the embedded<br />FunctionReference.Alias (RFC-0025) — TimeTriggerSpec has no field of<br />its own for it, so there is exactly one JSON path (spec.functionref.alias)<br />and one Go path (spec.Alias, promoted) for the concept, never two<br />competing ones. The timer publisher (a later RFC-0025 task) reads it<br />the same way timer.go:80 already reads the promoted spec.Name today. |  |  |
| `method` _string_ | HTTP Method for trigger, ex : GET, POST, PUT, DELETE, HEAD (default: "POST") | POST |  |
| `subpath` _string_ | Subpath to trigger a specific route if function<br />internally supports routing, (default: "/") | / |  |


#### TimeTriggerStatus



TimeTriggerStatus describes the observed state of a TimeTrigger.



_Appears in:_
- [TimeTrigger](#timetrigger)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### ToolConfig



ToolConfig declares how a Function is exposed as an MCP (Model Context
Protocol) tool. The MCP server reuses the function's existing internal
invocation path; this struct only declares the agent-facing tool contract.
Presence of the enclosing FunctionSpec.Tool is the on switch — there is no
separate enabled flag, so the in-memory zero value and the stored object
never disagree (the same rationale as StreamingConfig).



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `description` _string_ | Description is the human/agent-facing tool description surfaced in the MCP<br />tools/list response. Required. |  |  |
| `inputSchema` _[JSON](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#json-v1-apiextensions-k8s-io)_ | InputSchema is the JSON Schema (draft 2020-12) for the tool's arguments,<br />surfaced verbatim as the MCP tool inputSchema. Stored as raw JSON so the<br />CRD does not constrain the schema shape. When empty the tool advertises an<br />open object schema (\{"type":"object"\}). |  |  |
| `toolName` _string_ | ToolName overrides the advertised tool name. Defaults to<br />"<namespace>-<function name>". Must match ^[a-zA-Z0-9_-]\{1,64\}$. |  | Pattern: `^[a-zA-Z0-9_-]\{1,64\}$` <br /> |
| `alias` _string_ | Alias, when set, targets a FunctionAlias by name (RFC-0025) instead of<br />the live Function: the MCP registry serves the tool from the alias's<br />currently-resolved FunctionVersion snapshot, and tools/call is proxied<br />to the ":<alias>" route rather than straight to the live Function.<br />Empty (the default) preserves today's behavior. Router/registry-side<br />resolution lands in a later RFC-0025 task — until then this field is<br />accepted but inert. |  | MaxLength: 63 <br /> |


#### TopicRef



TopicRef is a message-queue topic destination for an async invocation result.
Topics are namespace-scoped: the destination publishes to the source
function's namespace (RFC-0024 rule R6).



_Appears in:_
- [DestinationRef](#destinationref)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `messageQueueType` _[MessageQueueType](#messagequeuetype)_ | MessageQueueType selects the provider: "statestore" (the RFC-0027<br />built-in, no broker) now; broker types (e.g. kafka) with the egress phase. |  |  |
| `topic` _string_ | Topic is the topic the result envelope is published to. The schema bounds<br />mirror ValidateTopicName: a stream-safe charset excluding "/" so the<br />topic/<namespace>/<topic> mapping cannot alias across namespaces. |  | MaxLength: 249 <br />Pattern: `^[a-zA-Z0-9._-]+$` <br /> |




#### ValidationErrorType

_Underlying type:_ _integer_





_Appears in:_
- [ValidationError](#validationerror)



#### VersioningConfig



VersioningConfig opts a Function into RFC-0025 immutable version
snapshots and named aliases.



_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `mode` _[VersioningMode](#versioningmode)_ | Mode auto (default) mints a version on every runtime-affecting<br />update once the referenced package build succeeds; manual mints<br />only on explicit `fission fn publish`. | auto | Enum: [auto manual] <br /> |
| `retain` _integer_ | Retain bounds unaliased version history per function (GC floor 1).<br />Defaults to 10. Alias-referenced versions are never GC'd. |  | Minimum: 1 <br /> |


#### VersioningMode

_Underlying type:_ _string_

VersioningMode selects when versions are minted.

_Validation:_
- Enum: [auto manual]

_Appears in:_
- [VersioningConfig](#versioningconfig)

| Field | Description |
| --- | --- |
| `auto` |  |
| `manual` |  |


#### Workflow



Workflow declares a durable state machine whose task states are Fission
functions (RFC-0022). The engine executes WorkflowRuns against a snapshot
of this spec embedded in the run's event stream; editing a Workflow never
changes in-flight runs.



_Appears in:_
- [WorkflowList](#workflowlist)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `Workflow` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[WorkflowSpec](#workflowspec)_ |  |  |  |
| `status` _[WorkflowStatus](#workflowstatus)_ |  |  |  |


#### WorkflowBranch



WorkflowBranch is one concurrent sub-machine of a Parallel state (or
the iterator template of a Map state).



_Appears in:_
- [WorkflowState](#workflowstate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `startAt` _string_ |  |  |  |
| `states` _object (keys:string, values:[WorkflowBranchState](#workflowbranchstate))_ | MaxProperties=20 (vs 100 top-level) keeps the apiserver's CEL cost<br />estimate for doubly-nested rules under budget — the phase-1 lesson. |  | MaxProperties: 20 <br />MinProperties: 1 <br /> |


#### WorkflowBranchState



WorkflowBranchState is WorkflowState minus the fan-out fields: nested
Parallel/Map is impossible BY TYPE, which is what keeps the CRD schema
non-recursive (controller-gen cannot render a self-referential type).



_Appears in:_
- [WorkflowBranch](#workflowbranch)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[WorkflowStateType](#workflowstatetype)_ |  |  | Enum: [Task Choice Parallel Map Wait Succeed Fail] <br /> |
| `function` _[FunctionReference](#functionreference)_ |  |  |  |
| `duration` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ |  |  |  |
| `timeout` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ |  |  |  |
| `retry` _[RetryPolicy](#retrypolicy)_ |  |  |  |
| `catch` _[WorkflowCatchRoute](#workflowcatchroute) array_ |  |  |  |
| `choices` _[WorkflowChoiceRule](#workflowchoicerule) array_ |  |  |  |
| `default` _string_ |  |  |  |
| `inputPath` _string_ |  |  |  |
| `resultPath` _string_ |  |  |  |
| `outputPath` _string_ |  |  |  |
| `next` _string_ |  |  |  |
| `end` _boolean_ |  |  |  |


#### WorkflowCatchRoute



WorkflowCatchRoute routes a matched error class to a next state.



_Appears in:_
- [WorkflowBranchState](#workflowbranchstate)
- [WorkflowState](#workflowstate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `errorType` _string_ | ErrorType matches a typed function error (\{"errorType": ...\} body),<br />a built-in class (Fission.PermanentError, Fission.FunctionError,<br />Fission.Timeout), or Fission.All (matches anything). |  |  |
| `next` _string_ |  |  |  |
| `resultPath` _string_ | ResultPath, when set, merges the error object<br />(\{"errorType": ..., "cause": ...\}) into the flowing document at<br />this JSONPath, so the catch target still sees the business data<br />(e.g. retry a charge after a grace period). Unset keeps the<br />Step-Functions-parity default: the error object REPLACES the<br />document. |  |  |


#### WorkflowChoiceCondition



WorkflowChoiceCondition is a leaf comparison against the state input.
Exactly one operator must be set. Numeric values use resource.Quantity
(CRDs cannot carry floats; Quantity accepts YAML numbers and strings).



_Appears in:_
- [WorkflowChoiceRule](#workflowchoicerule)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `variable` _string_ | Variable is a JSONPath into the state's (shaped) input. Required on<br />every leaf condition — enforced by the webhook, not the schema: this<br />struct is inline-embedded in WorkflowChoiceRule, and a<br />schema-required field would wrongly reject composite (and/or/not)<br />rules that carry no inline leaf. |  |  |
| `stringEquals` _string_ |  |  |  |
| `numericEquals` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#quantity-resource-api)_ |  |  |  |
| `numericGreaterThan` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#quantity-resource-api)_ |  |  |  |
| `numericLessThan` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#quantity-resource-api)_ |  |  |  |
| `booleanEquals` _boolean_ |  |  |  |
| `isPresent` _boolean_ |  |  |  |
| `isNull` _boolean_ |  |  |  |


#### WorkflowChoiceRule



WorkflowChoiceRule is one ordered rule of a Choice state: either a leaf
condition (inline) or exactly one of And/Or/Not over leaf conditions
(depth-1 composition; deeper nesting is additive later).



_Appears in:_
- [WorkflowBranchState](#workflowbranchstate)
- [WorkflowState](#workflowstate)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `variable` _string_ | Variable is a JSONPath into the state's (shaped) input. Required on<br />every leaf condition — enforced by the webhook, not the schema: this<br />struct is inline-embedded in WorkflowChoiceRule, and a<br />schema-required field would wrongly reject composite (and/or/not)<br />rules that carry no inline leaf. |  |  |
| `stringEquals` _string_ |  |  |  |
| `numericEquals` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#quantity-resource-api)_ |  |  |  |
| `numericGreaterThan` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#quantity-resource-api)_ |  |  |  |
| `numericLessThan` _[Quantity](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#quantity-resource-api)_ |  |  |  |
| `booleanEquals` _boolean_ |  |  |  |
| `isPresent` _boolean_ |  |  |  |
| `isNull` _boolean_ |  |  |  |
| `and` _[WorkflowChoiceCondition](#workflowchoicecondition) array_ |  |  |  |
| `or` _[WorkflowChoiceCondition](#workflowchoicecondition) array_ |  |  |  |
| `not` _[WorkflowChoiceCondition](#workflowchoicecondition)_ |  |  |  |
| `next` _string_ | Next names the state to transition to when this rule matches. |  |  |


#### WorkflowList



WorkflowList is a list of Workflows.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `WorkflowList` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `items` _[Workflow](#workflow) array_ |  |  |  |


#### WorkflowRetentionPolicy



WorkflowRetentionPolicy bounds retained history for finished runs.



_Appears in:_
- [WorkflowSpec](#workflowspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `maxCount` _integer_ |  |  |  |
| `maxAge` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ |  |  |  |


#### WorkflowRun



WorkflowRun is one execution of a Workflow. Full step history lives in
the statestore EventLog stream for the run, never in etcd; status carries
a bounded tail for kubectl visibility.



_Appears in:_
- [WorkflowRunList](#workflowrunlist)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `WorkflowRun` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `spec` _[WorkflowRunSpec](#workflowrunspec)_ |  |  |  |
| `status` _[WorkflowRunStatus](#workflowrunstatus)_ |  |  |  |


#### WorkflowRunEventSummary



WorkflowRunEventSummary is one bounded-tail history entry for kubectl
visibility; the full history lives in the statestore EventLog.



_Appears in:_
- [WorkflowRunStatus](#workflowrunstatus)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `seq` _integer_ |  |  |  |
| `type` _string_ |  |  |  |
| `state` _string_ |  |  |  |
| `attempt` _integer_ |  |  |  |
| `at` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ |  |  |  |
| `note` _string_ |  |  |  |


#### WorkflowRunList



WorkflowRunList is a list of WorkflowRuns.





| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `apiVersion` _string_ | `fission.io/v1` | | |
| `kind` _string_ | `WorkflowRunList` | | |
| `kind` _string_ | Kind is a string value representing the REST resource this object represents.<br />Servers may infer this from the endpoint the client submits requests to.<br />Cannot be updated.<br />In CamelCase.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |  |  |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object.<br />Servers should convert recognized schemas to the latest internal value, and<br />may reject unrecognized values.<br />More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |  |  |
| `metadata` _[ListMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#listmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |  |  |
| `items` _[WorkflowRun](#workflowrun) array_ |  |  |  |


#### WorkflowRunPhase

_Underlying type:_ _string_

WorkflowRunPhase is the run's coarse lifecycle phase.

_Validation:_
- Enum: [Pending Running Succeeded Failed Cancelled TimedOut]

_Appears in:_
- [WorkflowRunStatus](#workflowrunstatus)

| Field | Description |
| --- | --- |
| `Pending` |  |
| `Running` |  |
| `Succeeded` |  |
| `Failed` |  |
| `Cancelled` |  |
| `TimedOut` |  |


#### WorkflowRunSpec



WorkflowRunSpec identifies the Workflow to execute and the run's input.



_Appears in:_
- [WorkflowRun](#workflowrun)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `workflowRef` _string_ | WorkflowRef names the Workflow (same namespace) this run executes. |  |  |
| `workflowGeneration` _integer_ | WorkflowGeneration records (for observability) which Workflow<br />generation this run executes. It is NOT the pinning mechanism: the<br />authoritative spec is the snapshot the engine embeds in the run's<br />event stream at RunStarted; a Workflow edit or deletion mid-run can<br />neither fork nor strand a run. Set by the CLI; 0 means unknown. |  |  |
| `input` _[JSON](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#json-v1-apiextensions-k8s-io)_ | Input is the run's initial input document — ANY JSON value<br />(apiextensionsv1.JSON, not RawExtension: the RawExtension schema is<br />type=object and the apiserver would reject a bare string/array/<br />number). Webhook-capped at 256KiB (etcd objects cap at ~1.5MiB) —<br />pass larger inputs by reference. |  |  |


#### WorkflowRunStatus



WorkflowRunStatus describes the observed state of a WorkflowRun.



_Appears in:_
- [WorkflowRun](#workflowrun)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `phase` _[WorkflowRunPhase](#workflowrunphase)_ |  |  | Enum: [Pending Running Succeeded Failed Cancelled TimedOut] <br /> |
| `activeStates` _string array_ | ActiveStates lists the state names currently executing. |  |  |
| `startedAt` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ |  |  |  |
| `finishedAt` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ |  |  |  |
| `output` _[JSON](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#json-v1-apiextensions-k8s-io)_ | Output holds the final output inline up to the step-I/O spill<br />threshold — ANY JSON value (see Input for why apiextensionsv1.JSON);<br />larger outputs spill to the statestore KV and OutputRef points<br />there (the CLI dereferences). |  |  |
| `outputRef` _string_ |  |  |  |
| `errorType` _string_ | ErrorType and Cause carry the terminal failure classification so<br />kubectl answers "why did it fail" without the history endpoint.<br />Cause is bounded; the full detail lives in the run history. |  |  |
| `cause` _string_ |  |  | MaxLength: 1024 <br /> |
| `recentEvents` _[WorkflowRunEventSummary](#workflowruneventsummary) array_ | RecentEvents is a bounded (<=20) tail; full history is in the<br />EventLog. |  |  |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


#### WorkflowSpec



WorkflowSpec is a state machine: states are data, logic lives in
functions.



_Appears in:_
- [Workflow](#workflow)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `startAt` _string_ | StartAt names the state execution begins at. |  |  |
| `states` _object (keys:string, values:[WorkflowState](#workflowstate))_ | States is the state machine graph, keyed by state name. The size<br />bound mirrors validation.MaxWorkflowStates and lets the apiserver's<br />CEL cost estimator bound rules on nested types. |  | MaxProperties: 100 <br />MinProperties: 1 <br /> |
| `defaultRetry` _[RetryPolicy](#retrypolicy)_ | DefaultRetry applies to Task states that do not set their own Retry. |  |  |
| `timeout` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | Timeout bounds a whole run; expiry fails it with errorType<br />Fission.Timeout. Defaults to 24h (a mis-authored graph or endlessly<br />caught-and-retried loop must not hold an active run forever). |  |  |
| `historyRetention` _[WorkflowRetentionPolicy](#workflowretentionpolicy)_ | HistoryRetention bounds stored history (count + age) per finished run. |  |  |


#### WorkflowState



WorkflowState is one state in the machine. Exactly the fields for its
Type may be set (enforced at admission).



_Appears in:_
- [WorkflowSpec](#workflowspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[WorkflowStateType](#workflowstatetype)_ |  |  | Enum: [Task Choice Parallel Map Wait Succeed Fail] <br /> |
| `function` _[FunctionReference](#functionreference)_ | Function is the Task state's target. |  |  |
| `timeout` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | Timeout bounds one attempt of a Task invocation. |  |  |
| `retry` _[RetryPolicy](#retrypolicy)_ | Retry overrides the workflow's DefaultRetry for this Task. |  |  |
| `catch` _[WorkflowCatchRoute](#workflowcatchroute) array_ | Catch routes a failed Task (retries exhausted, or a permanent error)<br />to another state by matched errorType; first match wins. |  |  |
| `choices` _[WorkflowChoiceRule](#workflowchoicerule) array_ | Choices are the Choice state's ordered rules; first match wins. |  |  |
| `default` _string_ | Default names the state a Choice falls through to when no rule<br />matches; without it, no-match fails the run (Fission.NoChoiceMatched). |  |  |
| `branches` _[WorkflowBranch](#workflowbranch) array_ | Branches are the Parallel state's concurrent sub-machines (or the<br />Map state's single iterator template). Branch states cannot nest<br />further fan-out — enforced by the bounded WorkflowBranchState type. |  | MaxItems: 10 <br /> |
| `itemsPath` _string_ | ItemsPath selects the array a Map state iterates (one branch per<br />element, input = the element). |  |  |
| `duration` _[Duration](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#duration-v1-meta)_ | Duration is how long a Wait state pauses the run — durably: the<br />delay is a statestore Queue message, so a controller restart never<br />loses it (robfig/cron-style absolute schedules stay with the timer<br />subsystem; only durations here). |  |  |
| `maxConcurrency` _integer_ | MaxConcurrency throttles how many branches execute at once. Zero<br />means the engine default (10) — NOT unbounded: an unthrottled<br />large Map against poolmgr is a self-inflicted cold-start burst.<br />The default is applied by the engine, not the schema: a schema<br />default would stamp the field onto every state type. |  | Minimum: 0 <br /> |
| `inputPath` _string_ | InputPath/ResultPath/OutputPath shape step I/O with JSONPath<br />(Step Functions semantics; dialect pinned in pkg/workflow/expr). |  |  |
| `resultPath` _string_ |  |  |  |
| `outputPath` _string_ |  |  |  |
| `next` _string_ | Next names the state to run after this one; exactly one of Next/End<br />is set on Task states (Succeed/Fail are implicitly terminal). |  |  |
| `end` _boolean_ |  |  |  |


#### WorkflowStateType

_Underlying type:_ _string_

WorkflowStateType enumerates the state kinds the engine executes.

_Validation:_
- Enum: [Task Choice Parallel Map Wait Succeed Fail]

_Appears in:_
- [WorkflowBranchState](#workflowbranchstate)
- [WorkflowState](#workflowstate)

| Field | Description |
| --- | --- |
| `Task` |  |
| `Choice` |  |
| `Parallel` |  |
| `Map` |  |
| `Wait` |  |
| `Succeed` |  |
| `Fail` |  |


#### WorkflowStatus



WorkflowStatus describes the observed state of a Workflow.



_Appears in:_
- [Workflow](#workflow)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ |  |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ |  |  |  |


