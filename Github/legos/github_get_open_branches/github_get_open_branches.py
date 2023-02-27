
##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List
import pprint
from github import GithubException


class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"', 
        title='owner'
    )
    repository: str = Field(
        description='Full name of the GitHub repository. Eg: "unskript/Awesome-CloudOps-Automation"',
        title='repository',
    )


def github_get_open_branches_printer(output):
    if not output:
        return
    pprint.pprint(output)


def github_get_open_branches(handle, owner: str, repository: str)-> List:
    """github_get_all_branches returns 100 open github branches for a user.

        :type handle: object
        :param handle: Object returned from task.validate(...).
    
        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Full name of the GitHub repository. Eg: "unskript/Awesome-CloudOps-Automation"

        :rtype: List of branches for a user for a repository
    """
    result = []
    try:
        user = handle.get_user(login=owner)
        repos = user.get_repos()
        if len(list(repos)) == 0:
            return [f"{owner} does not have any repositories"]
        for repo in repos:
            if repo.full_name == repository:
                branches = repo.get_branches()
                [result.append(branch.name) for branch in branches[:100]]
    except GithubException as e:
        if e.status == 403:
            return [f"You need push access"]
        elif e.status == 404:
            return [f"No such username or repository"]
        else:
            return [e.data]
    return result



