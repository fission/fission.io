+++
title = "Fission Serverless Function + Zapier Webhook - Automate your workflows"
date = "2022-04-14T11:35:34+05:30"
author = "Atulpriya Sharma"
description = "Automate your workflows with Fission serverless functions and Zapier Webhooks"
categories = ["Tutorials"]
type = "blog"
images = ["images/featured/fission-zapier-featured.png"]
+++

There hasn’t been a greater need for automation than what it is today.
Things around us are moving fast and everyone wants things done faster. Getting that agility manually is tough and hence individuals and teams globally look for ways to automate workflows.

In this post, I’m going to show you how you can **automate your workflows using Fission serverless functions and Zapier Webhooks**.

## What is Zapier?

[**Zapier**](https://zapier.com) is one of the world’s most widely used tools to automate workflows.
It allows you to integrate various apps that you use and integrate them along with actions to complete a flow.

For example, you want to track all the mentions on Twitter.
You can create a ZAP, to trigger whenever someone mentions you.
It will take the tweet and put it in a Google Sheet.
All of this without you writing a single line of code!

*PS: Do read how we created a [Twitter Bot on Fission](/blog/developing-a-serverless-twitter-bot-on-fission/)!*

Apart from the various app integrations that Zapier provides, **Webhooks** are a popular way to get the most out of your applications.
It’s probably the ultimate way to automate your workflow with Zapier.
If you want to know how Webhooks differ from APIs, I suggest reading [Webhook vs API - Which One Do You Need?](https://towardsdatascience.com/webhook-vs-api-which-one-do-you-need-8c430f8ea71b)

{{< figure src="/images/featured/fission-zapier-featured.png" alt="Automate Workflows using Fission and Zapier webhooks" height="600" width="1000">}}

## Fission Serverless Function + Zapier Webhook  - The Use Case

The use case is of a pet food online store called Pawesome.
The user chooses products they wish to purchase and places an order.
They fill a form to complete the order.
Details of this form are sent to a Zapier webhook.

At the Zapier end, we’ve created a Zap to dump the data to a Google Sheet.
The webhook receives the data sent from our application and dumps it in a Google Sheet.

This as you see is a very simple use case of using Fission Serverless Function with Zapier Webhook.
You can in fact make any change to the workflow or create an entirely new use case.

The application is developed in **Python** using **Flask Web Framework**.

## Pre requisites

There are three things that you need to have this application working.

1. Fission
2. Google Account
3. Zapier Starter Account - *the basic Free account doesn’t provide Webhook integration, however you can use their 14-day trial.*

### Fission

Fission as you might know is an Open source serverless framework that runs on top of Kubernetes.
Since the application is deployed as a Fission function, you must have Fission installed in your Kubernetes cluster.
You can refer to our [Fission Installation](/docs/installation) guide for more.

### Google Sheet Setup

Before we start with creating the Zap, we need to create a Google Sheet with the required fields

1. Log in to your Google Sheets/Drive account
2. Create blank spreadsheet
3. In the top row, add the following headers:
    1. name
    2. email
    3. itemOrdered
4. Save the spreadsheet with some name

### Creating a Zap

We will first start by creating a Zapier Webhook and a Zap before working on the application. To do that, follow these steps:

1. Sign In to your Zapier Account.
2. Click **Create Zap** button on top left to create a Zap
3. Choose Webhook from Triggers and select **Catch Hook** at **Trigger Event**
4. At this point, you will have the Zapier Webhook URL
5. In the next step, test the Webhook url by sending dummy data to it, you should see Zapier showing the data that you sent it
6. Next, we create an **Action** that will be performed after the event is triggered
7. Select **Google Sheets** from App Event options & select **Create Spreadsheet Row**
8. Pick your **Google Account** - *the same one where you created the spreadsheet*. It will ask you to allow Zapier to access Google Drive. You need to allow it for this integration to work
9. From the dropdown menu, select the spreadsheet you created earlier and choose a worksheet
10. Zapier will automatically populate the option based on the row headers provided
11. At this point we need the actual data to validate and create the Zap, you can pause here and proceed with the example to generate data, comeback and verify
12. Once the verification is complete, the trigger is created. Give your Zap a name and activate it

{{< figure src="zapier-fission.gif" alt="Fission serverless function with Zapier Webhook integration." height="600" width="1000">}} Above GIF shows how to create a ZAP

## Application Setup & Deployment

Clone the [Pawesome Repo](https://github.com/fission/examples/tree/main/python/ZapierWebhook) to your local system to begin setting up the application.

### Setting up Secret

We will make use of **Kubernetes Secrets** to store and access the `webhook_url`.

Start by encoding the `webhook_url` that you got after creating the Zap

```bash
echo -n 'actual-webhook-url' | base64
EncodedWebhookUrl
```

Create a new `secret.yaml` file and add the encoded string as data. We would be accessing these secrets from our code. Refer to our [documentation on accessing secrets in Fission](https://fission.io/docs/usage/function/access-secret-cfgmap-in-function/) from code.

```yaml
apiVersion: v1
kind: Secret
metadata:
  namespace: default
  name: secret
data:
  webhook_url: EncodedWebhookUrl
type: Opaque
```

Create a Python environment

```bash
fission environment create --name python --image fission/python-env --builder fission/python-builder:latest
```

Create a zip archive as sample.zip archive by executing package.sh script

```bash
./package.sh
```

Create a Package

```bash
fission package create --name fissionzapier-pkg --sourcearchive sample.zip --env python
```

Create the pawesome fission function

```bash
fission fn create --name pawesome --pkg fissionzapier-pkg --entrypoint "main.main" --secret secret
```

Create a route

```bash
fission route create --name pawesome --method POST --method GET --prefix /pawesome --function pawesome
```

## Executing & Running Pawesome

Port forward the service to access it from browser

```bash
kubectl port-forward svc/router 8888:80 -nfission
```

Navigate to `http://127.0.0.1:8888/pawesome` to access the application. Choose any product and click on Place Order. In the dialog box, enter your name and email id rest can be ignored and click on Submit. You should see Order Placed Successfully dialog box. Open the Google Sheet that you had created, you should see a new row added with the `name`, `email id` and `itemOrdered`.

{{< figure src="pawesome.gif" alt="Fission serverless function with Zapier Webhook integration." height="600" width="1000">}} Above GIF shows the Pawesome application.

With this you have successfully automated a simple workflow using Fission serverless function and Zapier webhook.
You can choose any Action and Trigger to create better useful workflows for your use case.

## Conclusion

That's about it for this post.
With this, you now know how to integrate Zapier Webhook with Fission serverless functions.
You can infact extend this use case to integrate with your CRM to track leads.
This way you can focus more on the actual work rather than integrating various applications that you work with.

In case you still have any questions, feel free to reach out to us. We would be happy to help.

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)