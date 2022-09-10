[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]


<br />
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

## Runbooks
| Category                                                                                               | Directory                                                                                              | Runbooks                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MongoDB        | [/mongo](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Mongo/README.md)        | [MongoDB Server Connectivity Runbook](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Mongo/MongoDB_Server_Connectivity.ipynb)                       |
| K8S     |                                                                                                        | [Pod Stuck in ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb)      |
|                                                                                                        |                                                                                                        | [Pod Stuck in Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb)                |
|                                                                                                        |                                                                                                        | [Pod Stuck in CrashLoopback State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb)            |
|                                                                                                        |                                                                                                        | [Get Kube System Config Map](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/Get-Kube-System-Config-Map.ipynb)                            |
|                                                                                                        |                                                                                                        | [Get K8S Candidate Nodes For a given config](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S-Get-Candidate-Nodes-Given-Config.ipynb)  |
| AWS               | [/aws](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/README.md)            | [Configure Url Endpoint on Cloudwatch Alarm](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb) |
|                                                                                                        |                                                                                                        | [Delete Unattached EBS Volumes](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Delete_Unattached_EBS_Volume.ipynb)                              |
|                                                                                                        |                                                                                                        | [Detect ECS Failed Deployment](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Detect-ECS-failed-deployment.ipynb)                               |
|                                                                                                        |                                                                                                        | [EC2 Disk Cleanup](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/EC2-Disk-Cleanup.ipynb)                                                       |
|                                                                                                        |                                                                                                        | [Get AWS ELB Unhealthy Instances](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Get-Aws-Elb-Unhealthy-Instances.ipynb)                         |
|                                                                                                        |                                                                                                        | [Resize EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize-EBS-Volume.ipynb)                                                     |
|                                                                                                        |                                                                                                        | [Resize List of PVCs](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize-List-Of-Pvcs.ipynb)                                                 |
|                                                                                                        |                                                                                                        | [Resize EKS PVC](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize_PVC.ipynb)                                                               |
|                                                                                                        |                                                                                                        | [Restart AWS EC2 Instance](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart_AWS_EC2_Instances.ipynb)                                      |
|                                                                                                        |                                                                                                        | [Restart AWS EC2 Instance by Tag](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart-Aws-Instance-given-Tag.ipynb)                          |
|                                                                                                        |                                                                                                        | [Restart UnHealthy Services Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart-Unhealthy-Services-Target-Group.ipynb)         |
|                                                                                                        |                                                                                                        | [Stop Untagged EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Stop_Untagged_EC2_Instances.ipynb)                                 |
| Jenkins     | [/jenkins](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/jenkins/README.md)    | [Fetch Jenkins Build Logs](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Jenkins/Fetch-Jenkins-Build-Logs.ipynb)                                   |
| Postgresql | [/postgresql](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/postgresql/README.md) | [Display Long running Queries](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Postgresql/Display-postgresql-long-running.ipynb)                     |
|                                                                                                                                                                                                               
## Quick start

### Get started with docker
#### Linux/Mac/Windows (x86)

```s
docker run -it -p 8888:8888 \
     -v $HOME/.unskript:/data \
     -e NB_USER=jovyan \
     -e CHOWN_HOME=yes \
     -e CHOWN_EXTRA_OPTS='-R' \
     --user root \
     -w /home/jovyan \ 
     public.ecr.aws/unskript/awesome-runbooks:latest
```

#### Linux/Mac/Windows (arm64)
```s
docker run -it -p 8888:8888 \
    -v $HOME/.unskript:/data  \
    -e NB_USER=jovyan \
    -e CHOWN_HOME=yes \
    -e CHOWN_EXTRA_OPTS='-R' \
    --user root \
    -w /home/jovyan \
   public.ecr.aws/unskript/awesome-runbooks:v0.6.0-arm64
```

> Inside the docker there is `/data` folder that is where we store the `credentials` and `runbooks`. So if you would like to retain the `connectors` and `runbooks` you can use the docker's `-v` option to retain the changes done on the `docker`.

> Note: New files are created inside the docker and will persist unless --rm option is given (which we have not suggested) i.e. `Save-As` function can be used, but user has to remember the file name and insert in the URL

### Open the Runbook
Once you run the above command, here's the table which will help you find the URL for runbook of your choice. 

