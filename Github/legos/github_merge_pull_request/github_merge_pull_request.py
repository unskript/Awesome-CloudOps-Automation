
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
    commit_message: str = Field(
        description='Merge commit message.', 
        title='Commit Message'
    )


def github_merge_pull_request_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_merge_pull_request(handle, owner:str, repository:str, pull_request_number: int, commit_message:str) -> str:
    """github_merge_pull_request returns message and commit sha of successfully merged branch

        Note- The base branch is considered to be "master"

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type pull_request_number: int
        :param pull_request_number: Pull request number. Eg:167

        :type commit_message: str
        :param commit_message: Commit Message

        :rtype: String of details with message of successfully merged branch
    """
    pr_number = int(pull_request_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        p = repo.get_pull(pr_number)
        commit = repo.merge(base="master", head=p.head.sha, commit_message=commit_message)
        return f"Successully merged branch with commit SHA- {commit.sha}"
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such pull number or repository or user found")
        if e.status==409:
            raise Exception("Merge Conflict")
        raise e.data
    except Exception as e:
        raise e

