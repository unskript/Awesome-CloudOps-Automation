##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from github import GithubException
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import pprint


class InputSchema(BaseModel):
    branch_name: str = Field(
        description='Branch name. Eg:"dummy-branch-name"', 
        title='Branch Name'
    )
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )



def github_get_branch_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_get_branch(handle, owner:str, repository: str, branch_name: str) -> Dict:
    """github_get_branch returns details of commits (if any) of a branche for a user.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type branch_name: string
        :param branch_name: Branch Name Eg: "dummy-branch"

        :rtype: Dict of branch with commits for a user for a repository
    """
    branch_info = {}
    try:
        user = handle.get_user(login=owner)
        repo_name = user.login+"/"+repository
        repo = handle.get_repo(repo_name)
        if repo.full_name == repo_name:
            branch = repo.get_branch(branch_name)
            if branch.name == branch_name:
                branch_info["branch"] = branch.name
                branch_info["commit"] = branch.commit.sha
            else:
                return [f"{branch_name} not found"]
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such repository or user found")
        raise e.data
    except Exception as e:
        raise e
    return result

