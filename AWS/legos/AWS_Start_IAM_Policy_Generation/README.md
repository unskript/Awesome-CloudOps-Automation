[<img align="left" src="https://raw.githubusercontent.com/unskript/Awesome-CloudOps-Automation/master/.github/images/runbooksh_dark.png#gh-dark-mode-only" width="100" height="100" style="padding-right: 5px">](https://raw.githubusercontent.com/unskript/Awesome-CloudOps-Automation/master/.github/images/runbooksh_dark.png)
[<img align="left" src="https://raw.githubusercontent.com/unskript/Awesome-CloudOps-Automation/master/.github/images/runbooksh_light.png#gh-light-mode-only" width="100" height="100" style="padding-right: 5px">](https://raw.githubusercontent.com/unskript/Awesome-CloudOps-Automation/master/.github/images/runbooksh_light.png)


# AWS Start IAM Policy Generation


## Description
Given a region, a CloudTrail ARN (where the logs are being recorded), a reference IAM ARN (whose usage we will parse), and a Service role, this will begin the generation of a IAM policy.  The output is a String of the generation Id.

## Action Details
```python
action.start_iam_policy_generation(handle, region:str, CloudTrailARN:str, IAMPrincipalARN:str, AccessRole:str, hours:float) -> str
```
- `handle`: Object of type unSkript AWS Connector.
- `region`: AWS region where CloudTrail logs are recorded.
- `CloudTrailARN`: ARN of the logs you wish to parse.
- `IAMPrincipalARN`: Reference ARN - we are copying the usage from this account.
- `AccessRole`: Role that allows access to logs.
- `hours`: Hours of data to parse.

## Action Output
This action will return a string value representing the generation Id.
<img src="./1.jpg">

## See it in Action


You can try out this action on the [runbooks.sh](http://runbooks.sh) open-source platform or on the [unSkript Cloud Free Trial](https://us.app.unskript.io). 

Feel free to join the community Slack at [https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) for support, questions, and comments