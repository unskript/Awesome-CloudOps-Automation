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


def github_list_pull_requests_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_list_pull_requests(handle, owner:str, repository:str) -> List:
    """github_list_pull_requests returns all pull requests for a user

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: List of pull requests for a user
    """
    result = []
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        #Fetch open PRs and sort by created
        prs = repo.get_pulls(state='open', sort='created')
        for pr in prs:
            prs_dict = {}
            prs_dict[pr.number] = pr.title
            result.append(prs_dict)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such repository or user found")
        raise e.data
    except Exception as e:
        raise e
    return result