| Category                                                                                               | Runbooks                                                                                                                                                                 | URL                                                                                                    |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| [MongoDB](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Mongo/README.md)         | [MongoDB Server Connectivity Runbook](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Mongo/MongoDB_Server_Connectivity.ipynb)                       | [Open in browser](http://127.0.0.1:8888/lab/tree/MongoDB\_Server\_Connectivity.ipynb)                |
| [K8S](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/README.md)        | [Pod Stuck in ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb)      | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S\_Pod\_Stuck\_In\_ImagePullBackOff\_State.ipynb) |
|                                                                                                        | [Pod Stuck in Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb)                | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S\_Pod\_Stuck\_In\_Terminating\_State.ipynb)      |
|                                                                                                        | [Pod Stuck in CrashLoopback State](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb)            | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S\_Pod\_Stuck\_In\_CrashLoopBack\_State.ipynb)    |
|                                                                                                        | [Get Kube System Config Map](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/Get-Kube-System-Config-Map.ipynb)                            | [Open in browser](http://127.0.0.1:8888/lab/tree/Get-Kube-System-Config-Map.ipynb)                   |
|                                                                                                        | [Get K8S Candidate Nodes For a given config](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Kubernetes/K8S-Get-Candidate-Nodes-Given-Config.ipynb)  | [Open in browser](http://127.0.0.1:8888/lab/tree/K8S-Get-Candidate-Nodes-Given-Config.ipynb)         |
| [AWS](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/README.md)               | [Configure Url Endpoint on Cloudwatch Alarm](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb) | [Open in browser](http://127.0.0.1:8888/lab/tree/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb) |
|                                                                                                        | [Delete Unattached EBS Volumes](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Delete_Unattached_EBS_Volume.ipynb)                              | [Open in browser](http://127.0.0.1:8888/lab/tree/Delete\_Unattached\_EBS\_Volume.ipynb)              |
|                                                                                                        | [Detect ECS Failed Deployment](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Detect-ECS-failed-deployment.ipynb)                               | [Open in browser](http://127.0.0.1:8888/lab/tree/Detect-ECS-failed-deployment.ipynb)                 |
|                                                                                                        | [EC2 Disk Cleanup](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/EC2-Disk-Cleanup.ipynb)                                                       | [Open in browser](http://127.0.0.1:8888/lab/tree/EC2-Disk-Cleanup.ipynb)                             |
|                                                                                                        | [Get AWS ELB Unhealthy Instances](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Get-Aws-Elb-Unhealthy-Instances.ipynb)                         | [Open in browser](http://127.0.0.1:8888/lab/tree/Get-Aws-Elb-Unhealthy-Instances.ipynb)              |
|                                                                                                        | [Resize EBS Volume](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize-EBS-Volume.ipynb)                                                     | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize-EBS-Volume.ipynb)                            |
|                                                                                                        | [Resize List of PVCs](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize-List-Of-Pvcs.ipynb)                                                 | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize-List-Of-Pvcs.ipynb)                          |
|                                                                                                        | [Resize EKS PVC](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Resize_PVC.ipynb)                                                               | [Open in browser](http://127.0.0.1:8888/lab/tree/Resize\_PVC.ipynb)                                  |
|                                                                                                        | [Restart AWS EC2 Instance](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart_AWS_EC2_Instances.ipynb)                                      | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart\_AWS\_EC2\_Instances.ipynb)                 |
|                                                                                                        | [Restart AWS EC2 Instance by Tag](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart-Aws-Instance-given-Tag.ipynb)                          | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart-Aws-Instance-given-Tag.ipynb)               |
|                                                                                                        | [Restart UnHealthy Services Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Restart-Unhealthy-Services-Target-Group.ipynb)         | [Open in browser](http://127.0.0.1:8888/lab/tree/Restart-Unhealthy-Services-Target-Group.ipynb)      |
|                                                                                                        | [Stop Untagged EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/AWS/Stop_Untagged_EC2_Instances.ipynb)                                 | [Open in browser](http://127.0.0.1:8888/lab/tree/Stop\_Untagged\_EC2\_Instances.ipynb)               |
| [Jenkins](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Jenkins/README.md)       | [Fetch Jenkins Build Logs](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Jenkins/Fetch-Jenkins-Build-Logs.ipynb)                                   | [Open in browser](http://127.0.0.1:8888/lab/tree/Fetch-Jenkins-Build-Logs.ipynb)                     |
| [Postgresql](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Postgresql/README.md) | [Display Long running Queries](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/Postgresql/Display-postgresql-long-running.ipynb)                     | [Open in browser](http://127.0.0.1:8888/lab/tree/Display-postgresql-long-running.ipynb)              |


## Community
[Join the CloudOps Community Workspace](https://join.slack.com/t/cloud-ops-community/shared_invite/zt-1fvuobp10-~r_KyK9BxPhGiebOvl3h_w) on Slack to connect with other users, contributors and awesome people behind awesome CloudOps automation project. 

## Roadmap

See the [open issues](https://github.com/unskript/awesome-cloudops-automation/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**. Check out our [Contribution Guidelines](https://github.com/unskript/awesome-cloudops-automation/blob/main/.github/CONTRIBUTING.md) for more details. 

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
