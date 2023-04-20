# RunBook Connectors:
 | | | 
 | ---| ---| 
 | [AWS](xRunBook_List.md#AWS) | [ElasticSearch](xRunBook_List.md#ElasticSearch) | [Jenkins](xRunBook_List.md#Jenkins) |
 | [Jira](xRunBook_List.md#Jira) | [Kubernetes](xRunBook_List.md#Kubernetes) | [Postgresql](xRunBook_List.md#Postgresql) |
 | 

 
# RunBook Categories:
 | | | 
 | ---| ---| 
 | [IAM](runbook_IAM.md) | [SECOPS](runbook_SECOPS.md) | [COST_OPT](runbook_COST_OPT.md) |
 | [DEVOPS](runbook_DEVOPS.md) | [SRE](runbook_SRE.md) | [CLOUDOPS](runbook_CLOUDOPS.md) |
 | [TROUBLESHOOTING](runbook_TROUBLESHOOTING.md) | [ES](runbook_ES.md) | 
 
# Runbooks in IAM
* AWS [AWS Access Key Rotation for IAM users](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Access_Key_Rotation.ipynb): This runbook can be used to configure AWS Access Key rotation. Changing access keys (which consist of an access key ID and a secret access key) on a regular schedule is a well-known security best practice because it shortens the period an access key is active and therefore reduces the business impact if they are compromised. Having an established process that is run regularly also ensures the operational steps around key rotation are verified, so changing a key is never a scary step.
* AWS [AWS Add Mandatory tags to EC2](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Add_Mandatory_tags_to_EC2.ipynb): This xRunBook is a set of example actions that could be used to establish mandatory tagging to EC2 instances.  First testing inatnces for compliance, and creating reports of instances that are missing the required tags. There is also and action to add tags to an instance - to help bring them into tag compliance.
* AWS [Create a new AWS IAM User](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Add_new_IAM_user.ipynb): AWS has an inbuilt identity and access management system known as AWS IAM. IAM supports the concept of users, group, roles and privileges. IAM user is an identity that can be created and assigned some privileges. This runbook can be used to create an AWS IAM User
* AWS [Update and Manage AWS User permission](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Update_and_Manage_AWS_User_Permission.ipynb): This runbook can be used Update and Manage AWS IAM User Permission
