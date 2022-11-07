[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]
![awesome-cloudops][awesome-shield]

<br />
<p align="center">
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
<p align="center">
  <h3 align="center">Awesome CloudOps Automation</h3>
  <p align="center">
    CloudOps automation made simpler!
    <br />
    <a href="https://docs.unskript.com/unskript-product-documentation/open-source/cloudops-automation-with-unskript"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://medium.com/unskript">Visit our blog</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>


## Mission
Simplify CloudOps automation for developers and DevOps engineers. 

## Vision 
A single repository to satisfy all your day-to-day CloudOps automation needs. Automate your workflows with our `Actions` that build automated `Runbooks`. 

>Are you looking for a script to automate your Kubernetes management? A script to restart the pod that is OOMkilled? We will cover these workflows (and more!). 



___
<br>

# Quick start Guide

## Get started with Docker:

```
docker run -it -p 8888:8888 \
 -v $HOME/.unskript:/data \
 --user root \
 docker.io/unskript/awesome-runbooks:latest
```

> Note: New files are created inside Docker and will persist unless --rm option is used. If you'd like to also save the credentials and xRunBooks on your local machine, use Docker's -v parameter when you start the container.

## Open and Use a xRunBook
Once your Docker image is up and running, unSkript will be running locally on your computer at http://127.0.0.1:8888/lab/tree/Welcome.ipynb.  A table will display the xRunBooks that are available, with a link to the description and a link to the local version of the xRunBook.

Click on the URL of the xRunBook you would like to explore. It will open in a new browser tab. To run this XRunBook:

1. Check the `Parameters` button at the top of the page. This lists all of the input parameters, and the default values.  Change them if needed.
2. Click on each Action in the xRunBook.  The `Configurations` button will show if Credentials are needed, and which inputs are used for each action.
3. Once each Action has been assigned Credentials and inputs, run each Action (in order) to run your xRunBook.

## Included xRunBooks 

These xRunBooks are included in every install.  Use them as is, or make a copy to modify for your use!

