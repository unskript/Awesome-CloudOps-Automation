##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException
import pprint


class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"', 
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )
    pull_request_number: int = Field(
        description='Pull request number. Eg: 167', 
        title='Pull Request Number'
    )



def github_close_pull_request_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_close_pull_request(handle, owner:str, repository:str, pull_request_number: int) -> str:
    """github_close_pull_request returns time at which the pull request was closed

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type pull_request_number: int
        :param pull_request_number: Pull request number. Eg: 167 

        :rtype: String of details of pull request closure
    """
    result = []
    pr_number = int(pull_request_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        try:
            if pr.state == "open":
                result = pr.edit(state='closed')
            else:
                return f"PR number {pr.number} is already closed"
            if result is None:
                return f"PR {pr.number} was closed at: {pr.closed_at} "
        except GithubException as e:
            if e.status == 404:
                raise Exception("You need admin access of an organization in case the repository is a part of an organization")
            raise e.data
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such pull number or repository or user found")
        raise e.data
    except Exception as e:
        raise e
    return result


