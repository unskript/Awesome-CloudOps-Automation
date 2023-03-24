##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from jira.client import JIRA
from pydantic import BaseModel, Field
from typing import Optional
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    issue_id: str = Field(
        title="Issue ID",
        description="Issue ID"
    )
    status: str = Field(
        title="New Status",
        description="New Status for the JIRA issue"
    )
    transition: Optional[str] = Field(
        title="Transition ID",
        description="Transition to use for status change for the JIRA issue"
    )


def jira_issue_change_status_printer(output):
    if output is None:
        return
    pp.pprint(output)


def jira_issue_change_status(hdl: JIRA, issue_id: str, status: str, transition: str = ""):
    """jira_get_issue_status gets the status of a given Jira issue.
        :type issue_id: str
        :param issue_id: ID of the issue whose status we want to fetch (eg ENG-14)

        :type status: str
        :param status: New Status for the JIRA issue

        :type transition: str
        :param transition: Transition to use for status change for the JIRA issue
        :rtype: String with issue status fetched from JIRA API
    """

    # Input param validation.
    issue = hdl.issue(issue_id)
    if transition:
        transitions = hdl.transitions(issue)
        t = [t for t in transitions if t.get('name') == status]
        if len(t) > 1:
            print("Multiple transitions possible for JIRA issue. Please select transition number to use", [
                t.get('id') for t in transitions if t.get('name') == status])
            return
        else:
            transition = t[0].get('id')

    hdl.transition_issue(issue, transition)
    return
