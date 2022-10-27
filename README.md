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
    <a href="https://unskript.gitbook.io/unskript-product-documentation/open-source"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://medium.com/unskript">Visit our blog</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>



# About the project

## Mission
To make CloudOps automation simpler for developers and DevOps engineers. 

## Vision 
A single repository to satisfy all your day-to-day CloudOps automation needs. Are you looking for a script to automate your Kubernetes management? Or do you need a script to restart the pod that is OOMkilled? We will cover that for you. 
                                                               
## Quick start

### Get started with docker
#### Linux/Mac/Windows (x86-64/arm64)

```
docker run -it -p 8888:8888 \
 -v $HOME/.unskript:/data \
 --user root \
 docker.io/unskript/awesome-runbooks:latest
```


> Inside the docker there is `/data` folder that is where we store the `credentials` and `runbooks`. So if you would like to retain the `connectors` and `runbooks` you can use the docker's `-v` option to retain the changes done on the `docker`.

> Note: New files are created inside the docker and will persist unless --rm option is used.
> 
### Open the Runbook
Once you run the above command, here's the table which will help you find the URL for runbook of your choice. 

| **Category**                                                                                               | **Runbooks**                                                                                                                                                                 | **URL**                                                                                                    |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| AWS | [AWS Access Key Rotation](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Access_Key_Rotation.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/AWS_Access_Key_Rotation.ipynb)
| AWS | [Add new IAM user](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Add-new-IAM-user.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Add-new-IAM-user.ipynb)
| AWS | [Configure url endpoint on a cloudwatch alarm](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb)
| AWS | [Delete Unattached EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Delete_Unattached_EBS_Volume.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Delete_Unattached_EBS_Volume.ipynb)
| AWS | [Detach Instance from ASG and Load Balancer](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detach-Instance-from-ASG-and-Load-Balancer.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Detach-Instance-from-ASG-and-Load-Balancer.ipynb)
| AWS | [Detect ECS failed deployment](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Detect-ECS-failed-deployment.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Detect-ECS-failed-deployment.ipynb)
| AWS | [EC2 Disk Cleanup](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/EC2-Disk-Cleanup.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/EC2-Disk-Cleanup.ipynb)
| AWS | [Enforce HTTP Redirection across AWS ALB](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce-HTTP-Redirection-across-AWS-ALB.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Enforce-HTTP-Redirection-across-AWS-ALB.ipynb)
| AWS | [Enforce Mandatory Tags Across All AWS Resources](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce-Mandatory-Tags-Across-All-AWS-Resources.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Enforce-Mandatory-Tags-Across-All-AWS-Resources.ipynb)
| AWS | [Find EC2 Instances Scheduled to retire](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Find-EC2-Instances-Scheduled-to-retire.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Find-EC2-Instances-Scheduled-to-retire.ipynb)
| AWS | [Get Aws Elb Unhealthy Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Get-Aws-Elb-Unhealthy-Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Get-Aws-Elb-Unhealthy-Instances.ipynb)
| AWS | [Lowering AWS CloudTrail Costs by Removing Redundant Trails](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Lowering-AWS-CloudTrail-Costs-by-Removing-Redundant-Trails.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Lowering-AWS-CloudTrail-Costs-by-Removing-Redundant-Trails.ipynb)
| AWS | [Monitor AWS DynamoDB provision capacity](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Monitor-AWS-DynamoDB-provision-capacity.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Monitor-AWS-DynamoDB-provision-capacity.ipynb)
| AWS | [Notify about unused keypairs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Notify-about-unused-keypairs.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Notify-about-unused-keypairs.ipynb)
| AWS | [Publicly Accessible Amazon RDS Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Publicly-Accessible-Amazon-RDS-Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Publicly-Accessible-Amazon-RDS-Instances.ipynb)
| AWS | [Remediate unencrypted S3 buckets](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Remediate-unencrypted-S3-buckets.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Remediate-unencrypted-S3-buckets.ipynb)
| AWS | [Renew SSL Certificate](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Renew_SSL_Certificate.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Renew_SSL_Certificate.ipynb)
| AWS | [Resize EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize-EBS-Volume.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize-EBS-Volume.ipynb)
| AWS | [Resize List Of Pvcs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize-List-Of-Pvcs.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize-List-Of-Pvcs.ipynb)
| AWS | [Resize PVC](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Resize_PVC.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize_PVC.ipynb)
| AWS | [Restart Aws Instance given Tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart-Aws-Instance-given-Tag.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart-Aws-Instance-given-Tag.ipynb)
| AWS | [Restart Unhealthy Services Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart-Unhealthy-Services-Target-Group.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart-Unhealthy-Services-Target-Group.ipynb)
| AWS | [Restart AWS EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_AWS_EC2_Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart_AWS_EC2_Instances.ipynb)
| AWS | [Restrict S3 Buckets with READ WRITE Permissions](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restrict-S3-Buckets-with-READ-WRITE-Permissions.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Restrict-S3-Buckets-with-READ-WRITE-Permissions.ipynb)
| AWS | [Run EC2 from AMI](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Run-EC2-from-AMI.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Run-EC2-from-AMI.ipynb)
| AWS | [Secure Publicly accessible Amazon RDS Snapshot](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Secure-Publicly-accessible-Amazon-RDS-Snapshot.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Secure-Publicly-accessible-Amazon-RDS-Snapshot.ipynb)
| AWS | [Stop Untagged EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Stop_Untagged_EC2_Instances.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Stop_Untagged_EC2_Instances.ipynb)
| AWS | [Terminate EC2 Instances Without Valid Lifetime Tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Terminate-EC2-Instances-Without-Valid-Lifetime-Tag.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Terminate-EC2-Instances-Without-Valid-Lifetime-Tag.ipynb)
| AWS | [Troubleshooting Your EC2 Configuration in Private Subnet](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Troubleshooting-Your-EC2-Configuration-in-Private-Subnet.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Troubleshooting-Your-EC2-Configuration-in-Private-Subnet.ipynb)
| AWS | [Update and Manage AWS User Permission](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Update-and-Manage-AWS-User-Permission.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Update-and-Manage-AWS-User-Permission.ipynb)
| Jenkins | [Fetch Jenkins Build Logs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Jenkins/Fetch-Jenkins-Build-Logs.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Fetch-Jenkins-Build-Logs.ipynb)
| Kubernetes | [Get Kube System Config Map](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Get-Kube-System-Config-Map.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Get-Kube-System-Config-Map.ipynb)
| Kubernetes | [K8S Get Candidate Nodes Given Config](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S-Get-Candidate-Nodes-Given-Config.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S-Get-Candidate-Nodes-Given-Config.ipynb)
| Kubernetes | [K8S Pod Stuck In CrashLoopBack State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb)
| Kubernetes | [K8S Pod Stuck In ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb)
| Kubernetes | [K8S Pod Stuck In Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_Terminating_State.ipynb)
| Kubernetes | [Rollback k8s Deployment and Update Jira](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Rollback-k8s-Deployment-and-Update-Jira.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Rollback-k8s-Deployment-and-Update-Jira.ipynb)
| Mongo | [MongoDB Server Connectivity](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Mongo/MongoDB_Server_Connectivity.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/MongoDB_Server_Connectivity.ipynb)
| MySQL | [MySQL Long Run Query](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/MySQL/MySQL_Long_Run_Query.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/MySQL_Long_Run_Query.ipynb)
| Postgresql | [Display postgresql long running](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Postgresql/Display-postgresql-long-running.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Display-postgresql-long-running.ipynb)



