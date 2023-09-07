##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
import datetime
from pydantic import BaseModel, Field
from tabulate import tabulate
from github import GithubException, BadCredentialsException, UnknownObjectException

class InputSchema(BaseModel):
    owner: Optional[str] = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )
    age_to_stale: Optional[int] = Field(
        '14',
        description=('Age in days to check if the issue creation or updation dates are '
                     'older and hence classify those issues as stale Eg:45'),
        title='Age to Stale',
    )


def github_list_stale_issues_printer(output):
    if output is None or output[1] is None:
        return

    success, res = output
    if not success:
        headers = ["Title", "Issue Number", "Assignee"]
        table = [[issue["title"], issue["issue_number"], issue["assignee"]] for issue in res]
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("No stale issues found.")


def github_list_stale_issues(handle, repository:str, age_to_stale:int=14) -> Tuple:
    """github_list_stale_issues returns details of stale issues

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type owner: string (Optional)
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type age_to_stale: int (Optional)
        :param age_to_stale: Age in days to check if the issue creation or updation dates 
        are older and hence classify those issues as stale Eg:45',

        :rtype: List of stale issues
    """
    result = []
    try:
        owner = handle.get_user().login  # Fetch the owner (authenticated user) login
        repo = handle.get_repo(f"{owner}/{repository}")
        issues = repo.get_issues()

        # Check if there are no open issues
        if issues.get_page(0) == []:
            print("No issues are open at the moment.")
            return (True, None)

        today = datetime.datetime.now()
        for issue in issues:
            creation_date = issue.created_at
            updation_date = issue.updated_at
            diff_in_updation = (today - updation_date).days
            diff_in_creation = (today - creation_date).days
            if diff_in_creation >= age_to_stale or diff_in_updation >= age_to_stale:
                issue_details = {
                    "title": issue.title,
                    "issue_number": issue.number,
                    "assignee": "None" if issue.assignee is None else issue.assignee.login
                }
                result.append(issue_details)
    except Exception as e:
        raise e

    return (False, result) if result else (True, None)