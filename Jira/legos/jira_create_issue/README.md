[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Create a Jira Issue</h2>

<br>

## Description
This Lego Create a Jira Issue.


## Lego Details

    jira_create_issue(handle: object, project_name: str, summary: str, issue_type: IssueType, description: str, fields: dict)

        handle: Object of type unSkript jira Connector
        project_name: The name of the project for which the issue will be generated
        summary: Summary of the issue
        description: Description of the issue
        issue_type: JIRA Issue Type. Possible values: Bug|Task|Story|Epic
        fields: User needs to pass the fields in the format of dict(KEY=VALUE) pair

## Lego Input
This Lego take six input handle, project_name, summary, issue_type, description and fields.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)