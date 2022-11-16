##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from jira.client import JIRA
from pydantic import BaseModel, Field
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    issue_id: str = Field(
        title="Issue ID",
        description="JIRA issue ID to assign. Eg ENG-42"
    )
    user_id: str = Field(
        title="User ID",
        description="User to assign the issue to. Eg user@acme.com"
    )


def legoPrinter(func):
    def Printer(*args, **kwargs):
        output = func(*args, **kwargs)
        print('\n')
        pp.pprint(output)
        return output
    return Printer


@legoPrinter
def jira_assign_issue(hdl: JIRA, issue_id: str, user_id: str) -> str:
    """jira_assign_issue assigns a given Jira issue to a user
    
        :type issue_id: str
        :param issue_id: JIRA issue ID to assign. Eg ENG-42

        :type user_id: str
        :param user_id: User to assign the issue to. Eg user@acme.com

        :rtype: str
    """

    # Input param validation.
    issue = hdl.issue(issue_id)
    hdl.assign_issue(issue, user_id)
    return issue.fields.assignee
