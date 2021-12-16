---
title: "Builder Pod"
weight: 7
description: >
  Place to build the user function
---

Builder pod builds the source archive and generates a deployment archive. This deployment archive is used by the [function pod](/docs/architecture/function-pod).
It consists of two containers:
* Fetcher
* Builder Container

### Fetcher

Fetcher is responsible to pull source archive from the [StorageSvc](/docs/architecture/storagesvc/) and verify the checksum of file to ensure the integrity of file.
After the build process, it uploads the deployment archive to StorageSvc.

### Builder Container

Builder Container compiles function source code into executable binary/files and is language-specific.

{{< img "../assets/builder-pod.png" "Fig.1 Builder Pod" "50em" "1" >}}

1. Builder Manager asks Fetcher to pull the source archive.
2. Fetcher pulls the source archive from the StorageSvc.
3. Save the archive to the shared volume.
4. Builder Manager sends a build request to the Builder Container to start the build process.
5. Builder Container reads source archive from the volume, compiles it into deployment archive.<br />
Finally, save the result back to the share volume.  

6. Builder Manager asks Fetcher to upload the deployment archive.


