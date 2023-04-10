# RunBook Connectors:
 | | | | | | 
 | ---| ---| ---| ---| ---| 
 | [AWS](xRunBook_List.md#AWS) | [ElasticSearch](xRunBook_List.md#ElasticSearch) | [Jenkins](xRunBook_List.md#Jenkins) | [Kubernetes](xRunBook_List.md#Kubernetes) | [Postgresql](xRunBook_List.md#Postgresql) | 

 
# RunBook Categories:
 | | | | | | | | | 
 | ---| ---| ---| ---| ---| ---| ---| ---| 
 | [IAM](runbook_IAM.md) | [SECOPS](runbook_SECOPS.md) | [CLOUDOPS](runbook_CLOUDOPS.md) | [DEVOPS](runbook_DEVOPS.md) | [SRE](runbook_SRE.md) | [COST_OPT](runbook_COST_OPT.md) | [TROUBLESHOOTING](runbook_TROUBLESHOOTING.md) | [ES](runbook_ES.md) | 

 # Runbooks in TROUBLESHOOTING
* AWS [Restart AWS EC2 Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_AWS_EC2_Instances_By_Tag.ipynb): This runbook can be used to Restart AWS EC2 Instances
* AWS [Restart AWS Instances with a given tag](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_Aws_Instance_given_Tag.ipynb): This runbook will discover all AWS EC2 instances matching a tag and then restart them. It will notify status through slack after its done. There is also a dry run mode that will just display the instances that match the query.
* AWS [Restart unhealthy services in a Target Group](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restart_Unhealthy_Services_Target_Group.ipynb): This runbook restarts unhealthy services in a target group. The restart command is provided via a tag attached to the instance.
* AWS [Troubleshooting Your EC2 Configuration in a Private Subnet](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Troubleshooting_Your_EC2_Configuration_in_Private_Subnet.ipynb): This runbook can be used to troubleshoot EC2 instance configuration in a private subnet by capturing the VPC ID for a given instance ID. Using VPC ID to get Internet Gateway details then try to SSH and connect to internet.
* Kubernetes [Kubernetes Log Healthcheck](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Log_Healthcheck.ipynb): This RunBook checks the logs of every pod in a namespace for warning messages.
* Kubernetes [Rollback Kubernetes Deployment](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Rollback_k8s_Deployment_and_Update_Jira.ipynb): This runbook can be used to rollback Kubernetes Deployment
