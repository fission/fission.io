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
| `terminationGracePeriod` _integer_ | The grace time for pod to perform connection draining before termination. The unit is in seconds.<br />(Optional) defaults to 360 seconds |  | Minimum: 0 <br /> |
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
- [HTTPTriggerSpec](#httptriggerspec)
- [KubernetesWatchTriggerSpec](#kuberneteswatchtriggerspec)
- [MessageQueueTriggerSpec](#messagequeuetriggerspec)
- [TimeTriggerSpec](#timetriggerspec)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `type` _[FunctionReferenceType](#functionreferencetype)_ | Type indicates whether this function reference is by name or selector. For now,<br />the only supported reference type is by "name".  Future reference types:<br />  * Function by label or annotation<br />  * Branch or tag of a versioned function<br />  * A "rolling upgrade" from one version of a function to another<br />Available value:<br />- name<br />- function-weights |  | Enum: [name function-weights] <br /> |
| `name` _string_ | Name of the function. |  |  |
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

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `environment` _[EnvironmentReference](#environmentreference)_ | Environment is the build and runtime environment that this function is<br />associated with. An Environment with this name should exist, otherwise the<br />function cannot be invoked. |  |  |
| `package` _[FunctionPackageRef](#functionpackageref)_ | Reference to a package containing deployment and optionally the source. |  |  |
| `secrets` _[SecretReference](#secretreference) array_ | Reference to a list of secrets. |  |  |
| `configmaps` _[ConfigMapReference](#configmapreference) array_ | Reference to a list of configmaps. |  |  |
| `resources` _[ResourceRequirements](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#resourcerequirements-v1-core)_ | cpu and memory resources as per K8S standards<br />This is only for newdeploy to set up resource limitation<br />when creating deployment for a function. |  |  |
| `InvokeStrategy` _[InvokeStrategy](#invokestrategy)_ | InvokeStrategy is a set of controls which affect how function executes |  |  |
| `functionTimeout` _integer_ | FunctionTimeout provides a maximum amount of duration within which a request for<br />a particular function execution should be complete.<br />This is optional. If not specified default value will be taken as 60s |  |  |
| `idletimeout` _integer_ | IdleTimeout specifies the length of time that a function is idle before the<br />function pod(s) are eligible for deletion. If no traffic to the function<br />is detected within the idle timeout, the executor will then recycle the<br />function pod(s) to release resources. |  |  |
| `streaming` _[StreamingConfig](#streamingconfig)_ | Streaming opts this function into the router's streaming invocation path:<br />incremental flushing, an idle/max timeout split, and a router-driven pod<br />keepalive for the connection's lifetime. When nil (the default) the function<br />uses the classic buffered, retry-on-transient-error proxy path with a single<br />FunctionTimeout deadline. Additive and backward compatible. |  |  |
| `tool` _[ToolConfig](#toolconfig)_ | Tool, when non-nil, advertises this function as a Model Context Protocol<br />(MCP) tool on the fission-bundle --mcpPort server. The MCP server watches<br />Function CRDs and hot-updates its tool list from this field. Presence is<br />the on switch (like Streaming): nil (the default) means the function is<br />never advertised as a tool. Additive and backward compatible. |  |  |
| `concurrency` _integer_ | Maximum number of pods to be specialized which will serve requests<br />This is optional. If not specified default value will be taken as 500 |  |  |
| `requestsPerPod` _integer_ | RequestsPerPod indicates the maximum number of concurrent requests that can be served by a specialized pod<br />This is optional. If not specified default value will be taken as 1 |  |  |
| `onceOnly` _boolean_ | OnceOnly specifies if specialized pod will serve exactly one request in its lifetime and would be garbage collected after serving that one request<br />This is optional. If not specified default value will be taken as false |  |  |
| `retainPods` _integer_ | RetainPods specifies the number of specialized pods that should be retained after serving requests<br />This is optional. If not specified default value will be taken as 0 |  |  |
| `podspec` _[PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#podspec-v1-core)_ | Podspec specifies podspec to use for executor type container based functions<br />Different arguments mentioned for container based function are populated inside a pod. |  |  |


#### FunctionStatus



FunctionStatus describes the observed state of a Function.



_Appears in:_
- [Function](#function)

| Field | Description | Default | Validation |
| --- | --- | --- | --- |
| `observedGeneration` _integer_ | ObservedGeneration reflects the .metadata.generation that the<br />controller observed when it last updated the status. |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ | Conditions represent the latest observations of the function's state. |  |  |


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
| `lastUpdateTimestamp` _[Time](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#time-v1-meta)_ | LastUpdateTimestamp will store the timestamp the package was last updated<br />metav1.Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.<br />https://github.com/kubernetes/apimachinery/blob/44bd77c24ef93cd3a5eb6fef64e514025d10d44e/pkg/apis/meta/v1/time.go#L26-L35 |  |  |
| `conditions` _[Condition](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/#condition-v1-meta) array_ | Conditions represent the latest observations of the package's state. |  |  |


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
| `functionref` _[FunctionReference](#functionreference)_ | The reference to function |  |  |
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




#### ValidationErrorType

_Underlying type:_ _integer_





_Appears in:_
- [ValidationError](#validationerror)



