+++
title = "Fission Functions with ArgoWorkflow"
date = "2022-04-14T11:35:34+05:30"
author = "Neha Gupta"
description = "Create your workflow with Fission and Argo"
categories = ["Tutorials"]
type = "blog"
images = ["images/featured/fission-zapier-featured.png"]
+++

Fission Function allow user to perform one logical task. To group multiple task together such as one function is dependent on other we can use Argo Workflows. Argo Workflows is an open source container-native workflow engine with a feature to create DAGs i.e running task sequentially, parallely and with dependencies. We will try to develop a simple Insurance Eligibility programe which will take different input and calculate insurance instalment on basis of the inputs.

### Understanding the Insurance Calculator

The small application/Workflow will take basic information from the user and check the eligibility for the Insurance. Below are the input and different tasks which are performed to calculating the above:

* Take firstname of the user
* Take lastname of the user
* Create fullname using the above two.
* Input age and montly salary.
* On basis of predefined criteria i.e. ,
  * if age is below a certain age and yearly salary is above some numbers user lies in a low risk criteria
  * otherwise he/she falls in high risk criteria. And the installments varies accordingly.
* We print the above calculated output to the user.

{{< figure src="/images/featured/insurance-workflow-argo.png" alt="Developing Insurance calculator DAG using Argo" height="400" width="600">}}

## Pre Requisites

### Fission

You should have Fission running on your system. You can refer to our [Fission Installation](/docs/installation) guide for more infromation.

### ArgoWorkflow

For installing latest version ArgoWorkflow, you can refer to [ArgoWorkflow Installation](https://argoproj.github.io/argo-workflows/quick-start/)  

We are ready to build our Insurance Installment calculator now.

### Creating Fission functions and triggers

We have to create all the functions which would be helping us with the calculation. You can refer to [Fission Function](https://github.com/neha-Gupta1/argo-workflow/tree/main/insurance/fission-functions) folder for all the functions required for this application. Clone the above folder and run below command -

`sudo chmod 755 insurance/fission-functions/spec.sh`

Verifing the Fission function and Trigger creation,

```bash
$ fission fn list
NAME              ENV    EXECUTORTYPE MINSCALE MAXSCALE MINCPU MAXCPU MINMEMORY MAXMEMORY SECRETS CONFIGMAPS
get-full-name     go     poolmgr      0        0        0      0      0         0
highriskinsurance go     poolmgr      0        0        0      0      0         0
lowriskinsurance  go     poolmgr      0        0        0      0      0         0
set-age           go     poolmgr      0        0        0      0      0         0
set-first-name    go     poolmgr      0        0        0      0      0         0
set-last-name     go     poolmgr      0        0        0      0      0         0
set-salary        go     poolmgr      0        0        0      0      0         0
```

```bash
$ fission httptrigger list
NAME                                 METHOD URL                     FUNCTION(s)       INGRESS HOST PATH                    TLS ANNOTATIONS
65222407-76ed-43b2-97d9-160d5bc61c36 [GET]  /hello                  hello             false   *    /hello                      
getfullname                          [GET]  /getfullnamehandler     get-full-name     false   *    /getfullnamehandler         
gethighriskinsurance                 [GET]  /getHighRiskEligibility highriskinsurance false   *    /getHighRiskEligibility     
getlowriskinsurance                  [GET]  /getLowRiskEligibility  lowriskinsurance  false   *    /getLowRiskEligibility      
postage                              [GET]  /setage                 set-age           false   *    /setage                     
postfirstname                        [GET]  /postfirstname          set-first-name    false   *    /postfirstname              
postlastname                         [GET]  /postlastname           set-last-name     false   *    /postlastname               
postsalary                           [GET]  /setmonthlysalary       set-salary        false   *    /setmonthlysalary  
```

### Running the application

The above function helped us in creating independent logics. Now we are going to club them together and create a workflow using Argo. This workflow takes its decision on basis of input provided.

```bash
argo submit --watch insurance/insuranceDag.yaml 

Name:                hello-argo-4n4pm
Namespace:           fission
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Running
Created:             Tue Sep 20 10:56:57 +0530 (10 seconds ago)
Started:             Tue Sep 20 10:56:57 +0530 (10 seconds ago)
Duration:            10 seconds
Progress:            0/4
Parameters:          
  age:               35
  salary:            20000

STEP                   TEMPLATE          PODNAME  DURATION  MESSAGE
 ● hello-argo-4n4pm    insurance                              
 ├─◷ getage            getage                                 
 ├─◷ getmonthlysalary  getmonthlysalary                       
 ├─◷ postfirstname     postfirstname                          
 └─◷ postlastname      postlastname                           

This workflow does not have security context set. You can run your workflow pods more securely by setting it.
Learn more at https://argoproj.github.io/argo-workflows/workflow-pod-security-context/
```

`--watch` will help us to follow the status of workflow. You can view the logs/output of the Workflow using the below command,

```bash
$ argo logs -f hello-argo-4n4pm

hello-argo-4n4pm-761537852:  _______________________ 
hello-argo-4n4pm-761537852: < {Hello Neha Gupta!! as per your age: 35 We can give you an insurance with assured money 20000} >
hello-argo-4n4pm-761537852:  ----------------------- 
hello-argo-4n4pm-761537852:     \
hello-argo-4n4pm-761537852:      \
hello-argo-4n4pm-761537852:       \     
hello-argo-4n4pm-761537852:                     ##        .            
hello-argo-4n4pm-761537852:               ## ## ##       ==            
hello-argo-4n4pm-761537852:            ## ## ## ##      ===            
hello-argo-4n4pm-761537852:        /""""""""""""""""___/ ===        
hello-argo-4n4pm-761537852:   ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
hello-argo-4n4pm-761537852:        \______ o          __/            
hello-argo-4n4pm-761537852:         \    \        __/             
hello-argo-4n4pm-761537852:           \____\______/   
hello-argo-4n4pm-761537852: time="2022-09-20T05:28:20.770Z" level=info msg="sub-process exited" argo=true error="<nil>"
```

`hello-argo-4n4pm` should be replaced by the Workflow name.
