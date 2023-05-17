##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
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


def github_get_pull_request_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_get_pull_request(handle, owner:str, repository:str, pull_request_number: int) -> Dict:
    """github_get_pull_request returns details of pull requests for a user

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type pull_request_number: int
        :param pull_request_number: Pull request number. Eg: 167

        :rtype: Dict of details of pull request for a user
    """
    prs_dict = {}
    pr_number = int(pull_request_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        prs_dict["pull_number"] = pr.number
        prs_dict["pull_title"] = pr.title
        prs_dict["pull_changed_files"] = pr.changed_files
        prs_dict["pull_review_comments"] = pr.review_comments
        prs_dict["pull_commits"] = pr.commits
    except GithubException as e:
        if e.status == 403:
            raise BadCredentialsException("You need admin access") from e
        if e.status == 404:
            raise UnknownObjectException("No such pull number or repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return prs_dict
