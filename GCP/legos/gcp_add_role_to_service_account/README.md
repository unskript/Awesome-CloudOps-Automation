[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>GCP Add Role to Service Account</h1>

## Description
This Lego add role and member to the service account in GCP.

## Lego Details

    gcp_add_role_to_service_account(handle: object, project_id: str, role: str, member_email:str, sa_id:str)

        handle: Object of type unSkript GCP Connector
        project_id: Name of the project
        role: Role name from which member needs to remove e.g iam.serviceAccountUser
        member_email: Member email which has GCP access e.g test@company.com
        sa_id: Service Account email

## Lego Input
project_id: Name of the project. eg- "unskript-test2"
role: Role name from which member needs to remove e.g iam.serviceAccountUser
member_email: Member email which has GCP access e.g test@company.com
sa_id: Service Account email

## Lego Output
Here is a sample output.

<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)