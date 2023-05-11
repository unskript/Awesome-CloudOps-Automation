
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from github import GithubException, BadCredentialsException, UnknownObjectException


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


def github_list_pull_request_commits_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_list_pull_request_commits(
        handle,
        owner:str,
        repository:str,
        pull_request_number: int
        ) -> List:
    """github_list_pull_request_commits returns details of pull requests commits

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type pull_request_number: int
        :param pull_request_number: Pull request number. Eg: 167

        :rtype: List of details of pull request commits
    """
    result = []
    pr_number = int(pull_request_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        commits = pr.get_commits()
        for commit in commits:
            commits_dict = {}
            commits_dict["sha"] = commit.sha
            commits_dict["committer"] = commit.committer.login
            commits_dict["date"] = commit.commit.author.date
            result.append(commits_dict)
    except GithubException as e:
        if e.status == 403:
            raise BadCredentialsException("You need admin access") from e
        if e.status == 404:
            raise UnknownObjectException("No such pull number or repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
