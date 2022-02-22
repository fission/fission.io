+++
title = "Function Composition: What It Means, and Why You Should Care"
date = "2018-06-08T11:39:15-07:00"
author = "Timirah James"
description = "Composing Fission functions with Fission Workflows"
categories = ["Fission"]
type = "blog"
+++

FaaS Functions give you the ability to quickly deploy services made of small functionality.  But any more complex use case requires multiple functions.  What are the different approaches to this?  What are the parameters on the basis of which we should compare these approaches?  

In this short blog post, I’ll briefly go over the significance of function composition and why you should care about it. 


## First off, What is Function Composition
	
Function composition refers to combining single functions to create bigger, more complex functions. I like to think of it as creating “super function combinations” in order to gain more dynamic and effective functionality -- each function being a building block in the orchestration of an application’s data and/or control flow.


## Why does Function Composition matter?
The way you compose serverless functions can be a vital and determining factor when deploying functions, and tends to have direct influence over how your functions are deployed -- from latency, to resource usage (and corresponding costs), to the weight of the responsibility that a developer will have pertaining to the overall success or failure of functions altogether. 

For example, combining all your functions together into one big FaaS function from a source level (or manual compilation) might just be the simplest way to compose your functions, right? Right. 

However, composing your functions this way can actually turn out to cost you more than it benefits you. While you won’t have to deal with the overhead of serialization, you will have to deal with the restriction of not being able to scale your functions independently as they are all handled and deployed as one single serverless function. This could be prove to be wasteful. With each function performing its own task, they require their own amounts of resources, CPU, memory, etc. So in a case where a request is made that only requires one specific function, sufficient resources for the whole set of functions would be needed. This case defeats the purpose of utilizing functions as a service in the first place -- to only pay for the resources you that you’ve actually used. If the need and execution of a function is not immediate, you should not have to pay for it. 


There are several different approaches to composing functions, from direct chaining, to event-driven, to workflows. Each approach comes with its own set of benefits and takeaways, which is why it’s essential to explore and decide which approach(es) make sense for your application and what you’re willing to risk. 

## Learn More at Velocity San Jose!

To learn about more different approaches of function composition along with advantages and disadvantages for each style, be sure to catch myself and Soam Vasani’s talk session **_“Function Composition in a Serverless World”_** next week at [O’Reilly’s Velocity Conference](https://conferences.oreilly.com/velocity/vl-ca) in San Jose, on Friday, June 14th!


**Follow us on Twitter for more updates! [@fissionio](https://www.twitter.com/fissionio)**

--- 


**_Author:_**

* Timirah James **|** Fission Developer Advocate, Platform9 Systems  **|**  [Tweet the Author](https://www.twitter.com/timirahj)

