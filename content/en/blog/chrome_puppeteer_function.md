+++
title = "Headless Chrome with Puppeteer in a function"
date = "2021-05-09T23:50:51+05:30"
author = "Vishal Biyani"
description = "Test websites with a headless chrome and Puppeteer in a fission function"
categories = ["Tutorials"]
type = "blog"
+++

# Introduction

Running chrome headless is useful for various test automation tasks but running a headless Chrome in Docker can be tricky ([More details here](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#running-puppeteer-in-docker)). Also the [this Github issue](https://github.com/puppeteer/puppeteer/issues/3994#issuecomment-524396092) has some good insights on the issues you might face. This blog shows running headless chrome in a fission function. You can find the working example with code etc. in [examples repo here](https://github.com/fission/examples/tree/main/miscellaneous/nodejs-chrome-headless).

Typical use cases for which Puppeteer is used are:

- Generating screenshots of specific web pages
- Automating form submission at scale or doing any testing of web pages
- Testing of chrome extensions
- Crawl web pages to gather information from them.

# Demo

If you simply want to get a sense of running function run, assuming you have Fission installed, you can run `fission spec apply` and then then test the function

```sh
$ fission spec apply
DeployUID: 0e8b177b-19bd-4e97-80b7-42f1f3801ed8
Resources:
 * 1 Functions
 * 1 Environments
 * 1 Packages
 * 0 Http Triggers
 * 0 MessageQueue Triggers
 * 0 Time Triggers
 * 0 Kube Watchers
 * 1 ArchiveUploadSpec
Validation Successful
1 environment updated: node-chrome
1 function updated: chrome
```

The test gives out Google homepage content as a response because that is the URL we have configured in the function.

```sh
$ fission fn test --name chrome

<!DOCTYPE html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en-IN"><head><meta charset="UTF-8"><meta 
content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script 
src="https://apis.google.com/_/scs/abc-static/_/js/k=gapi.gapi.en.lqqPe8Y-aUs.O/m=gapi_iframes,googleapis_client/rt=j/
sv=1/d=1/ed=1/rs=AHpOoo_7ZBgzLryveB2qtYoSqeBQ4P-TYA/cb=gapi.loaded_0" nonce="GSIA5d0Gka6XrtwFCPVCrg==" async=""></
script><script nonce="GSIA5d0Gka6XrtwFCPVCrg==">(function(){window.google={kEI:'lmY2X4L-AoOW4-EPxPiykAY',kEXPI:'31',
kBL:'tCe1'};google.sn='webhp';google.kHL='en-IN';})();(function(){google.lc=[];google.li=0;google.getEI=function(a)
```

# How does it work?

## Building a custom image

The stock Fission image does not have Chromium built in and we use a modified base image. You will need to copy this modified Dockerfile in fission's environment repo at environments/nodejs as it needs rest of code of environment.

```sh
$ tree
.
├── Dockerfile
├── README.md
├── package.json
└── server.js

$ docker build -t vishalbiyani/node-chrome:1 .
 
```

Or simply add this section to [Dockerfile of NodeJS environment](https://github.com/fission/environments/blob/master/nodejs/Dockerfile), build a new image and keep it ready. We will use this custom image to create environments later.

```dockerfile
# Needed for chromium
RUN apk add --no-cache \
      chromium \
      nss \
      freetype \
      freetype-dev \
      harfbuzz \
      ca-certificates \
      ttf-freefont \
      nodejs \
      yarn
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

RUN yarn add puppeteer@1.19.0
RUN addgroup -S pptruser && adduser -S -g pptruser pptruser \
    && mkdir -p /home/pptruser/Downloads /app \
    && chown -R pptruser:pptruser /home/pptruser \
    && chown -R pptruser:pptruser /app

USER pptruser
```

## Creating env & function with source code

Let's start by initializing the specs for function and environment:

```sh
$ fission spec init
```

Creating the environment and function specs & apply. 

> Note that we are using a custom image `--image vishalbiyani/node-chrome:1` for headless chromium.

```sh
$ fission env create --name node-chrome --image --image vishalbiyani/node-chrome:1 --builder ghcr.io/fission/node-builder --spec

$ fission fn create --name chrome --env node-chrome --src hello.js --src package.json --entrypoint hello --spec

$ fission spec apply 
```

We have to wait for package building to be successful, and if fails, please rebuild once again:

```sh
$ fission package rebuild --name chrome-76a831d5-107c-4d09-a4fa-a1d2fab770e8

$ fission package list
NAME                                        BUILD_STATUS ENV         LASTUPDATEDAT
chrome-76a831d5-107c-4d09-a4fa-a1d2fab770e8 succeeded    node-chrome 14 Aug 20 15:52 IST

```

Finally the test:

```sh
$ fission fn test --name chrome

<!DOCTYPE html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en-IN"><head><meta charset="UTF-8"><meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title><script src="https://apis.google.com/_/scs/abc-static/_/js/k=gapi.gapi.en.
```

We were able to use the Puppeteer library for just a single use in this example. The real world use cases are definitely not as trivial as this one, but this blog demos what is possible. We can spin up many functions to generate screenshots or crawl web pages. If we want workflow between functions - we can use the MQs and connectors to coordinate that as well. This can be very powerful for many use cases and the functions allow us to scale on demand as needed.

**Follow us on Twitter for more updates! [@fissionio](https://www.twitter.com/fissionio)**

--- 

**_Author:_**

* [Vishal Biyani](https://twitter.com/vishal_biyani)  **|**  [Fission Contributor](https://github.com/vishal-biyani)  **|**  CTO - [InfraCloud Technologies](http://infracloud.io/)