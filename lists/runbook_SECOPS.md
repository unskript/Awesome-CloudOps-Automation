# RunBook Connectors:
 | | | 
 | ---| ---| 
 | [AWS](xRunBook_List.md#AWS) | [ElasticSearch](xRunBook_List.md#ElasticSearch) | [Jenkins](xRunBook_List.md#Jenkins) |
 | [Kubernetes](xRunBook_List.md#Kubernetes) | [Postgresql](xRunBook_List.md#Postgresql) | 

 
# RunBook Categories:
 | | | 
 | ---| ---| 
 | [IAM](runbook_IAM.md) | [SECOPS](runbook_SECOPS.md) | [CLOUDOPS](runbook_CLOUDOPS.md) |
 | [DEVOPS](runbook_DEVOPS.md) | [SRE](runbook_SRE.md) | [COST_OPT](runbook_COST_OPT.md) |
 | [TROUBLESHOOTING](runbook_TROUBLESHOOTING.md) | [ES](runbook_ES.md) | 

 # Runbooks in SECOPS
* AWS [AWS Access Key Rotation for IAM users](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/AWS_Access_Key_Rotation.ipynb): This runbook can be used to configure AWS Access Key rotation. Changing access keys (which consist of an access key ID and a secret access key) on a regular schedule is a well-known security best practice because it shortens the period an access key is active and therefore reduces the business impact if they are compromised. Having an established process that is run regularly also ensures the operational steps around key rotation are verified, so changing a key is never a scary step.
* AWS [Create a new AWS IAM User](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Add_new_IAM_user.ipynb): AWS has an inbuilt identity and access management system known as AWS IAM. IAM supports the concept of users, group, roles and privileges. IAM user is an identity that can be created and assigned some privileges. This runbook can be used to create an AWS IAM User
* AWS [Enforce HTTP Redirection across all AWS ALB instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Enforce_HTTP_Redirection_across_AWS_ALB.ipynb): This runbook can be used to enforce HTTP redirection across all AWS ALBs. Web encryption protocols like SSL and TLS have been around for nearly three decades. By securing web data in transit, these security measures ensure that third parties can’t simply intercept unencrypted data and cause harm. HTTPS uses the underlying SSL/TLS technology and is the standard way to communicate web data in an encrypted and authenticated manner instead of using insecure HTTP protocol. In this runbook, we implement the industry best practice of redirecting all unencrypted HTTP data to the secure HTTPS protocol.
* AWS [Publicly Accessible Amazon RDS Instances](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Publicly_Accessible_Amazon_RDS_Instances.ipynb): This runbook can be used to find the publicly accessible RDS instances for the given AWS region.
* AWS [Remediate unencrypted S3 buckets](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Remediate_unencrypted_S3_buckets.ipynb): This runbook can be used to filter all the S3 buckets which are unencrypted and apply encryption on unencrypted S3 buckets.
* AWS [Renew AWS SSL Certificates that are close to expiration](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Renew_SSL_Certificate.ipynb): This runbook can be used to list all AWS SSL (ACM) Certificates that need to be renewed within a given threshold number of days. Optionally it can renew the certificate using AWS ACM service.
* AWS [Restrict S3 Buckets with READ/WRITE Permissions to all Authenticated Users](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Restrict_S3_Buckets_with_READ_WRITE_Permissions.ipynb): This runbook will list all the S3 buckets.Filter buckets which has ACL public READ/WRITE permissions and Change the ACL Public READ/WRITE permissions to private in the given region.
* AWS [Secure Publicly accessible Amazon RDS Snapshot](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/AWS/Secure_Publicly_accessible_Amazon_RDS_Snapshot.ipynb): This lego can be used to list all the manual database snapshots in the given region. Get publicly accessible DB snapshots in RDS and Modify the publicly accessible DB snapshots in RDS to private.
