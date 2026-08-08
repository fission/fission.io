---
title: "Fission Metrics Reference"
weight: 8
description: >
  Fission Metrics - List of Prometheus metrics in Fission
---

**Fission exports Prometheus metrics for requests, cold starts, function calls, archive storage, message-queue triggers, eventing, async invocations, workflows, and the statestore, so you can monitor and alert on your deployment.**

{{< notice info >}}
To access these metrics, you'll need to install Fission 1.16 or higher.
{{< /notice >}}

{{< notice info >}}
To access `fission_mqt_inprocess` and `fission_mqt_status` metrics, you'll need to install Fission 1.20.3 or higher.
{{< /notice >}}

The table below lists every metric, the component that emits it, its labels, and what it measures.

| Metric Name | Component | Labels | Description |
| ------------------- | --------- | ------------------ | -------------------- |
| http_requests_total | General   | path, method, code | Number of requests by path, method and status code |
| http_requests_duration_seconds | General | path, method | Time taken to serve the request by path and method |
| http_requests_in_flight | General | path, method | Number of requests currently being served by path and method |
| fission_error_span_export_failures_total | General | Nil | Error spans the error-biased exporter failed to send |
| fission_error_span_export_drops_total | General | Nil | Error spans dropped without export because the error-biased exporter was saturated |
| fission_function_cold_starts_total | Executor | function_name, function_namespace | How many cold starts are made by function_name, function_namespace |
| fission_function_running_seconds  | Executor | function_name, function_namespace | The running time (last access - create) in seconds of the function |
| fission_function_cold_start_errors_total  | Executor | function_name, function_namespace | Count of Fission cold start errors |
| fission_executor_specializations_rejected_total | Executor | function_name, function_namespace | Specialization requests rejected at a capacity bound (concurrency cap or in-flight limit) |
| fission_executor_function_service_ensures_total | Executor | result | Count of per-function Service ensure operations by result (created, updated, exists, error) |
| fission_executor_oci_pools_reaped_total | Executor | Nil | Per-image (OCI) warm pools destroyed by the idle pool reaper |
| fission_executor_oci_pool_reap_failures_total | Executor | Nil | Idle-pool reap attempts whose deployment delete failed |
| fission_provisioned_target | Executor | function_name, function_namespace | Desired provisioned-concurrency warm-pod count |
| fission_provisioned_ready | Executor | function_name, function_namespace | Current provisioned-concurrency warm-pod count |
| fission_provisioned_eager_specializations_total | Executor | function_name, function_namespace, outcome | Provisioned eager specialization attempts by outcome (success, error) |
| fission_provisioned_window_transitions_total | Executor | function_name, function_namespace | Provisioned window transitions per function |
| fission_function_calls_total | Router | function_namespace, function_name, function_version, path, method, code | Count of Fission function calls |
| fission_function_errors_total | Router | function_namespace, function_name, function_version, path, method, code | Count of Fission function errors |
| fission_function_overhead_seconds | Router | function_namespace, function_name, function_version, path, method, code | The function call delay caused by Fission. |
| fission_invocation_failures_total | Router | component, reason | Count of failed function invocations attributed by component and reason |
| fission_router_sticky_requests_total | Router | function_namespace, function_name | Requests to sticky-routed functions that carried their sticky key |
| fission_router_sticky_key_missing_total | Router | function_namespace, function_name | Requests to sticky-routed functions missing their sticky key (default pick used) |
| fission_router_route_table_applies_total | Router | result | Route table applications by result (no_change, handler_swapped, shape_changed, rejected) |
| fission_router_mux_rebuilds_total | Router | listener, reason | Full mux rebuilds by listener and reason |
| fission_router_routes | Router | listener | Routes currently in the route table (public = HTTP triggers, internal = functions) |
| fission_router_route_resync_drift_total | Router | Nil | Routes the periodic resync had to correct; a nonzero value means a watch event was missed |
| fission_router_route_resync_failures_total | Router | Nil | Resync passes that failed; the drift guard could not verify the route table this tick |
| fission_router_mux_materialize_failures_total | Router | Nil | Mux materializations that failed before the swap; the served mux is stale until a retry succeeds |
| fission_router_tap_flush_errors_total | Router | Nil | Failed batched tap flushes from the router to the executor |
| fission_router_tap_flush_notfound_total | Router | Nil | Batched tap flushes the executor answered 404 (expired or unknown addresses) |
| fission_router_endpointcache_hits_total | Router | Nil | Requests served from the EndpointSlice endpoint index (no executor RPC) |
| fission_router_endpointcache_misses_total | Router | Nil | Requests with no ready endpoint in the EndpointSlice endpoint index |
| fission_router_endpointcache_endpointlb_picks_total | Router | Nil | Requests dialed directly to a pod IP by the endpoint-LB path (newdeploy/container) |
| fission_router_endpointcache_quarantines_total | Router | Nil | Endpoints quarantined from the index after a dial failure |
| fission_router_endpointcache_dial_timeout_strikes_total | Router | Nil | Soft dial failures (timeouts) recorded against endpoints |
| fission_router_endpointcache_fallbacks_total | Router | reason | Warm-path requests routed to the executor instead of the endpoint index, by reason |
| fission_router_endpointcache_mode | Router | requested, effective, endpoint_lb | Always 1; labels carry the requested and effective EndpointSlice cache modes |
| fission_router_endpointcache_size | Router | Nil | Number of functions with at least one EndpointSlice in the router's endpoint index |
| fission_router_endpointcache_informers | Router | Nil | Number of running per-namespace EndpointSlice informers |
| fission_async_deliveries_total | Router | condition | Count of async invocation delivery attempts, by response condition |
| fission_async_retries_total | Router | Nil | Count of async invocation deliveries requeued for a retry |
| fission_async_dlq_total | Router | reason | Count of async invocations dead-lettered, by reason |
| fission_async_destinations_total | Router | outcome | Count of async destination fires, by outcome |
| fission_async_depth_cap_total | Router | Nil | Count of async destination invocations dropped for exceeding the chain depth cap |
| fission_async_version_fallback_total | Router | Nil | Count of async deliveries that fell back to the bare function route after a 404 on a version-pinned route |
| fission_async_queue_depth | Router | Nil | Async invocation queue depth: visible messages awaiting delivery |
| fission_async_oldest_age_seconds | Router | Nil | Age in seconds of the oldest visible async invocation (0 when none) |
| fission_eventing_egress_queue_depth | Router | mqType | Broker egress queue depth: visible jobs awaiting publish |
| fission_eventing_egress_oldest_age_seconds | Router | mqType | Age in seconds of the oldest visible broker egress job (0 when none) |
| fission_archives | StorageSvc | Nil | Number of archives stored |
| fission_archive_memory_bytes | StorageSvc | Nil | Amount of memory consumed by archives |
| fission_storagesvc_legacy_archive_access_total | StorageSvc | Nil | Accesses by a namespace-scoped caller to a legacy (unscoped) archive |
| fission_mqt_subscriptions | MqTrigger | Nil | Total number of subscriptions to mq currently |
| fission_mqt_messages_processed_total | MqTrigger | trigger_name, trigger_namespace | Total number of messages processed by trigger |
| fission_mqt_message_lag | MqTrigger | trigger_name, trigger_namespace, topic, partition | Total number of messages lag per topic and partition |
| fission_mqt_inprocess | MqTrigger | Nil | Total number of MQTs in active processing |
| fission_mqt_status | MqTrigger | trigger_name, trigger_namespace | Status of an individual trigger 1 if processing otherwise 0 |
| fission_eventing_published_total | Router, MqTrigger | provider, outcome | Count of topic publishes by provider and outcome (published, error, invalid, capped, unsupported) |
| fission_eventing_delivered_total | MqTrigger | condition | Count of topic-event deliveries reaching terminal handling, by condition (success, exhausted) |
| fission_eventing_retries_total | MqTrigger | Nil | Count of topic-event delivery retries |
| fission_eventing_errortopic_total | MqTrigger | outcome | Count of exhausted events routed to the error topic, by outcome (published, error, dropped) |
| fission_eventing_trimmed_total | MqTrigger | reason | Count of topic events trimmed by retention, by reason (mincursor, age, size) |
| fission_eventing_responsetopic_total | MqTrigger | outcome | Count of response-topic publishes after successful deliveries, by outcome (published, error) |
| fission_eventing_gap_events_total | MqTrigger | Nil | Count of topic events a subscription found already trimmed when it resumed |
| fission_eventing_lag | MqTrigger | namespace, trigger | Per-trigger consumer lag (stream head minus committed cursor) |
| fission_eventing_egress_total | MqTrigger | outcome | Count of broker egress job outcomes (published, retry, malformed, settle_failed) |
| fission_statestore_ops_total | StateStore | capability, op | Statestore operations, by capability and op |
| fission_statestore_errors_total | StateStore | capability, op | Statestore operations that returned an error, by capability and op |
| fission_statestore_quota_rejections_total | StateStore | reason | Writes rejected by a scope quota, by reason |
| fission_statestore_conservation_scrape_errors_total | StateStore | Nil | Failures reading a driver's conservation stats; a nonzero value means the drift gauge is stale |
| fission_statestore_conservation_drift | StateStore | Nil | Queue conservation drift (enqueued - inflight - acked - dead); must be zero |
| fission_workflow_runs_total | Workflow | workflow, phase | Workflow runs reaching a terminal phase, by workflow and phase |
| fission_workflow_step_duration_seconds | Workflow | state, outcome | Task step attempt duration (invocation round trip), by workflow state and outcome |
| fission_workflow_active_runs | Workflow | Nil | Runs currently executing (started, not yet terminal) |
| fission_buildermgr_oci_publish_total | BuilderMgr | result | OCI package publish outcomes by result (published, degraded) |
| fission_autopublish_total | BuilderMgr | result | Auto-publish reconcile outcomes by result (created, unchanged, deferred) |
| fission_versiongc_deleted_total | BuilderMgr | Nil | Version retention GC: FunctionVersions deleted |
| fission_versiongc_skipped_total | BuilderMgr | reason | Version retention GC: FunctionVersion deletes skipped, by reason (referenced, forbidden) |
