---
title: "Logger"
weight: 9
description: >
  Record and persist function logs
---

Logger is deployed as <a href="https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/" target="_blank">DaemonSet</a> to help to forward function logs to a centralized database service for log persistence.
Currently, only InfluxDB is supported to store logs.

{{< img "../assets/logger.png" "Fig.1 Logger" "45em" "1" >}}

1. Containers in the function pod write logs to docker log files.
2. Logger watches pod creation/update events
3. Create symlinks to the container logs if the pod runs on the same node. (Symlinks will be removed if the pods no longer exist.)
4. Logger (`Fluentbit`) reads logs from symlinks.
5. Logs are piped to InfluxDB to persist.