| **Category**                                                                                               | **Runbooks**                                                                                                                                                                 | **URL**                                                                                                    |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| AWS | [AWS Access Key Rotation](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Access_Key_Rotation.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/AWS_Access_Key_Rotation.ipynb)
| AWS | [Add new IAM user](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Add_new_IAM_user.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Add_new_IAM_user.ipynb)
| AWS | [Configure url endpoint on a cloudwatch alarm](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Configure_url_endpoint_on_a_cloudwatch_alarm.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Configure_url_endpoint_on_a_cloudwatch_alarm.ipynb)
| AWS | [Delete Unattached EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Delete_Unattached_EBS_Volume.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Delete_Unattached_EBS_Volume.ipynb)
| AWS | [Detach Instance from ASG and Load Balancer](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detach_Instance_from_ASG_and_Load_Balancer.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Detach_Instance_from_ASG_and_Load_Balancer.ipynb)
| AWS | [Detect ECS failed deployment](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detect_ECS_failed_deployment.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Detect_ECS_failed_deployment.ipynb)
| AWS | [EC2 Disk Cleanup](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/EC2_Disk_Cleanup.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/EC2_Disk_Cleanup.ipynb)
| AWS | [Enforce HTTP Redirection across AWS ALB](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce_HTTP_Redirection_across_AWS_ALB.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Enforce_HTTP_Redirection_across_AWS_ALB.ipynb)
| AWS | [Enforce Mandatory Tags Across All AWS Resources](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce_Mandatory_Tags_Across_All_AWS_Resources.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Enforce_Mandatory_Tags_Across_All_AWS_Resources.ipynb)
| AWS | [Find EC2 Instances Scheduled to retire](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Find_EC2_Instances_Scheduled_to_retire.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Find_EC2_Instances_Scheduled_to_retire.ipynb)
| AWS | [Get Aws Elb Unhealthy Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Get_Aws_Elb_Unhealthy_Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Get_Aws_Elb_Unhealthy_Instances.ipynb)
| AWS | [Lowering AWS CloudTrail Costs by Removing Redundant Trails](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Lowering_AWS_CloudTrail_Costs_by_Removing_Redundant_Trails.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Lowering_AWS_CloudTrail_Costs_by_Removing_Redundant_Trails.ipynb)
| AWS | [Monitor AWS DynamoDB provision capacity](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Monitor_AWS_DynamoDB_provision_capacity.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Monitor_AWS_DynamoDB_provision_capacity.ipynb)
| AWS | [Notify about unused keypairs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Notify_about_unused_keypairs.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Notify_about_unused_keypairs.ipynb)
| AWS | [Publicly Accessible Amazon RDS Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Publicly_Accessible_Amazon_RDS_Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Publicly_Accessible_Amazon_RDS_Instances.ipynb)
| AWS | [Remediate unencrypted S3 buckets](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Remediate_unencrypted_S3_buckets.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Remediate_unencrypted_S3_buckets.ipynb)
| AWS | [Renew SSL Certificate](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Renew_SSL_Certificate.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Renew_SSL_Certificate.ipynb)
| AWS | [Resize EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_EBS_Volume.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize_EBS_Volume.ipynb)
| AWS | [Resize List Of Pvcs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_List_Of_Pvcs.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize_List_Of_Pvcs.ipynb)
| AWS | [Resize PVC](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_PVC.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize_PVC.ipynb)
| AWS | [Restart AWS EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_AWS_EC2_Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart_AWS_EC2_Instances.ipynb)
| AWS | [Restart Aws Instance given Tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_Aws_Instance_given_Tag.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart_Aws_Instance_given_Tag.ipynb)
| AWS | [Restart Unhealthy Services Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_Unhealthy_Services_Target_Group.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart_Unhealthy_Services_Target_Group.ipynb)
| AWS | [Restrict S3 Buckets with READ WRITE Permissions](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restrict_S3_Buckets_with_READ_WRITE_Permissions.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restrict_S3_Buckets_with_READ_WRITE_Permissions.ipynb)
| AWS | [Run EC2 from AMI](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Run_EC2_from_AMI.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Run_EC2_from_AMI.ipynb)
| AWS | [Secure Publicly accessible Amazon RDS Snapshot](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Secure_Publicly_accessible_Amazon_RDS_Snapshot.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Secure_Publicly_accessible_Amazon_RDS_Snapshot.ipynb)
| AWS | [Stop Untagged EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Stop_Untagged_EC2_Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Stop_Untagged_EC2_Instances.ipynb)
| AWS | [Terminate EC2 Instances Without Valid Lifetime Tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Terminate_EC2_Instances_Without_Valid_Lifetime_Tag.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Terminate_EC2_Instances_Without_Valid_Lifetime_Tag.ipynb)
| AWS | [Troubleshooting Your EC2 Configuration in Private Subnet](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Troubleshooting_Your_EC2_Configuration_in_Private_Subnet.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Troubleshooting_Your_EC2_Configuration_in_Private_Subnet.ipynb)
| AWS | [Update and Manage AWS User Permission](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Update_and_Manage_AWS_User_Permission.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Update_and_Manage_AWS_User_Permission.ipynb)
| Jenkins | [Fetch Jenkins Build Logs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Jenkins/Fetch_Jenkins_Build_Logs.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Fetch_Jenkins_Build_Logs.ipynb)
| Kubernetes | [Get Kube System Config Map](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Get_Kube_System_Config_Map.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Get_Kube_System_Config_Map.ipynb)
| Kubernetes | [K8S Get Candidate Nodes Given Config](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Get_Candidate_Nodes_Given_Config.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Get_Candidate_Nodes_Given_Config.ipynb)
| Kubernetes | [K8S Pod Stuck In CrashLoopBack State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb)
| Kubernetes | [K8S Pod Stuck In ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb)
| Kubernetes | [K8S Pod Stuck In Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_Terminating_State.ipynb)
| Kubernetes | [Rollback k8s Deployment and Update Jira](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Rollback_k8s_Deployment_and_Update_Jira.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Rollback_k8s_Deployment_and_Update_Jira.ipynb)
| Mongo | [MongoDB Server Connectivity](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Mongo/MongoDB_Server_Connectivity.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/MongoDB_Server_Connectivity.ipynb)
| MySQL | [MySQL Long Run Query](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/MySQL/MySQL_Long_Run_Query.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/MySQL_Long_Run_Query.ipynb)
| Postgresql | [Display postgresql long running](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Postgresql/Display_postgresql_long_running.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Display_postgresql_long_running.ipynb)



## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Check out our [Contribution Guidelines](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/CONTRIBUTING.md) for more details. 

### How to Contribute?

1. Work with us on any of our [open issues](https://github.com/unskript/awesome-cloudops-automation/issues).
2. Create a new Action. Read the [Action developer guide](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/DEVELOPERGUIDE.md) for more details.
3. Combine Actions into a xRunBook.  Your xRunBook will be featured on the ReadMe.  [What's a xRunBook?](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/Anatomy-of-Runbook.md)



### Contribution Tips:
1. Use the [Docker environment](#get-started-with-docker), or our free [cloud sandbox](https://us.app.unskript.io/profiles/6c38d3da1cde7b3c0623d138f525a5508a3260c8) for testing your contribution.
2. Join our [Slack Community](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) so you can present yourself and get support.

### Step by step process for HacktoberFest
#### Issues
1. Find or propose an issue you want to work on. 
2. Prepare the issue before you start working on it. 
    - Make sure the description is clear. 
    - Tag yourself in Assignees section. 

3. To create a new xRunBook:
  
  - **Using Docker**:
    1. `git clone https://github.com/unskript/Awesome-CloudOps-Automation`
    2. `cd Awesome-CloudOps-Automation`
    3. ```CONTAINER=`docker ps -l | grep awesome-runbooks | awk '{print $1}'` ```
    4. `docker cp templates/runbooks/GCP.ipynb $CONTAINER:/home/jovyan/runbooks/`<YOUR_RUNBOOK_NAME.ipynb>
    5. Point your browser to `http://127.0.0.1:8888/lab/tree/<YOUR_RUNBOOK_NAME.ipynb>` to begin editing.
  - **unSkript sandbox**:
    1. The onboarding flow will drop you into Runbook creation with sandbox credentials
    2.  Start building your lego from the proposed handle (GCP, k8s et al)
5. Create a branch
6. Copy over the template directory into a directory naming your connector and your Action(lego) name:
```
cp -r templates/legos <your_connector>/legos/<your_lego_name> 
```
>For Example: `cp -r templates/legos GCP/legos/gcp_filter_instance_by_label` will create a gcp_filter_instance_by_label xRunBook in the GCP directory.

7. To create a Lego/action, you need to populate 4 files
    - lego.json : add the description, headline and function_name
    - lego.py : copy over the code you wrote inside the Jupyter interface into this file. 
      * To Copy foober.ipynb from Docker to your local machine:
       * ```CONTAINER=`docker ps -l | grep awesome-runbooks | awk '{print $1}'` ```
      *  ```docker cp $CONTAINER:/home/jovyan/runbooks/foobar.ipynb foobar.ipynb```

    - README.md : some description about what the lego does
    - 1.png : a screenshot of the output of your code
7. Open a Pull Request and add a member of the core team as Reviewer (Jayasimha, Shloka, Amit, Abhishek)
9. Expect feedback and merge in the next 48h-72h.
10. Once merged, promote your work on LinkedIn, Twitter and other social media channels! (Optional, but people need to know you are awesome 😉)


![](https://github.com/unskript/Awesome-CloudOps-Automation/blob/9ca0b1a41bf0215933f09c2651a0d199cd702b90/.github/onboarding_hfest_2022.gif?raw=true)


##### Guideline to create Runbook

You can read the [Guideline for creating a Runbook](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/guidelines-to-creating-runbook.md)


## HacktoberFest 2022 Resource

The resources that are available for testing for our HacktoberFest are [here](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/hfest_2022_resource.md)


## Community
[Join the CloudOps Community Slack Channel](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to connect with other users, contributors and awesome people behind awesome CloudOps automation project. 

## Roadmap

See the [open issues](https://github.com/unskript/awesome-cloudops-automation/issues) for a list of proposed features (and known issues).


## License
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
