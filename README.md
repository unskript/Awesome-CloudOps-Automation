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
| [MongoDB](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Mongo/README.md)         | [MongoDB Server Connectivity Runbook](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Mongo/MongoDB_Server_Connectivity.ipynb)                       | [Open in browser](http://127.0.0.1:8888/lab/tree/MongoDB\_Server\_Connectivity.ipynb)                |
| [K8S](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/README.md)        | [Pod Stuck in ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb)      | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S\_Pod\_Stuck\_In\_ImagePullBackOff\_State.ipynb) |
|                                                                                                        | [Pod Stuck in Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb)                | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S\_Pod\_Stuck\_In\_Terminating\_State.ipynb)      |
|                                                                                                        | [Pod Stuck in CrashLoopback State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb)            | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S\_Pod\_Stuck\_In\_CrashLoopBack\_State.ipynb)    |
|                                                                                                        | [Get Kube System Config Map](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/Get-Kube-System-Config-Map.ipynb)                            | [Open in browser](http://127.0.0.1:8888/lab/tree/get-kube-system-config-map.ipynb)                   |
|                                                                                                        | [Get K8S Candidate Nodes For a given config](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S-Get-Candidate-Nodes-Given-Config.ipynb)  | [Open in browser](http://127.0.0.1:8888/lab/tree/k8s-get-candidate-nodes-given-config.ipynb)         |
| [AWS](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/README.md)               | [Configure Url Endpoint on Cloudwatch Alarm](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb) |
|                                                                                                        | [Delete Unattached EBS Volumes](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Delete_Unattached_EBS_Volume.ipynb)                              | [Open in browser](http://127.0.0.1:8888/lab/tree/Delete\_Unattached\_EBS\_Volume.ipynb)              |
|                                                                                                        | [Detect ECS Failed Deployment](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Detect-ECS-failed-deployment.ipynb)                               | [Open in browser](http://127.0.0.1:8888/lab/tree/Detect-ECS-failed-deployment.ipynb)                 |
|                                                                                                        | [EC2 Disk Cleanup](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/EC2-Disk-Cleanup.ipynb)                                                       | [Open in browser](http://127.0.0.1:8888/lab/tree/ec2-disk-cleanup.ipynb)                             |
|                                                                                                        | [Get AWS ELB Unhealthy Instances](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Get-Aws-Elb-Unhealthy-Instances.ipynb)                         | [Open in browser](http://127.0.0.1:8888/lab/tree/get-aws-elb-unhealthy-instances.ipynb)              |
|                                                                                                        | [Resize EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize-EBS-Volume.ipynb)                                                     | [Open in browser](http://127.0.0.1:8888/lab/tree/resize-ebs-volume.ipynb)                            |
|                                                                                                        | [Resize List of PVCs](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize-List-Of-Pvcs.ipynb)                                                 | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize-List-Of-Pvcs.ipynb)                          |
|                                                                                                        | [Resize EKS PVC](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize_PVC.ipynb)                                                               | [Open in browser](http://127.0.0.1:8888/lab/tree/resize\_pvc.ipynb)                                  |
|                                                                                                        | [Restart AWS EC2 Instance](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart_AWS_EC2_Instances.ipynb)                                      | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart\_AWS\_EC2\_Instances.ipynb)                 |
|                                                                                                        | [Restart AWS EC2 Instance by Tag](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart-Aws-Instance-given-Tag.ipynb)                          | [Open in browser](http://127.0.0.1:8888/lab/tree/restart-aws-instance-given-tag.ipynb)               |
|                                                                                                        | [Restart UnHealthy Services Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart-Unhealthy-Services-Target-Group.ipynb)         | [Open in browser](http://127.0.0.1:8888/lab/tree/restart-unhealthy-services-target-group.ipynb)      |
|                                                                                                        | [Stop Untagged EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Stop_Untagged_EC2_Instances.ipynb)                                 | [Open in browser](http://127.0.0.1:8888/lab/tree/Stop\_Untagged\_EC2\_Instances.ipynb)               |
| [Jenkins](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Jenkins/README.md)       | [Fetch Jenkins Build Logs](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Jenkins/Fetch-Jenkins-Build-Logs.ipynb)                                   | [Open in browser](http://127.0.0.1:8888/lab/tree/fetch-jenkins-build-logs.ipynb)                     |
| [Postgresql](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Postgresql/README.md) | [Display Long-running Queries](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Postgresql/Display-postgresql-long-running.ipynb)                     | [Open in browser](http://127.0.0.1:8888/lab/tree/Display-postgresql-long-running.ipynb)              |

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
