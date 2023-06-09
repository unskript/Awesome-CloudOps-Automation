
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
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


def github_get_open_branches_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_get_open_branches(handle, owner: str, repository: str)-> List:
    """github_get_open_branches returns 100 open github branches for a user.

        :type handle: object
        :param handle: Object returned from task.validate(...).
    
        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: List of branches for a user for a repository
    """
    result = []
    try:
        user = handle.get_user(login=owner)
        repos = user.get_repos()
        repo_name = owner+"/"+repository
        if len(list(repos)) == 0:
            return [f"{owner} does not have any repositories"]
        for repo in repos:
            if repo.full_name == repo_name:
                branches = repo.get_branches()
                result = [branch.name for branch in branches[:100]]
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such pull number or repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
