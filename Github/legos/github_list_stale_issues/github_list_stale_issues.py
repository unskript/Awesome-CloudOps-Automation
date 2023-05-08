
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
from typing import Tuple
import datetime
from pydantic import BaseModel, Field
from github import GithubException

class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )
    age_to_stale: str = Field(
        description=('Age in days to check if the issue creation or updation dates are '
                     'older and hence classify those issues as stale Eg:45'),
        title='Age to Stale',
    )


def github_list_stale_issues_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_list_stale_issues(handle, owner:str, repository:str, age_to_stale:int) -> Tuple:
    """github_list_stale_issues returns details of stale issues

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type age_to_stale: int
        :param age_to_stale: Age in days to check if the issue creation or updation dates 
        are older and hence classify those issues as stale Eg:45',

        :rtype: List of stale issues
    """
    result = []
    age = int(age_to_stale)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login +'/'+ repository
        repo = handle.get_repo(repo_name)
        issues = repo.get_issues()
        for issue in issues:
            creation_date = issue.created_at
            updation_date = issue.updated_at
            today = datetime.datetime.now()
            diff_in_updation = (today - updation_date).days
            diff_in_creation = (today - creation_date).days
            if diff_in_creation >= age or diff_in_updation >= age:
                issue_details = {}
                issue_details["title"] = issue.title
                issue_details["issue_number"] = issue.number
                if isinstance(issue.assignee, type(None)):
                    issue_details["assignee"] = issue.assignee.login
                else:
                    issue_details["assignee"] = issue.assignee
                result.append(issue_details)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such pull number or repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    if len(result) != 0:
        return (False, result)
    return (True, None)
