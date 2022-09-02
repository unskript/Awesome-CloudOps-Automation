##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from jira.client import JIRA
from pydantic import BaseModel, Field
from typing import Optional
import pprint

pp = pprint.PrettyPrinter(indent=4)

from beartype import beartype

def jira_issue_change_status_Printer(func):
    def Printer(*args, **kwargs):
        output = func(*args, **kwargs)
        print('\n')
        return output
    return Printer


@beartype
def jira_issue_change_status(hdl: JIRA, issue_id: str, status: str, transition: str = ""):
    """jira_get_issue_status gets the status of a given Jira issue.
        :type issue_id: str
        :param issue_id: ID of the issue whose status we want to fetch (eg ENG-14)
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


def unskript_default_printer(output):
    if isinstance(output, (list, tuple)):
        for item in output:
            print(f'item: {item}')
    elif isinstance(output, dict):
        for item in output.items():
            print(f'item: {item}')
    else:
        print(f'Output for {task.name}')
        print(output)