## Community
[Join the CloudOps Community Workspace](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) on Slack to connect with other users, contributors and awesome people behind awesome CloudOps automation project. 

## Roadmap

See the [open issues](https://github.com/unskript/awesome-cloudops-automation/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**. Check out our [Contribution Guidelines](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/CONTRIBUTING.md) for more details. 

Here is the Link for the [Developer Guide](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/DEVELOPERGUIDE.md)

### How to contribute?

#### Pre-requisites:
1. You can use the docker environment (see instructions above) with your infrastructure credentials for validating your changes. We also have a sandbox where you can do testing : open a free account on [unSkript](https://us.app.unskript.io/profiles/6c38d3da1cde7b3c0623d138f525a5508a3260c8) to access the sandbox. 
2. Join our [Slack Community](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) so you can present yourself and get support

#### Step by step process for Hacktoberfest
1. Find or propose an issue you want to work on. 
2. Prepare the issue before you start working on it. 
    - Make sure the description is clear. 
    - Tag yourself in Assignees section. 
3. If using Docker
  `On your Host machine`:
   1. git clone https://github.com/unskript/Awesome-CloudOps-Automation
   2. cd Awesome-CloudOps-Automation
   3. CONTAINER=`docker ps -l | grep awesome-runbooks | awk '{print $1}'`
   4. docker cp templates/runbooks/GCP.ipynb $CONTAINER:/home/jovyan/runbooks/<YOUR_RUNBOOK_NAME.ipynb>

  - Point your browser to `http://127.0.0.1:8888/lab/tree/<YOUR_RUNBOOK_NAME.ipynb>`
4. If using unSkript sandbox
    - Onboarding will drop you into runbook creation with sandbox credentials
    - Start building your lego from the proposed handle (GCP, k8s et al)
5. Create a branch
6. Copy over the template directory 
```
cp -r templates/legos your_connector/legos/your_lego_name e.g. cp -r templates/legos GCP/legos/gcp_filter_instance_by_label
```
7. You need to populate 4 files
    - lego.json : add the description, headline and function_name
    - lego.py : copy over the code you wrote inside the Jupyter interface into this file
    - README.md : some description about what the lego does
    - 1.png : a screenshot of the output of your code
7. Open a Pull Request and add a member of the core team as Reviewer (Jayasimha, Shloka, Amit, Abhishek)
9. Expect a feedback and merge in the next 48h-72h
10. Once merged, promote your work on LinkedIn, Twitter and other social media channels! (Optional, but people need to know you are awesome 😉)

An example run for the above can be seen in the [screencast](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/onboarding_hfest_2022.gif)

<img src="https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/onboarding_hfest_2022.gif">

##### Anatomy of a Runbook

You can read about the [Anatomy of a Runbook](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/Anatomy-of-Runbook.md)

##### Guideline to create Runbook

You can read the [Guideline for creating a Runbook](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/guidelines-to-creating-runbook.md)


## HacktoberFest 2022 Resource

The resource that are avilable for testing for our hacktoberfest is [here](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/hfest_2022_resource.md)

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
