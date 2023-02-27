##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from github import GithubException
from typing import Optional, List
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
        description='Full name of the GitHub repository. Eg: "unskript/Awesome-CloudOps-Automation"',
        title='Repository',
    )



def github_get_branch_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_get_branch(handle, owner:str, repository: str, branch_name: str) -> List:
    """github_get_branch returns details of commits (if any) of a branche for a user.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Full name of the GitHub repository. Eg: "unskript/Awesome-CloudOps-Automation"

        :type branch_name: string
        :param branch_name: Branch Name Eg: "dummy-branch"

        :rtype: List of branch with commits for a user for a repository
    """
    result = []
    try:
        user = handle.get_user(login=owner)
        repos = user.get_repos()
        for repo in repos:
            if repo.full_name ==repository:
                branches = repo.get_branches()
                flag_to_check_branch = 0
                for branch in branches:
                    if branch.name==branch_name:
                        flag_to_check_branch = 1
                        branch_info={}
                        branch_info["branch"] = branch.name
                        branch_info["commit"] = branch.commit.sha
                        result.append(branch_info)
        if flag_to_check_branch==0:
            return [f"Branch not found"]
    except GithubException as e:
        if e.status== 403:
            return [f"You need push access"]
        if e.status==404:
            return [f"No such username or repository"]
        else:
            return [f"e.data"]
    return result

