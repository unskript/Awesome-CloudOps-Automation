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
        title='JIRA Issue ID',
        description='Issue ID. Eg EN-1234'
    )


def legoPrinter(func):
    def Printer(*args, **kwargs):
        description, labels, attachment = func(*args, **kwargs)
        print('\n')
        pp.pprint(description)
        pp.pprint(labels)
        pp.pprint(attachment)
        return
    return Printer


@legoPrinter
def jira_get_issue(hdl: JIRA, issue_id: str) -> str:
    """jira_get_issue Get Jira Issue Info

        :type issue_id: str
        :param issue_id: Issue ID.

        :rtype: Jira Issue Info
    """
    # Input param validation.
    issue = hdl.issue(issue_id)
    return issue.fields.description, issue.fields.labels, issue.fields.attachment
