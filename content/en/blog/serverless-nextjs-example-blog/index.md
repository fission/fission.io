---
title: "Serverless Next.js Example Blog with Fission"
date: 2021-11-17T13:29:16+05:30
author: Sanket Sudake
categories: ["Tutorials"]
draft: false
---

## What is Next.js?

Next.js is a framework for building fast, modern websites using React.
Next.js provides a couple of features for building static and server-side rendered websites.
With [Next.js examples](https://nextjs.org/examples) and [showcase](https://nextjs.org/showcase), you can get a taste of Next.js.
You can refer to the [Next.js documentation](https://nextjs.org/docs) for more details.

## Next.js Example Blog with Fission

Next.js is gaining a lot of popularity in serverless world.
Fission can be used to host a low traffic frontend website, with minimal cost and reduced maintenance.
Fission can host your existing Next.js application with few modifications.

Fission recently launched support for prefixed path routing in [1.13.1 release](/docs/releases/1.13.1/).
Using prefix path routing, a single Fission function can handle multiple routes.
We use this feature to create a blog with Next.js.

Let's do a walkthrough of how to deploy a Next.js application with Fission.

## Get Next.js application running

Typical Next.js application has a `pages` directory, which contains all the pages to be served.
There are supplimentary directories such as `styles`, `data`, `components`, `public` etc. which could be part of your Next.js application.

We have a built demo blog application with Fission, source code is available on [GitHub](https://github.com/fission/examples/tree/main/miscellaneous/nextjs-blog-demo).

Clone the [examples repository](https://github.com/fission/examples) first.

We will do a quick walkthrough of our code structure in Next.js blog.

```text
.
├── components      # Common components used in Next.js app
├── data            # Holds data of the blog content
├── next.config.js  # All the configuration for Next.js
├── package.json    # Node module dependencies
├── pages           # Code for all the pages
├── public          # Static files like CSS, JS, images
└── styles          # Styles for the blog
```

Apart from the above directories & files, you might notice few additional files, we cover them later.

You can get blog application running without Fission with following commands,

```bash
$ cd samples/nextjs-blog-demo
# Check Node.js installed (16.x version recommended)
$ node -v
v16.13.0
# Check NPM installed
$ npm -v
8.1.0
# Install Node modules
$ npm install
# Run the application
$ npm run dev
> nextjs-app@0.1.0 dev
> next dev
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

You can visit running blog application on <localhost:3000/nextapp>.
Please note `/nextapp` is the prefix path,i.e. all the pages will be served from `/nextapp/`.

{{< imgproc blog-example Fit "800X800" >}}
Blog Screenshot
{{< /imgproc >}}

You can change the prefix path in `next.config.js` file.

## Customize Next.js application to work with Fission

We would be using [Fission Node.js support](/docs/usage/languages/nodejs/) to host our Next.js application.

Fission Node.js functions typically expect entrypoint function that processes HTTP requests.
When Fission function is invoked, Fission runs entrypoint function and passes the request object to it.

We create `app.js` file at root of our Next.js application.
`app.js` file defines the entrypoint function.
Function loads request handler from Next.js application instance and invokes it for each request.

```js
"use strict";
const next = require('next');
const isDev = false;
console.log(__dirname);
const nextConfig = require('./next.config');
const nextApp = next({
  dev: isDev,
  dir: __dirname,
  conf: nextConfig,
});
const handle = nextApp.getRequestHandler();
module.exports = async function (context, callback) {
  console.log(context.request.url);
  nextApp.prepare().then(() => handle(context.request, context.response));
}
```

We also provide configuration with `next.config.js` file.
Let's have look at our `next.config.js` file.

```js
module.exports = {
  reactStrictMode: true,
  basePath: '/nextapp',
  distDir: '.next',
  images: {
    path: '/nextapp/_next/image',
  },
  env: {
    imgPrefix: '/nextapp',
  },
}
```

If you see `basePath` is set to `/nextapp`, so that all the pages will be served from `/nextapp/`.
If you want to change the base path, you can change all instances of `/nextapp` with your base path in `next.config.js` file.

## Packaging Next.js source and Generate Fission Specs

Here, we compile Next.js application locally and generate zip file with all the required files.

Build Next.js application locally,

```bash
npm install
npm run build
```

This zip file can be used to deploy Next.js application via Fission package.

```bash
zip -r nextjs-source.zip app.js next.config.js package.json \
  package.lock.json data/ pages/ public/ \
  styles/ node_modules/ yarn.lock .next/ \
  components/
```

Fission specs provides a declarative way to describe objects to be created in Fission for your application deployment.

```bash
# Initialize specs directory, create specs/ directory at root of the app
fission spec init
# Create a spec for Node.js environment
fission env create --spec --name nodejs --image fission/node-env-16
# Define package for our Next.js application with zip created above
fission package create --spec --deploy nextjs-source.zip --env nodejs --name nextjs-source
# Define function and entrypoint for our Next.js application
fission fn create --spec --name nextjs-func --pkgname nextjs-source --entrypoint "app"
# Create route to access our Next.js application outside of Fission
fission route create --spec --name next-blog --function nextjs-func \
    --method GET --method POST --prefix /nextapp  --keepprefix
```

Please note that we are using `--prefix` option to define the prefix path for our Next.js application.
This tells Fission any request to `/nextapp/` will be handled by our Next.js application.
We also pass `--keepprefix` option to tell Fission to keep the prefix path in the request URL, when Fission forwards the request to our Next.js application.

## Deploy Next.js application to Fission

Once you specs and source zip file are created, you can deploy your Next.js application to Fission.

```bash
fission spec apply
```

You can check the status of package with `fission package list`.

```bash
fission pkg list
NAME          BUILD_STATUS ENV    LASTUPDATEDAT
nextjs-source succeeded    nodejs 28 Jul 21 12:12 IST
```

With router URL you can visit your Next.js application at <router-url/nextapp>

## Conclusion

In this simple example, we understood how to create a Next.js application with Fission.
Though we have covered Next.js application with Fission, you can use Fission to deploy any other application written in any language in similar fashion.

----

If you would like to find out more about Fission:

- Get started in [fission.io](http://fission.io/).
- Check out the
  [Fission project in GitHub](https://github.com/fission/fission).
- Meet the maintainers on the
  [Fission Slack](/slack).
- Follow [@fissionio on Twitter](https://twitter.com/fissionio).
