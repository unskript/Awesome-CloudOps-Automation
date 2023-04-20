[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]


<br />
<p align="center">
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
<p align="center">
  <h3 align="center">Awesome CloudOps Automation</h3>
  <p align="center">
    <img src=https://img.shields.io/static/v1?label=ActionCount&message=466&color=green><img src=https://img.shields.io/static/v1?label=xRunBookCount&message=54&color=orange>
  
  <p align="center">
    CloudOps automation made simple!
    <br />
    <a href="https://docs.unskript.com/unskript-product-documentation/open-source/cloudops-automation-with-unskript"><strong>Explore the docs</strong></a>
    <br />
      <a href="https://www.youtube.com/channel/UCvtSYNHVvuogq2u-F7UDMkw"><strong>unSkript on YouTube</strong></a>
    <br />
    <br />
    <a href="https://unskript.com/blog">Visit our blog</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>


## Mission
Simplify CloudOps automation for developers and DevOps engineers. 

## Vision 
A single repository to satisfy all your day-to-day CloudOps automation needs. Automate your workflows with our *Actions* that build automated *RunBooks*. 

With hundreds of Actions and RunBooks included in the repository, you can get started quickly with minimal toil.

>**Better. Faster. Smarter SRE.**

___
<br>

# Quick Start Guide



## Open Source Docker

Our Docker install is and will always be open source. It includes a Jupyter runtime and all of the prebuilt Actions and RunBooks. Build your own Actions and RunBooks

### Get Started
1.  Clone this repository to your local machine to your $HOME directory. 

```
cd $HOME
git clone https://github.com/unskript/Awesome-CloudOps-Automation 
cd Awesome-CloudOps-Automation
```

