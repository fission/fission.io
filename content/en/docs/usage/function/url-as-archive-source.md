---
title: "Use URL as archive source when creating functions/packages"
weight: 7
description: >
  Embed a remote URL directly in a package archive when creating functions or packages to cut creation time and improve spec portability.
---

**Embedding a URL directly in the package archive skips the download-and-upload step, cutting package creation time.**
Previously, when a user provided a URL as the archive source, the CLI downloaded the file and uploaded it to internal storagsvc to persist it.
This approach increased the total package creation time if the file size was large.

With 1.7.0+, the CLI embeds the given URL in the package archive directly, bringing two benefits:

* Shorten package creation time.
* Increase the portability of fission spec file.

For example, creating a package from a remote URL:

```bash
$ fission pkg create --spec --name dummy-package2 --env nodejs \
    --code https://raw.githubusercontent.com/fission/examples/main/nodejs/hello.js
```

This produces a package spec that references the URL directly rather than an uploaded copy:

```yaml
apiVersion: fission.io/v1
kind: Package
metadata:
  creationTimestamp: null
  name: dummy-package2
  namespace: default
spec:
  deployment:
    checksum: {}
    type: url
    url: https://raw.githubusercontent.com/fission/examples/main/nodejs/hello.js
    ....
```

The CLI still downloads the file once, to generate the SHA256 checksum that detects if the file changes.
To skip this download step, use `--srcchecksum`, `--deploychecksum`, or `--insecure`.
