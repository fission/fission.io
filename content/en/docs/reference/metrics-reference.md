---
title: "Fission Metrics Reference"
weight: 8
description: >
  Fission Metrics - List of Prometheus metrics in Fission
---

{{< notice info >}}
To access these metrics, you'll need to install Fission 1.16 or higher.
{{< /notice >}}

| Metric Name | Component | Labels | Description |
| ------------------- | --------- | ------------------ | -------------------- |
| http_requests_total | General   | path, method, code | Number of requests by path, method and status code |
| http_requests_duration_seconds | General | path, method | Time taken to serve the request by path and method |
| http_requests_in_flight | General | path, method | Number of requests currently being served by path and method |
| fission_function_cold_starts_total | Executor | function_name, function_namespace | How many cold starts are made by function_name, function_namespace |
| fission_function_running_seconds  | Executor | function_name, function_namespace | The running time (last access - create) in seconds of the function |
| fission_function_cold_start_errors_total  | Executor | function_name, function_namespace | Count of Fission cold start errors |
| fission_function_calls_total | Router | function_namespace, function_name, path, method, code | Count of Fission function calls |
| fission_function_errors_total | Router | function_namespace, function_name, path, method, code | Count of Fission function errors |
| fission_function_overhead_seconds | Router | function_namespace, function_name, path, method, code | The function call delay caused by Fission. |
| fission_archives_total | StorageSvc | Nil | Number of archives stored |
| fission_archive_memory_bytes | StorageSvc | Nil | Amount of memory consumed by archives |
| fission_mqt_subscriptions | MqTrigger | Nil | Total number of subscriptions to mq currently |
| fission_mqt_messages_processed_total | MqTrigger | trigger_name, trigger_namespace | Total number of messages processed by trigger |
| fission_mqt_message_lag | MqTrigger | trigger_name, trigger_namespace, topic, partition | Total number of messages lag per topic and partition |
