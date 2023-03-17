##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from jira import JIRA, Issue
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    jql: str = Field(
        title="Jira issue search using Jira Query Language (JQL)",
        description="Search string to execute in JIRA. "
        "Valid JQL expression eg \"project = EN and status in (\"Selected for Development\") AND labels in (beta)\""
    )
    max_results: Optional[int] = Field(
        default=5,
        title="Limit number of matching issues",
        description="Max limit on number of matching issues"
    )


def legoPrinter(func):
    def Printer(*args, **kwargs):
        matching_issues = func(*args, **kwargs)
        print('\n')
        for issue in matching_issues:
            print('ID:{}: Summary:{} Description:{}'.format(
                issue.key, issue.fields.summary, issue.fields.description))

            for attachment in args[0].issue(issue.key).fields.attachment:
                print("\n Attachment Name: '{filename}', size: {size}".format(
                    filename=attachment.filename, size=attachment.size))
                print("\n")
        return matching_issues
    return Printer


@legoPrinter
def jira_search_issue(handle: JIRA, jql: str, max_results: int = 0) -> List:
    """jira_search_issue get Jira issues matching JQL queries.
        :type jql: str
        :param jql: Search string to execute in JIRA.

        :type max_results: int
        :param max_results: Max limit on number of matching issues

        :rtype: Jira issues matching JQL queries
    """
    matching_issues = handle.search_issues(jql, maxResults=max_results)
    return matching_issues
