##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException
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


def github_delete_branch_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_delete_branch(handle, owner:str, repository: str, branch_name: str)-> List:
    """github_delete_branch returns details of the deleted branch.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type branch_name: string
        :param branch_name: Branch Name Eg: "dummy-branch"

        :rtype: Deleted branch info
    """
    result = []
    try:
        user = handle.get_user(login=owner)
        repo_name = user.login+"/"+repository
        repo = handle.get_repo(repo_name)
        if repo.full_name == repo_name:
            branch = repo.get_branch(branch_name)
            flag_to_check_branch = 0
            if branch.name == branch_name:
                flag_to_check_branch = 1
                ref = repo.get_git_ref(f"heads/{branch_name}")
                ref.delete()
                result.append(f"{branch_name} successfully deleted")
        if flag_to_check_branch == 0:
            return [f"{branch_name} not found"]
    except GithubException as e:
        if e.status== 403:
            return [f"You need push access"]
        if e.status==404:
            return [f"No such username or repository"]
        else:
            return [e.data]
    return result

