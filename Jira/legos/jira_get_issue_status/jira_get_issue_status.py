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
        title='Issue ID',
        description='Issue ID'
    )


def jira_get_issue_status_printer(output):
    if output is None:
        return
    pp.pprint(output)


def jira_get_issue_status(hdl: JIRA, issue_id: str):
    """jira_get_issue_status get issue status

        :type issue_id: str
        :param issue_id: Issue ID.

        :rtype:
    """
    # Input param validation.
    issue = hdl.issue(issue_id)
    return issue.fields.status.name
