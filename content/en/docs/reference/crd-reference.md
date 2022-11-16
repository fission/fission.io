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
- [Function](#function)
- [HTTPTrigger](#httptrigger)
- [KubernetesWatchTrigger](#kuberneteswatchtrigger)
- [MessageQueueTrigger](#messagequeuetrigger)
- [Package](#package)
- [TimeTrigger](#timetrigger)



#### AllowedFunctionsPerContainer

_Underlying type:_ `string`

AllowedFunctionsPerContainer defaults to 'single'. Related to Fission Workflows

_Appears in:_
- [EnvironmentSpec](#environmentspec)



#### Archive



Archive contains or references a collection of sources or binary files.

_Appears in:_
- [PackageSpec](#packagespec)

| Field | Description |
| --- | --- |
| `type` _[ArchiveType](#archivetype)_ | Type defines how the package is specified: literal or URL. Available value:  - literal  - url |
| `literal` _integer array_ | Literal contents of the package. Can be used for encoding packages below TODO (256 KB?) size. |
| `url` _string_ | URL references a package. |
| `checksum` _[Checksum](#checksum)_ | Checksum ensures the integrity of packages referenced by URL. Ignored for literals. |


#### ArchiveType

_Underlying type:_ `string`

ArchiveType is either literal or URL, indicating whether the package is specified in the Archive struct or externally.

_Appears in:_
- [Archive](#archive)





#### BuildStatus

_Underlying type:_ `string`

BuildStatus indicates the current build status of a package.

_Appears in:_
- [PackageStatus](#packagestatus)



#### Builder



Builder is the setting for environment builder.

_Appears in:_
- [EnvironmentSpec](#environmentspec)

| Field | Description |
| --- | --- |
| `image` _string_ | Image for containing the language compilation environment. |
| `command` _string_ | (Optional) Default build command to run for this build environment. |
| `container` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#container-v1-core)_ | (Optional) Container allows the modification of the deployed builder container using the Kubernetes Container spec. Fission overrides the following fields: - Name - Image; set to the Builder.Image - Command; set to the Builder.Command - TerminationMessagePath - ImagePullPolicy - ReadinessProbe |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#podspec-v1-core)_ | PodSpec will store the spec of the pod that will be applied to the pod created for the builder |


#### CanaryConfig



CanaryConfig is for canary deployment of two functions.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `CanaryConfig`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[CanaryConfigSpec](#canaryconfigspec)_ |  |
| `status` _[CanaryConfigStatus](#canaryconfigstatus)_ |  |


#### CanaryConfigSpec



CanaryConfigSpec defines the canary configuration spec

_Appears in:_
- [CanaryConfig](#canaryconfig)

| Field | Description |
| --- | --- |
| `trigger` _string_ | HTTP trigger that this config references |
| `newfunction` _string_ | New version of the function |
| `oldfunction` _string_ | Old stable version of the function |
| `weightincrement` _integer_ | Weight increment step for function |
| `duration` _string_ | Weight increment interval, string representation of time.Duration, ex : 1m, 2h, 2d (default: "2m") |
| `failurethreshold` _integer_ | Threshold in percentage beyond which the new version of the function is considered unstable |
| `failureType` _[FailureType](#failuretype)_ |  |


#### CanaryConfigStatus



CanaryConfigStatus represents canary config status

_Appears in:_
- [CanaryConfig](#canaryconfig)

| Field | Description |
| --- | --- |
| `status` _string_ |  |


#### Checksum



Checksum of package contents when the contents are stored outside the Package struct. Type is the checksum algorithm; "sha256" is the only currently supported one. Sum is hex encoded.

_Appears in:_
- [Archive](#archive)

| Field | Description |
| --- | --- |
| `type` _[ChecksumType](#checksumtype)_ |  |
| `sum` _string_ |  |


#### ChecksumType

_Underlying type:_ `string`

ChecksumType specifies the checksum algorithm, such as sha256, used for a checksum.

_Appears in:_
- [Checksum](#checksum)



#### ConfigMapReference



ConfigMapReference is a reference to a kubernetes configmap.

_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description |
| --- | --- |
| `namespace` _string_ |  |
| `name` _string_ |  |


#### Environment



Environment is environment for building and running user functions.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `Environment`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[EnvironmentSpec](#environmentspec)_ |  |


#### EnvironmentReference



EnvironmentReference is a reference to an environment.

_Appears in:_
- [FunctionSpec](#functionspec)
- [PackageSpec](#packagespec)

| Field | Description |
| --- | --- |
| `namespace` _string_ |  |
| `name` _string_ |  |


#### EnvironmentSpec



EnvironmentSpec contains with builder, runtime and some other related environment settings.

_Appears in:_
- [Environment](#environment)

| Field | Description |
| --- | --- |
| `version` _integer_ | Version is the Environment API version 
 Version "1" allows user to run code snippet in a file, and it's supported by most of the environments except tensorflow-serving. 
 Version "2" supports downloading and compiling user function if source archive is not empty. 
 Version "3" is almost the same with v2, but you're able to control the size of pre-warm pool of the environment. |
| `runtime` _[Runtime](#runtime)_ | Runtime is configuration for running function, like container image etc. |
| `builder` _[Builder](#builder)_ | (Optional) Builder is configuration for builder manager to launch environment builder to build source code into deployable binary. |
| `allowedFunctionsPerContainer` _[AllowedFunctionsPerContainer](#allowedfunctionspercontainer)_ | (Optional) defaults to 'single'. Fission workflow uses 'infinite' to load multiple functions in one function pod. Available value: - single - infinite |
| `allowAccessToExternalNetwork` _boolean_ | Istio default blocks all egress traffic for safety. To enable accessibility of external network for builder/function pod, set to 'true'. (Optional) defaults to 'false' |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#resourcerequirements-v1-core)_ | The request and limit CPU/MEM resource setting for poolmanager to set up pods in the pre-warm pool. (Optional) defaults to no limitation. |
| `poolsize` _integer_ | The initial pool size for environment |
| `terminationGracePeriod` _integer_ | The grace time for pod to perform connection draining before termination. The unit is in seconds. (Optional) defaults to 360 seconds |
| `keeparchive` _boolean_ | KeepArchive is used by fetcher to determine if the extracted archive or unarchived file should be placed, which is then used by specialize handler. (This is mainly for the JVM environment because .jar is one kind of zip archive.) |
| `imagepullsecret` _string_ | ImagePullSecret is the secret for Kubernetes to pull an image from a private registry. |


#### ExecutionStrategy



ExecutionStrategy specifies low-level parameters for function execution, such as the number of instances. 
 MinScale affects the cold start behavior for a function. If MinScale is 0 then the deployment is created on first invocation of function and is good for requests of asynchronous nature. If MinScale is greater than 0 then MinScale number of pods are created at the time of creation of function. This ensures faster response during first invocation at the cost of consuming resources. 
 MaxScale is the maximum number of pods that function will scale to based on TargetCPUPercent and resources allocated to the function pod.

_Appears in:_
- [InvokeStrategy](#invokestrategy)

| Field | Description |
| --- | --- |
| `ExecutorType` _[ExecutorType](#executortype)_ | ExecutorType is the executor type of function used. Defaults to "poolmgr". 
 Available value:  - poolmgr  - newdeploy  - container |
| `MinScale` _integer_ | This is only for newdeploy to set up minimum replicas of deployment. |
| `MaxScale` _integer_ | This is only for newdeploy to set up maximum replicas of deployment. |
| `TargetCPUPercent` _integer_ | Deprecated: use hpaMetrics instead. This is only for executor type newdeploy and container to set up target CPU utilization of HPA. Applicable for executor type newdeploy and container. |
| `SpecializationTimeout` _integer_ | This is the timeout setting for executor to wait for pod specialization. |
| `hpaMetrics` _[MetricSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#metricspec-v2beta2-autoscaling) array_ | hpaMetrics is the list of metrics used to determine the desired replica count of the Deployment created for the function. Applicable for executor type newdeploy and container. |
| `hpaBehavior` _[HorizontalPodAutoscalerBehavior](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#horizontalpodautoscalerbehavior-v2beta2-autoscaling)_ | hpaBehavior is the behavior of HPA when scaling in up/down direction. Applicable for executor type newdeploy and container. |


#### ExecutorType

_Underlying type:_ `string`

ExecutorType is the primary executor for an environment

_Appears in:_
- [ExecutionStrategy](#executionstrategy)



#### FailureType

_Underlying type:_ `string`

FailureType refers to the type of failure

_Appears in:_
- [CanaryConfigSpec](#canaryconfigspec)



#### Function



Function is function runs within environment runtime with given package and secrets/configmaps.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `Function`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[FunctionSpec](#functionspec)_ |  |


#### FunctionPackageRef



FunctionPackageRef includes the reference to the package also the entrypoint of package.

_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description |
| --- | --- |
| `packageref` _[PackageRef](#packageref)_ | Package reference |
| `functionName` _string_ | FunctionName specifies a specific function within the package. This allows functions to share packages, by having different functions within the same package. 
 Fission itself does not interpret this path. It is passed verbatim to build and runtime environments. 
 This is optional: if unspecified, the environment has a default name. |


#### FunctionReference



FunctionReference refers to a function

_Appears in:_
- [HTTPTriggerSpec](#httptriggerspec)
- [KubernetesWatchTriggerSpec](#kuberneteswatchtriggerspec)
- [MessageQueueTriggerSpec](#messagequeuetriggerspec)
- [TimeTriggerSpec](#timetriggerspec)

| Field | Description |
| --- | --- |
| `type` _[FunctionReferenceType](#functionreferencetype)_ | Type indicates whether this function reference is by name or selector. For now, the only supported reference type is by "name".  Future reference types:   * Function by label or annotation   * Branch or tag of a versioned function   * A "rolling upgrade" from one version of a function to another Available value: - name - function-weights |
| `name` _string_ | Name of the function. |
| `functionweights` _object (keys:string, values:integer)_ | Function Reference by weight. this map contains function name as key and its weight as the value. This is for canary upgrade purpose. |


#### FunctionReferenceType

_Underlying type:_ `string`

FunctionReferenceType refers to type of Function

_Appears in:_
- [FunctionReference](#functionreference)



#### FunctionSpec



FunctionSpec describes the contents of the function.

_Appears in:_
- [Function](#function)

| Field | Description |
| --- | --- |
| `environment` _[EnvironmentReference](#environmentreference)_ | Environment is the build and runtime environment that this function is associated with. An Environment with this name should exist, otherwise the function cannot be invoked. |
| `package` _[FunctionPackageRef](#functionpackageref)_ | Reference to a package containing deployment and optionally the source. |
| `secrets` _[SecretReference](#secretreference) array_ | Reference to a list of secrets. |
| `configmaps` _[ConfigMapReference](#configmapreference) array_ | Reference to a list of configmaps. |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#resourcerequirements-v1-core)_ | cpu and memory resources as per K8S standards This is only for newdeploy to set up resource limitation when creating deployment for a function. |
| `InvokeStrategy` _[InvokeStrategy](#invokestrategy)_ | InvokeStrategy is a set of controls which affect how function executes |
| `functionTimeout` _integer_ | FunctionTimeout provides a maximum amount of duration within which a request for a particular function execution should be complete. This is optional. If not specified default value will be taken as 60s |
| `idletimeout` _integer_ | IdleTimeout specifies the length of time that a function is idle before the function pod(s) are eligible for deletion. If no traffic to the function is detected within the idle timeout, the executor will then recycle the function pod(s) to release resources. |
| `concurrency` _integer_ | Maximum number of pods to be specialized which will serve requests This is optional. If not specified default value will be taken as 500 |
| `requestsPerPod` _integer_ | RequestsPerPod indicates the maximum number of concurrent requests that can be served by a specialized pod This is optional. If not specified default value will be taken as 1 |
| `onceOnly` _boolean_ | OnceOnly specifies if specialized pod will serve exactly one request in its lifetime and would be garbage collected after serving that one request This is optional. If not specified default value will be taken as false |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#podspec-v1-core)_ | Podspec specifies podspec to use for executor type container based functions Different arguments mentioned for container based function are populated inside a pod. |


#### HTTPTrigger



HTTPTrigger is the trigger invokes user functions when receiving HTTP requests.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `HTTPTrigger`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[HTTPTriggerSpec](#httptriggerspec)_ |  |


#### HTTPTriggerSpec



HTTPTriggerSpec is for router to expose user functions at the given URL path.

_Appears in:_
- [HTTPTrigger](#httptrigger)

| Field | Description |
| --- | --- |
| `host` _string_ | TODO: remove this field since we have IngressConfig already Deprecated: the original idea of this field is not for setting Ingress. Since we have IngressConfig now, remove Host after couple releases. |
| `relativeurl` _string_ | RelativeURL is the exposed URL for external client to access a function with. |
| `prefix` _string_ | Prefix with which functions are exposed. NOTE: Prefix takes precedence over URL/RelativeURL. Note that it does not treat slashes specially ("/foobar/" will be matched by the prefix "/foobar"). |
| `keepPrefix` _boolean_ | When function is exposed with Prefix based path, keepPrefix decides whether to keep or trim prefix in URL while invoking function. |
| `method` _string_ | Use Methods instead of Method. This field is going to be deprecated in a future release HTTP method to access a function. |
| `methods` _string array_ | HTTP methods to access a function |
| `functionref` _[FunctionReference](#functionreference)_ | FunctionReference is a reference to the target function. |
| `createingress` _boolean_ | If CreateIngress is true, router will create an ingress definition. |
| `ingressconfig` _[IngressConfig](#ingressconfig)_ | TODO: make IngressConfig an independent Fission resource IngressConfig for router to set up Ingress. |


#### IngressConfig



IngressConfig is for router to set up Ingress.

_Appears in:_
- [HTTPTriggerSpec](#httptriggerspec)

| Field | Description |
| --- | --- |
| `annotations` _object (keys:string, values:string)_ | Annotations will be added to metadata when creating Ingress. |
| `path` _string_ | Path is for path matching. The format of path depends on what ingress controller you used. |
| `host` _string_ | Host is for ingress controller to apply rules. If host is empty or "*", the rule applies to all inbound HTTP traffic. |
| `tls` _string_ | TLS is for user to specify a Secret that contains TLS key and certificate. The domain name in the key and crt must match the value of Host field. |


#### InvokeStrategy



InvokeStrategy is a set of controls over how the function executes. It affects the performance and resource usage of the function. 
 An InvokeStrategy is of one of two types: ExecutionStrategy, which controls low-level parameters such as which ExecutorType to use, when to autoscale, minimum and maximum number of running instances, etc. A higher-level AbstractInvokeStrategy will also be supported; this strategy would specify the target request rate of the function, the target latency statistics, and the target cost (in terms of compute resources).

_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description |
| --- | --- |
| `ExecutionStrategy` _[ExecutionStrategy](#executionstrategy)_ | ExecutionStrategy specifies low-level parameters for function execution, such as the number of instances. |
| `StrategyType` _[StrategyType](#strategytype)_ | StrategyType is the strategy type of function. Now it only supports 'execution'. |


#### KubernetesWatchTrigger



KubernetesWatchTrigger watches kubernetes resource events and invokes functions.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `KubernetesWatchTrigger`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[KubernetesWatchTriggerSpec](#kuberneteswatchtriggerspec)_ |  |


#### KubernetesWatchTriggerSpec



KubernetesWatchTriggerSpec defines spec of KuberenetesWatchTrigger

_Appears in:_
- [KubernetesWatchTrigger](#kuberneteswatchtrigger)

| Field | Description |
| --- | --- |
| `namespace` _string_ |  |
| `type` _string_ | Type of resource to watch (Pod, Service, etc.) |
| `labelselector` _object (keys:string, values:string)_ | Resource labels |
| `functionref` _[FunctionReference](#functionreference)_ | The reference to a function for kubewatcher to invoke with when receiving events. |


#### MessageQueueTrigger



MessageQueueTrigger invokes functions when messages arrive to certain topic that trigger subscribes to.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `MessageQueueTrigger`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[MessageQueueTriggerSpec](#messagequeuetriggerspec)_ |  |


#### MessageQueueTriggerSpec



MessageQueueTriggerSpec defines a binding from a topic in a message queue to a function.

_Appears in:_
- [MessageQueueTrigger](#messagequeuetrigger)

| Field | Description |
| --- | --- |
| `functionref` _[FunctionReference](#functionreference)_ | The reference to a function for message queue trigger to invoke with when receiving messages from subscribed topic. |
| `messageQueueType` _[MessageQueueType](#messagequeuetype)_ | Type of message queue (NATS, Kafka, AzureQueue) |
| `topic` _string_ | Subscribed topic |
| `respTopic` _string_ | Topic for message queue trigger to sent response from function. |
| `errorTopic` _string_ | Topic to collect error response sent from function |
| `maxRetries` _integer_ | Maximum times for message queue trigger to retry |
| `contentType` _string_ | Content type of payload |
| `pollingInterval` _integer_ | The period to check each trigger source on every ScaledObject, and scale the deployment up or down accordingly |
| `cooldownPeriod` _integer_ | The period to wait after the last trigger reported active before scaling the deployment back to 0 |
| `minReplicaCount` _integer_ | Minimum number of replicas KEDA will scale the deployment down to |
| `maxReplicaCount` _integer_ | Maximum number of replicas KEDA will scale the deployment up to |
| `metadata` _object (keys:string, values:string)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `secret` _string_ | Secret name |
| `mqtkind` _string_ | Kind of Message Queue Trigger to be created, by default its fission |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#podspec-v1-core)_ | (Optional) Podspec allows modification of deployed runtime pod with Kubernetes PodSpec The merging logic is briefly described below and detailed MergePodSpec function - Volumes mounts and env variables for function and fetcher container are appended - All additional containers and init containers are appended - Volume definitions are appended - Lists such as tolerations, ImagePullSecrets, HostAliases are appended - Structs are merged and variables from pod spec take precedence |


#### MessageQueueType

_Underlying type:_ `string`

MessageQueueType refers to Type of message queue

_Appears in:_
- [MessageQueueTriggerSpec](#messagequeuetriggerspec)



#### Package



Package Think of these as function-level images.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `Package`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[PackageSpec](#packagespec)_ |  |
| `status` _[PackageStatus](#packagestatus)_ | Status indicates the build status of package. |


#### PackageRef



PackageRef is a reference to the package.

_Appears in:_
- [FunctionPackageRef](#functionpackageref)

| Field | Description |
| --- | --- |
| `namespace` _string_ |  |
| `name` _string_ |  |
| `resourceversion` _string_ | Including resource version in the reference forces the function to be updated on package update, making it possible to cache the function based on its metadata. |


#### PackageSpec



PackageSpec includes source/deploy archives and the reference of environment to build the package.

_Appears in:_
- [Package](#package)

| Field | Description |
| --- | --- |
| `environment` _[EnvironmentReference](#environmentreference)_ | Environment is a reference to the environment for building source archive. |
| `source` _[Archive](#archive)_ | Source is the archive contains source code and dependencies file. If the package status is in PENDING state, builder manager will then notify builder to compile source and save the result as deployable archive. |
| `deployment` _[Archive](#archive)_ | Deployment is the deployable archive that environment runtime used to run user function. |
| `buildcmd` _string_ | BuildCommand is a custom build command that builder used to build the source archive. |


#### PackageStatus



PackageStatus contains the build status of a package also the build log for examination.

_Appears in:_
- [Package](#package)

| Field | Description |
| --- | --- |
| `buildstatus` _[BuildStatus](#buildstatus)_ | BuildStatus is the package build status. |
| `buildlog` _string_ | BuildLog stores build log during the compilation. |
| `lastUpdateTimestamp` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#time-v1-meta)_ | LastUpdateTimestamp will store the timestamp the package was last updated metav1.Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON. https://github.com/kubernetes/apimachinery/blob/44bd77c24ef93cd3a5eb6fef64e514025d10d44e/pkg/apis/meta/v1/time.go#L26-L35 |




#### Runtime



Runtime is the setting for environment runtime.

_Appears in:_
- [EnvironmentSpec](#environmentspec)

| Field | Description |
| --- | --- |
| `image` _string_ | Image for containing the language runtime. |
| `container` _[Container](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#container-v1-core)_ | (Optional) Container allows the modification of the deployed runtime container using the Kubernetes Container spec. Fission overrides the following fields: - Name - Image; set to the Runtime.Image - TerminationMessagePath - ImagePullPolicy 
 You can set either PodSpec or Container, but not both. kubebuilder:validation:XPreserveUnknownFields=true |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#podspec-v1-core)_ | (Optional) Podspec allows modification of deployed runtime pod with Kubernetes PodSpec The merging logic is briefly described below and detailed MergePodSpec function - Volumes mounts and env variables for function and fetcher container are appended - All additional containers and init containers are appended - Volume definitions are appended - Lists such as tolerations, ImagePullSecrets, HostAliases are appended - Structs are merged and variables from pod spec take precedence 
 You can set either PodSpec or Container, but not both. |


#### SecretReference



SecretReference is a reference to a kubernetes secret.

_Appears in:_
- [FunctionSpec](#functionspec)

| Field | Description |
| --- | --- |
| `namespace` _string_ |  |
| `name` _string_ |  |


#### StrategyType

_Underlying type:_ `string`

StrategyType is the strategy to be used for function execution

_Appears in:_
- [InvokeStrategy](#invokestrategy)



#### TimeTrigger



TimeTrigger invokes functions based on given cron schedule.



| Field | Description |
| --- | --- |
| `apiVersion` _string_ | `fission.io/v1`
| `kind` _string_ | `TimeTrigger`
| `kind` _string_ | Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds |
| `apiVersion` _string_ | APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources |
| `metadata` _[ObjectMeta](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#objectmeta-v1-meta)_ | Refer to Kubernetes API documentation for fields of `metadata`. |
| `spec` _[TimeTriggerSpec](#timetriggerspec)_ |  |


#### TimeTriggerSpec



TimeTriggerSpec invokes the specific function at a time or times specified by a cron string.

_Appears in:_
- [TimeTrigger](#timetrigger)

| Field | Description |
| --- | --- |
| `cron` _string_ | Cron schedule |
| `functionref` _[FunctionReference](#functionreference)_ | The reference to function |