2.  Launch Docker. (if you used a different directory in #1, update that in the first ```-v``` line.)

```
docker run -it -p 8888:8888 \
 -v $HOME/Awesome-CloudOps-Automation/custom:/data \
 -v $HOME/.unskript:/unskript \
 --user root \
 docker.io/unskript/awesome-runbooks:latest
```

* [YouTube Playlist with step by step guides](https://www.youtube.com/watch?v=QT0sghAo_t0&list=PLG7TPzTSJYkfCAtWKpdTjlRcyS21mXsE2)

---
## Cloud Free Trial
* Our Cloud Free Trial features everything found in Open Source, plus some basic enterprise features like [scheduling](https://docs.unskript.com/unskript-product-documentation/guides/xrunbooks/schedules) and [environments](https://docs.unskript.com/unskript-product-documentation/guides/proxies/connect-your-environment). 
* [Free Trial: Cloud](https://us.app.unskript.io/) 
* [YouTube Tutorials using Free Trial](https://www.youtube.com/watch?v=QjqAcJEiQNo&list=PLG7TPzTSJYkeOIAOj9iaxCaczKHX_qwZ_)

---
<br/>

# Open and Use a xRunBook

|**`Open Source Docker`**    | **`             Free Trial: Cloud             `** |
| :---: | :---: |
| Once Docker is running, your unSkript install can be found at http://127.0.0.1:8888/lab/tree/Welcome.ipynb. | Once you have completed the Onboarding Flow, every RunBook can be found in the xRunBooks link, under the *unSkript xRunBooks* tab |
| A table lists the xRunBooks that are available. Click on the URL of the xRunBook you would like to explore. | You can Search, or select a category or RunBook. To open a xRunBook, Click the 3 dot menu and import into your workspace. |




1. Check the `Parameters` button at the top of the page. This lists all of the input parameters, and the default values.  Change them as needed.
2. Click on each Action in the xRunBook.  The `Configurations` button will show if Credentials are needed, and the inputs required for the Action to be run. [How to Add Credentials](https://docs.unskript.com/unskript-product-documentation/guides/connectors).
3. Once each Action has been assigned Credentials and inputs, run each Action (in order) to run your xRunBook.



## Included xRunBooks
<details>
  <summary><b>See Full List</b></summary>

  These xRunBooks are included in every install.  Use them as is, or make a copy to modify for your use!

  | **Category**                                                                                               | **Runbooks**                                                                                                                                                                 | **URL**                                                                                                    |
  | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
  |AWS |[AWS Access Key Rotation for IAM users](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Access_Key_Rotation.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/AWS_Access_Key_Rotation.ipynb) | 
|AWS |[AWS Add Mandatory tags to EC2](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Add_Mandatory_tags_to EC2.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/AWS_Add_Mandatory_tags_to EC2.ipynb) | 
|AWS |[Create a new AWS IAM User](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Add_new_IAM_user.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Add_new_IAM_user.ipynb) | 
|AWS |[Change AWS EBS Volume To GP3 Type](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Change_AWS_EBS_Volume_To_GP3_Type.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Change_AWS_EBS_Volume_To_GP3_Type.ipynb) | 
|AWS |[Configure URL endpoint on a AWS CloudWatch alarm](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Configure_url_endpoint_on_a_cloudwatch_alarm.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Configure_url_endpoint_on_a_cloudwatch_alarm.ipynb) | 
|AWS |[Copy AMI to All Given AWS Regions](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Copy_ami_to_all_given_AWS_regions.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Copy_ami_to_all_given_AWS_regions.ipynb) | 
|AWS |[Create IAM User with policy](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Create_IAM_User_with_policy.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Create_IAM_User_with_policy.ipynb) | 
|AWS |[Delete Unattached AWS EBS Volumes](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Delete_Unattached_EBS_Volume.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Delete_Unattached_EBS_Volume.ipynb) | 
|AWS |[Delete Unused AWS Secrets](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Delete_Unused_AWS_Secrets.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Delete_Unused_AWS_Secrets.ipynb) | 
|AWS |[Detach EC2 Instance from ASG](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detach_Instance_from_ASG.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Detach_Instance_from_ASG.ipynb) | 
|AWS |[Detach EC2 Instance from ASG and Load balancer](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detach_ec2_Instance_from_ASG.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Detach_ec2_Instance_from_ASG.ipynb) | 
|AWS |[Detect ECS failed deployment](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detect_ECS_failed_deployment.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Detect_ECS_failed_deployment.ipynb) | 
|AWS |[AWS EC2 Disk Cleanup](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/EC2_Disk_Cleanup.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/EC2_Disk_Cleanup.ipynb) | 
|AWS |[Enforce HTTP Redirection across all AWS ALB instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce_HTTP_Redirection_across_AWS_ALB.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Enforce_HTTP_Redirection_across_AWS_ALB.ipynb) | 
|AWS |[Enforce Mandatory Tags Across All AWS Resources](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce_Mandatory_Tags_Across_All_AWS_Resources.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Enforce_Mandatory_Tags_Across_All_AWS_Resources.ipynb) | 
|AWS |[Handle AWS EC2 Instance Scheduled to retire](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Find_EC2_Instances_Scheduled_to_retire.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Find_EC2_Instances_Scheduled_to_retire.ipynb) | 
|AWS |[Get unhealthy EC2 instances from ELB](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Get_Aws_Elb_Unhealthy_Instances.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Get_Aws_Elb_Unhealthy_Instances.ipynb) | 
|AWS |[Lowering AWS CloudTrail Costs by Removing Redundant Trails](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Lowering_AWS_CloudTrail_Costs_by_Removing_Redundant_Trails.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Lowering_AWS_CloudTrail_Costs_by_Removing_Redundant_Trails.ipynb) | 
|AWS |[Monitor AWS DynamoDB provision capacity](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Monitor_AWS_DynamoDB_provision_capacity.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Monitor_AWS_DynamoDB_provision_capacity.ipynb) | 
|AWS |[List unused Amazon EC2 key pairs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Notify_about_unused_keypairs.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Notify_about_unused_keypairs.ipynb) | 
|AWS |[Publicly Accessible Amazon RDS Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Publicly_Accessible_Amazon_RDS_Instances.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Publicly_Accessible_Amazon_RDS_Instances.ipynb) | 
|AWS |[Remediate unencrypted S3 buckets](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Remediate_unencrypted_S3_buckets.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Remediate_unencrypted_S3_buckets.ipynb) | 
|AWS |[Renew AWS SSL Certificates that are close to expiration](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Renew_SSL_Certificate.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Renew_SSL_Certificate.ipynb) | 
|AWS |[Resize EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_EBS_Volume.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Resize_EBS_Volume.ipynb) | 
|AWS |[Resize list of pvcs.](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_List_Of_Pvcs.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Resize_List_Of_Pvcs.ipynb) | 
|AWS |[Resize PVC](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_PVC.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Resize_PVC.ipynb) | 
|AWS |[Restart AWS EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_AWS_EC2_Instances_By_Tag.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Restart_AWS_EC2_Instances_By_Tag.ipynb) | 
|AWS |[Restart AWS Instances with a given tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_Aws_Instance_given_Tag.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Restart_Aws_Instance_given_Tag.ipynb) | 
|AWS |[Restart unhealthy services in a Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_Unhealthy_Services_Target_Group.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Restart_Unhealthy_Services_Target_Group.ipynb) | 
|AWS |[Restrict S3 Buckets with READ/WRITE Permissions to all Authenticated Users](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restrict_S3_Buckets_with_READ_WRITE_Permissions.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Restrict_S3_Buckets_with_READ_WRITE_Permissions.ipynb) | 
|AWS |[Launch AWS EC2 from AMI](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Run_EC2_from_AMI.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Run_EC2_from_AMI.ipynb) | 
|AWS |[Secure Publicly accessible Amazon RDS Snapshot](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Secure_Publicly_accessible_Amazon_RDS_Snapshot.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Secure_Publicly_accessible_Amazon_RDS_Snapshot.ipynb) | 
|AWS |[Stop Untagged AWS EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Stop_Untagged_EC2_Instances.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Stop_Untagged_EC2_Instances.ipynb) | 
|AWS |[Terminate EC2 Instances Without Valid Lifetime Tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Terminate_EC2_Instances_Without_Valid_Lifetime_Tag.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Terminate_EC2_Instances_Without_Valid_Lifetime_Tag.ipynb) | 
|AWS |[Troubleshooting Your EC2 Configuration in a Private Subnet](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Troubleshooting_Your_EC2_Configuration_in_Private_Subnet.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Troubleshooting_Your_EC2_Configuration_in_Private_Subnet.ipynb) | 
|AWS |[Update and Manage AWS User permission](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Update_and_Manage_AWS_User_Permission.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/Update_and_Manage_AWS_User_Permission.ipynb) | 
|AWS |[AWS Redshift Get Daily Costs from AWS Products](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/aws_redshift_get_daily_product_costs.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/aws_redshift_get_daily_product_costs.ipynb) | 
|AWS |[AWS Redshift Get Daily Costs from EC2 Usage](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/aws_redshift_get_ec2_daily_costs.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/aws_redshift_get_ec2_daily_costs.ipynb) | 
|AWS |[AWS Redshift Update Database](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/aws_redshift_update_database.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/aws_redshift_update_database.ipynb) | 
|AWS |[Delete IAM profile](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/delete_iam_user.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/AWS/delete_iam_user.ipynb) | 
|ElasticSearch |[Elasticsearch Rolling restart](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/ElasticSearch/Elasticsearch_Rolling_Restart.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/ElasticSearch/Elasticsearch_Rolling_Restart.ipynb) | 
|Jenkins |[Fetch Jenkins Build Logs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Jenkins/Fetch_Jenkins_Build_Logs.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Jenkins/Fetch_Jenkins_Build_Logs.ipynb) | 
|Jira |[Jira Visualize Issue Time to Resolution](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Jira/jira_visualize_time_to_resolution.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Jira/jira_visualize_time_to_resolution.ipynb) | 
|Kubernetes |[k8s: Delete Evicted Pods From All Namespaces](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Delete_Evicted_Pods_From_Namespaces.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/Delete_Evicted_Pods_From_Namespaces.ipynb) | 
|Kubernetes |[k8s: Get kube system config map](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Get_Kube_System_Config_Map.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/Get_Kube_System_Config_Map.ipynb) | 
|Kubernetes |[k8s: Get candidate nodes for given configuration](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Get_Candidate_Nodes_Given_Config.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/K8S_Get_Candidate_Nodes_Given_Config.ipynb) | 
|Kubernetes |[Kubernetes Log Healthcheck](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Log_Healthcheck.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/K8S_Log_Healthcheck.ipynb) | 
|Kubernetes |[k8s: Pod Stuck in CrashLoopBackoff State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb) | 
|Kubernetes |[k8s: Pod Stuck in ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb) | 
|Kubernetes |[k8s: Pod Stuck in Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb) | 
|Kubernetes |[k8s: Resize List of PVCs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Resize_List_of_PVCs.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/Resize_List_of_PVCs.ipynb) | 
|Kubernetes |[k8s: Resize PVC](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Resize_PVC.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/Resize_PVC.ipynb) | 
|Kubernetes |[Rollback Kubernetes Deployment](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Rollback_k8s_Deployment_and_Update_Jira.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Kubernetes/Rollback_k8s_Deployment_and_Update_Jira.ipynb) | 
|Postgresql |[Display long running queries in a PostgreSQL database](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Postgresql/Display_Postgresql_Long_Running.ipynb) | [Open in Browser](http://127.0.0.1:8888/lab/tree/Postgresql/Display_Postgresql_Long_Running.ipynb) | 

</details>

<br/>
<br/>


# Contribute to Awesome-CloudOps-Automation

All contributions are **greatly appreciated**. Check out our [Contribution Guidelines](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/CONTRIBUTING.md) for more details. 

## How to Contribute?

1. Work with us on any of our [open issues](https://github.com/unskript/awesome-cloudops-automation/issues).
2. Create a new Action. Read the [Action developer guide](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/DEVELOPERGUIDE.md) for more details.
3. Combine Actions into a xRunBook.  Your xRunBook will be featured on the ReadMe.  [What's a xRunBook?](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/Anatomy-of-Runbook.md)



## Contribution Tips:
1. Use the [Docker environment](#get-started-with-docker), or our free [cloud sandbox](https://us.app.unskript.io/profiles/6c38d3da1cde7b3c0623d138f525a5508a3260c8) for testing your contribution.
2. Join our [Slack Community](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to discuss your PR, and for support if you run into any issues.



## Create a new xRunBook:
  |**`Open Source Docker`**    | **`             Free Trial: Cloud             `** |
| :---: | :---: |
| Your RunBooks are stored locally at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks``` Copy an existing xRunBook and rename it. It will appear in the Welcome page on refresh. Click to Open. | From the xRunBooks Page, Click the **Create New** button. Name you xRunBook, Give it a description, and choose your proxy.  |
| Your saved xRunBook can be found at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks``` | Once you save your xRunBook, navigate to the xRunBooks listing.  The 3 dot menu next to your RunBook has a "Download" option. | 


  1. All created RunBooks have a ipynb file. You'll need to create a .json file with metadata about your RunBook.  Copy from another RunBook un the repository.
  2. Copy the saved RunBook from the Custom folder into the folder of the Connector used, and submit a PR!
  3. Submit Your xRunBook to the repository. Follow the [submission steps](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source) to remove credentials, etc. from your xRunBook.
  

## Create a new Action:

### Create a new action inside an existing RunBook.

   1. If you will not use external credentials, click *+Add Action* at the top of the menu.
   2. If you will be using an existing credential, add an existing Action for that service (like AWS), and edit the code to create your new Action.
   3. If the service you'd like to build for does not have credentials yet, please [file an issue](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=Credential%2Ctriage&template=add_credential.yml&title=%5BCredential%5D%3A+).
### Creating and connecting your Action

1. [Creating Custom Actions](https://docs.unskript.com/unskript-product-documentation/guides/actions/create-custom-actions) describes the steps to create your own Action.
2.  To submit to OSS, follow the [Submit An Action](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source#actions) instructions.  




## Extending Docker
You can use our base docker to extend the functionality to fit your need. Follow this [document](./README_extending_docker.md) to create you own custom docker.

<br/>

## unSkript CLI

With `unskript-ctl.sh` (called unSkript cuttle) allows you to
  * List Existing Runbook
  * List All Existing Health Checks
  * List All Existing Health Check per connector
  * Run All Existing Health Checks 
  * Run All Existing Health Checks per connector
  * Run an existing Runbook


Here are the Options that are supported by the CTL Command
```
unskript-ctl.sh 
usage: unskript-ctl [-h] [-lr] [-rr RUN_RUNBOOK] [-rc RUN_CHECKS] [-df DISPLAY_FAILED_CHECKS] [-lc LIST_CHECKS] [-sa SHOW_AUDIT_TRAIL]

Welcome to unSkript CLI Interface VERSION: 0.1.0

optional arguments:
  -h, --help            show this help message and exit
  -lr, --list-runbooks  List Available Runbooks
  -rr RUN_RUNBOOK, --run-runbook RUN_RUNBOOK
                        Run the given runbook
  -rc RUN_CHECKS, --run-checks RUN_CHECKS
                        Run all available checks [all | connector | failed]
  -df DISPLAY_FAILED_CHECKS, --display-failed-checks DISPLAY_FAILED_CHECKS
                        Display Failed Checks [all | connector]
  -lc LIST_CHECKS, --list-checks LIST_CHECKS
                        List available checks, [all | connector]
  -sa SHOW_AUDIT_TRAIL, --show-audit-trail SHOW_AUDIT_TRAIL
                        Show audit trail [all | connector | execution_id]
```


# Community
[Join the CloudOps Community Slack Channel](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to connect with other users, contributors and awesome people behind awesome CloudOps automation project. 

<br/>

# Road Map

See the [open issues](https://github.com/unskript/awesome-cloudops-automation/issues) for a list of proposed features (and known issues).


<br/>

# License
Except as otherwise noted this project is licensed under the `Apache License, Version 2.0` .

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 .

Unless required by applicable law or agreed to in writing, project distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


[contributors-shield]: https://img.shields.io/github/contributors/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[contributors-url]: https://github.com/unskript/awesome-cloudops-automation/graphs/contributors
[github-actions-shield]: https://img.shields.io/github/workflow/status/unskript/awesome-cloudops-automation/e2e%20test?color=orange&label=e2e-test&logo=github&logoColor=orange&style=for-the-badge
[github-actions-url]: https://github.com/unskript/awesome-cloudops-automation/actions/workflows/docker-tests.yml
[forks-shield]: https://img.shields.io/github/forks/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[forks-url]: https://github.com/unskript/awesome-cloudops-automation/network/members
[stars-shield]: https://img.shields.io/github/stars/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[stars-url]: https://github.com/unskript/awesome-cloudops-automation/stargazers
[issues-shield]: https://img.shields.io/github/issues/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[issues-url]: https://github.com/unskript/awesome-cloudops-automation/issues
[twitter-shield]: https://img.shields.io/badge/-Twitter-black.svg?style=for-the-badge&logo=twitter&colorB=555
[twitter-url]: https://twitter.com/unskript
[awesome-shield]: https://img.shields.io/badge/awesome-cloudops-orange?style=for-the-badge&logo=bookstack 
