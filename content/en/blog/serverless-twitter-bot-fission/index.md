+++
title = "Developing a Serverless Twitter Bot on Fission"
date = "2022-04-01T11:30:34+05:30"
author = "Atulpriya Sharma"
description = "Developing a Serverless Twitter Bot on Fission using Python"
categories = ["Tutorials"]
type = "blog"
images = ["images/featured/serverless-twitterbot-fission.png"]
+++

Social Media can be extremely overwhelming whilst being useful. Twitter of all is one of the most hyperactive social media platforms. If you are an enterprise, most likely you’ll have tons of tweets  and DMs to reply to. While there are off the shelf tools available to help you do that, there’s always some missing functionality.

So why not develop a solution on your own? In today’ post I’ll show you how to develop a serverless Twitter Bot running on Fission. The simple application will show you how to use Twitter API and deploy the bot as a serverless function in Fission on your Kubernetes cluster.

{{< figure src="/images/featured/serverless-twitterbot-fission.png" alt="Developing Serverless Twitter Bot on Fission" height="600" width="1000">}}

## Understanding Serverless The Twitter Bot

Before I take you through the code, let me help you understand what our serverless Twitter Bot will do. Below are a few pointers to help you understand the app and the use case better:

* Respond to any tweet that mentions you with a generic message
* Send a notification to Slack channel about the mention
* Will be deployed as Fission function
* Will execute at regular intervals using Fission’s [Time Trigger](/docs/usage/triggers/timer/)

The serverless Twitter bot is developed in Python language and uses the following libraries:

* **[Tweepy](https://www.tweepy.org/)** - Twitter SDK in Python to interact with Twitter
* **[Slack SDK](https://slack.dev/python-slack-sdk/)** - Slack SDK in Python to send notification to Slack channel

> Note: To ensure that our application doesn’t violate Twitter policy, we’ve restricted it to check for mentions made after our latest tweet. That way the bot will not respond to all the tweets where you were mentioned and spam the feed.

## Pre Requisites

There are a couple things that need to be done before we start writing the code. We need to create a Twitter App, and a Slack App so that we can achieve what we want. Both the applications are free to create and you just need an account.

### Fission

Before you start working on this demo, you need to ensure that you have Fission installed and running on your system. You can refer to our [Fission Installation](/docs/installation) guide for more.

### Creating a Twitter App

1. Head to [Twitter Developer portal](https://developer.twitter.com/), if you don't have an account create one. (_note that this will be the account on which our bot will run_)
2. Create a **New Project** and provide details like Project Name, Use Case and Project Description.
3. On the next page, choose **Create New App**.
4. Select App Environment as Development and provide an **App Name**.
5. Save the **API Keys** and Secrets generated.
6. From the Project Page, choose **OAuth** from User Authentication Settings.
7. Turn on **OAuth 1.0a** option and choose Read and Write.
8. Provide a random **callback url** and **website url**.
9. Back on the Project Page, navigate to Keys and Tokens.
10. Under Authentication Tokens, generate Access Token and Secret. Make sure it says "_Created with Read and Write Permissions_"

{{< figure src="twitterbot.gif" alt="Developing Serverless Twitter Bot on Fission" height="600" width="1000">}} Above GIF shows how to create the Twitter application.

At this point, your Twitter App is ready to be used. Make sure to save `consumer_key`,`consumer_secret`,`access_token`,`access_token_secret`, we will need this later

### Creating a Slack App

1. Head to [Slack API portal](https://api.slack.com/), if you don't have an account create one.
2. Click on Create A New App and create it from Scratch.
3. Provide a unique **App Name**.
4. Select a **Slack Workspace** - _you should be a part of some workspace_
5. On the basic information page, select **Incoming Webhooks** and activate it.
6. Click on Add New Webhook to workspace
7. In a new window, select/enter a new channel name. This is the channel to which your slack app will send notifications.
8. At this point, you'll have the **Slack webhook url** with you.

{{< figure src="slackbot.gif" alt="Developing Serverless Twitter Bot on Fission" height="600" width="1000">}} Above GIF shows how to create the Slack application.

We have successfully created a Twitter App and a Slack App. Let's now create the application.

## Creating Twitter Bot

You can clone the [TwitterBot repository](https://github.com/fission/examples/tree/main/python/TwitterBot) to create this application. Remember ot update the code with your tokens, keys and usernames.

`app.py` is the file which has the actual code. Make sure to update the `username` in `app.py` before running the script.

As we are using sensitive information like tokens and secrets, we will use **Kubernetes Secrets** to store these and access them in the code

* `consumer_key` - Consumer Key
* `consumer_secret` - Consumer Secret
* `access_token` - OAuth Access Token
* `access_token_secret` - OAuth Access Token Secret

Start by encoding all the keys and secrets

``` bash
echo -n 'actual-consumer-key' | base64
EncodedConsumerKey==

echo -n 'actual-consumer-secret' | base64
EncodedConsumerSecret==

echo -n 'actual-access-token' | base64
EncodedAccessToken==

echo -n 'actual-access-token-secret' | base64
EncodedAccessTokenSecret==
```

Create a new `secrets.yaml` file and add the encoded strings as data. We would be accessing these secrets from our code. Refer to our documentation on [accessing secrets in Fission](https://fission.io/docs/usage/function/access-secret-cfgmap-in-function/) from code.

```yaml
apiVersion: v1
kind: Secret
metadata:
  namespace: default
  name: twitter-secret
data:
  consumer_key: EncodedConsumerKey==
  consumer_secret:  EncodedConsumerSecret==
  access_token: EncodedAccessToken==
  access_token_secret:  EncodedAccessTokenSecret==
type: Opaque
```

Deploy the secret using `kubectl apply -f secrets.yaml`

## Deploying Twitter Bot to Fission

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
fission package create --name fissiontwitter-pkg --sourcearchive sample.zip --env python --buildcmd "./build.sh"
```

Create the tweetbot fission function

```bash
fission fn create --name tweetbot --pkg fissiontwitter-pkg --entrypoint "app.main" --secret twitter-secret
```

## Running the Serverless Twitter Bot

At this point, our bot is successfully deployed as a Fission function. To test this, you first need to send a tweet mentioning the user. Post that execute our `tweetbot` function

```bash
fission fn test --name tweetbot
```

You should see that the bot has executed successfully by replying to the tweet and even sending a message in Slack.

{{< imgproc tweetresponse.png Fit "500X500" >}}
Our Twitter Bot responding to a tweet mentioning the user
{{< /imgproc >}}

{{< imgproc twitterbotslackmention.png Fit "500X500" >}}
Notification in slack channel
{{< /imgproc >}}

Now to automate this, one of the easiest ways is to let the **function execute at a pre-defined interval**. This can be achieved using [Fission Time trigger](/docs/usage/triggers/timer/). Creating a time trigger will ensure that your function is called after a set interval.

Below is how you can create a time trigger to run the function after every minute.

```bash
fission timer create --name minute --function tweetbot --cron "@every 1m"
```

With this you have successfully developed a serverless Twitter bot that can respond to mentions. Anyone who mentions you in a tweet, the bot will automatically respond to it with the generic message and drop a notification in your Slack channel.

## Conclusion

That’s about how you can create a serverless Twitter bot. This is useful whether you are an individual or an enterprise. You can very well modify the code to suit your requirements and extend the use case. Since this is running a serverless function on Fission, migrating it is easier. If you are still contemplating on why you should use Fission, you should read our post on [reasons to choose Fission](/blog/4-reasons-to-choose-fission-kubernetes-serverless-framework/).

In case you still have any questions, feel free to reach out to us. We would be happy to help.

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)