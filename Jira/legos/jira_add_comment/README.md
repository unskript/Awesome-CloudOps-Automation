[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Get Jira Add Comment</h2>

<br>

## Description
This Lego adds a comment to a Jira Issue.


## Lego Details

    jira_add_comment(handle: JIRA, issue_id: str, comment: str, visibility: Dict[str, str] = None)

        handle: Object of type unSkript jira Connector
        issue_id: Issue ID.
        comment: Comment to add in Jira Issue.
        visibility: a dict containing two entries: "type" and "value".
              "type" is 'role' (or 'group' if the Jira server has configured comment visibility for groups)
              "value" is the name of the role (or group) to which viewing of this comment will be restricted.
        is_internal: True marks the comment as 'Internal' in Jira Service Desk (Default: ``False``)

## Lego Input
This Lego take 4 input handle, issue_id, comment, visibility.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)