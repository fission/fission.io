+++
title = "How to Develop a Serverless Application with Fission (Part 3)"
date = "2018-09-08T13:27:34+08:00"
author = "Ta-Ching Chen"
description = "Write serverless Java functions with JVM"
categories = ["Fission", "application"]
type = "post"
+++

# Introduction

At [Part 2](/posts/how-to-develop-a-serverless-application-with-fission-pt-2), we knew what's real payload was passed to function and how to create a serverless guesbook. 
In the last post, we will go through the final bank sample and know how to deploy a application to different fission clusters.

# A Serverless Bank Application in Golang (Sample)

In this section, we use a more complex bank sample to demonstrate how to use AJAX interacts with fission functions.   

![Fission Bank Diagram](/images/how-to-develop-a-serverless-application-with-fission/fission-bank-sample.svg)

## Installation

You can clone repo below and follow the guide to install/try bank sample.

* [Fission Bank Repo](https://github.com/fission/fission-bank-sample)
 
## AJAX and CORS

AJAX ([Asynchronous JavaScript and XML](https://en.wikipedia.org/wiki/Ajax_(programming))) allows JavaScript sending requests to 
remote server without refreshing web page which quite suitable for using fission function to handle the requests.

Following is the sample code using jQuery to send AJAX requests to backend fission function on path "/accounts".

* [web/account.html](https://github.com/fission/fission-bank-sample/blob/f4d2480d36fef164895b43df33fb6d7f44191367/web/account.html#L59-L75)

```js
$.ajax({
    origin: "*",
    type: 'POST',
    url: '/accounts', // RESTful API function path
    crossDomain: true,
    data: JSON.stringify(data),
    contentType: "application/json",
    error: function (xhr) {
        $('#alert-danger').html('('+xhr.status+') '+xhr.responseText).show();
        return false;
    },
    success: function (response) {
        $('#alert-success').html(response).show();
        window.location.href = "./login.html";
        return true;
    }
});
```

In this sample, we put both website pages and fission functions under same domain. For most cases, however, the web pages 
are often served with different domain and hitting CORS([Cross-Origin Resource Sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)) problem like following.

![CORS Chrome](/images/how-to-develop-a-serverless-application-with-fission/cors-chrome.png)

To fix this, we have to add couple change to our function.

* Add CORS header to response header
* Add OPTIONS pre-flight request handler

## Add CORS header to response header

Browser checks whether response contains CORS headers. So before replying user request call `setCORS()` to add header.
For more details about CORS header, please visit https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS. 

* [functions/common.go](https://github.com/fission/fission-bank-sample/blob/f4d2480d36fef164895b43df33fb6d7f44191367/functions/common.go#L15-L22)

 ```go
func reply(msg []byte, code int, w http.ResponseWriter) {
    w = setCORS(w) // set CORS header
    w.WriteHeader(code)
    w.Write(msg)
} 

func setCORS(w http.ResponseWriter) http.ResponseWriter {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Headers", "*")
    w.Header().Set("Access-Control-Allow-Credentials", "true")
    w.Header().Set("Access-Control-Allow-Methods", "*")
    w.Header().Set("Access-Control-Expose-Headers", "*")
    return w
}
```

## Add OPTIONS pre-flight request handler

* Graph from https://en.wikipedia.org/wiki/Cross-origin_resource_sharing

![Flowchart_showing_Simple_and_Preflight_XHR](/images/how-to-develop-a-serverless-application-with-fission/Flowchart_showing_Simple_and_Preflight_XHR.svg)

From the graph above, we can see that browser will send OPTIONS request to remote server. So we should add another function to handle such requests.

* [functions/optionsHandler.go](https://github.com/fission/fission-bank-sample/blob/f4d2480d36fef164895b43df33fb6d7f44191367/functions/optionsHandler.go#L7-L9)

```go
func CorsOptionsHandler(w http.ResponseWriter, r *http.Request) {
	setCORS(w).WriteHeader(http.StatusOK)
}
```

And you need to create OPTIONS http triggers point to `options-handler` function for **every URL endpoint**.

```bash
$ fission route list|grep OPTIONS
e019d4be-fdfe-404a-bfca-5a5b24fe531f OPTIONS      /accounts                       false   options-handler
6fac456d-d155-422c-8580-c464ba308050 OPTIONS      /accounts/                      false   options-handler
4452f18c-f9b2-40d6-b676-ee868627e237 OPTIONS      /sessions                       false   options-handler
3f74a3a1-edc5-470d-bbcd-4395377705a1 OPTIONS      /transaction                    false   options-handler
93845c23-eadb-4335-9a1c-1ddec0da19bd OPTIONS      /transaction/withdraw           false   options-handler
ba9c8cdb-ad31-4eec-9ae9-00001fdd85e6 OPTIONS      /transaction/deposit            false   options-handler
6b2be34d-5f07-4426-8baf-951c71db3602 OPTIONS      /transaction/transfer           false   options-handler
```
 
# Deploy the Same Application to Different Environment

In the last section of the post, assume you already created a serverless application on your own cluster. You may start 
wondering is there any way to migrate a application from one cluster to another? 

The answer is **YES**. 

Consider most of developers have different environments (e.g. Canary, Production) to test and run with. 
Fission allows users to deploy the same application with `spec` files. A spec file is a Fission Object in YAML format includes all necessary information. 

Here is a sample YAML that describe a go environment:

```yaml
apiVersion: fission.io/v1
kind: Environment
metadata:
  creationTimestamp: null
  name: go
  namespace: default
spec:
  TerminationGracePeriod: 360
  builder:
    command: build
    image: fission/go-builder
  keeparchive: false
  poolsize: 3
  resources: {}
  runtime:
    functionendpointport: 0
    image: fission/go-env
    loadendpointpath: ""
    loadendpointport: 0
  version: 2
```

The best thing is you don't need to write YAML files by hand. You can create with CLI directly. 

Here are steps for how to create application spec files:

1. Create spec directory
2. Create fission resources with flag `--sepc`
3. Check spec files under `spec` directory

```bash
$ fission spec init

$ fission env create --name go --image fission/go-env --builder fission/go-builder --spec

$ cat specs/env-go.yaml
```

After creating all fission objects for application, you can deploy & destroy an application with `apply` command:

```bash
$ fission spec apply 
```

Now, the go environment was created automatically.

```bash
$ fission env list
NAME   UID                                  IMAGE            POOLSIZE MINCPU MAXCPU MINMEMORY MAXMEMORY EXTNET GRACETIME
go     d30a78ee-a618-11e8-a55e-08002720b796 fission/go-env   3        0      0      0         0         false  360
```

But what about archiving source code into source package? Is there any way to archive it automatically?

At [Part 1](/posts/how-to-develop-a-serverless-application-with-fission-pt-1/#add-additional-go-dependencies) we use `ZIP` command to 
archive source package. You can achieve this by writing a `ArchiveUploadSpec` YAML file like following. `fission spec` 
will automatically archives files list on `include` field once it detects `ArchiveUploadSpec` exists.   

* [spec/pkg.yaml](https://github.com/fission/fission-bank-sample/blob/f4d2480d36fef164895b43df33fb6d7f44191367/specs/pkg.yaml#L1-L21)

```yaml
apiVersion: fission.io/v1
kind: Package
metadata:
  name: bank-go-pkg
  namespace: default
spec:
  source:
    url: archive://bank-go-zip # need to match source archive name below
  buildcmd: "build"
  environment:
    name: go
    namespace: default
status:
  buildstatus: pending

---
kind: ArchiveUploadSpec
name: bank-go-zip # source archive name
include:
  - "functions/*.go"
  - "functions/vendor"
```

After `apply` command, you shall see a package was created. 

```bash
$ fission pkg list
NAME                  BUILD_STATUS ENV
bank-go-pkg           succeeded    go
```

**NOTE**: Currently, v0.10.0 doesn't support to create spec files for archiving package. There is an [issue](https://github.com/fission/fission/issues/769)
trying to address the problem and will be released in 0.11.0.

# Conclusion

After all 3 parts of this post, hope you understand fission more well and start using fission as FaaS solution on kubernetes. 
Since fission is a growing project, feel free to [join the Fission community](https://fission.io/community/) to share your idea with us! :)

---

**_Authors:_**

* Ta-Ching Chen **|** [Fission Contributor](https://github.com/life1347) **|** [Tech blog](https://tachingchen.com/blog)
