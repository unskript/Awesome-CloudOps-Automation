##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from jira import JIRA, Issue
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import pprint
from tabulate import tabulate

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    jql: str = Field(
        title="Jira issue search using Jira Query Language (JQL)",
        description="Search string to execute in JIRA. "
        "Valid JQL expression eg \"project = EN and status in (\"Selected for Development\") AND labels in (beta)\""
    )
    max_results: Optional[int] = Field(
        default=50,
        title="Limit number of matching issues",
        description="Max limit on number of matching issues"
    )


def jira_search_issue_printer(output):
    if output is None:
        return
    print_data = []
    for issue in output:
        print_data.append([issue.get("ID"), issue.get("Summary")])
    print(tabulate(print_data, headers=["Issue ID", "Summary"], tablefmt="grid"))

def jira_search_issue(handle: JIRA, jql: str, max_results: int = 50) -> List:
    """jira_search_issue get Jira issues matching JQL queries.
        :type jql: str
        :param jql: Search string to execute in JIRA.

        :type max_results: int
        :param max_results: Max limit on number of matching issues

        :rtype: Jira issues matching JQL queries
    """
    result = []
    total_done = 0
    while True:
        matching_issues = handle.search_issues(jql, startAt=total_done, maxResults=max_results)
        for i in matching_issues:
            result.append({"ID": i.key, "Summary":i.fields.summary})
        total_done += max_results
        if total_done > matching_issues.total:
            break
    return result
