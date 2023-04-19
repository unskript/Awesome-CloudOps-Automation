
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException



class InputSchema(BaseModel):
    owner: str = Field(
        ..., description='Username of the GitHub user. Eg: "johnwick"', title='Owner'
    )
    repository: str = Field(
        ...,
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )


def github_list_open_issues_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_list_open_issues(handle, owner:str, repository:str) -> List:
    """github_list_open_issues returns details of open issues

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: List of open issues
    """
    result = []
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login +'/'+ repository
        repo = handle.get_repo(repo_name)
        issues = repo.get_issues()
        for issue in issues:
            if issue.state == 'open':
                issue_details = {}
                issue_details["title"] = issue.title
                issue_details["issue_number"] = issue.number
                if type(issue.assignee)=='NoneType':
                    issue_details["assignee"] = issue.assignee.login
                else:
                    issue_details["assignee"] = issue.assignee
                result.append(issue_details)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such repository or user found")
        raise e.data
    except Exception as e:
        raise e
    return result

