
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


def github_get_pull_request_reviewers_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_get_pull_request_reviewers(handle, owner:str, repository:str, pull_request_number: int) -> List:
    """github_get_pull_request_reviewers returns reviewers of a pull request

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type pull_request_number: int
        :param pull_request_number: Pull request number. Eg: 167

        :rtype: List of reviewers of a pull request
    """
    result = []
    pr_number = int(pull_request_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        review_requests = pr.get_review_requests()
        for request in review_requests:
            for r in request:
                result.append(r.login)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such pull number or repository or user found")
        raise e.data
    except Exception as e:
        raise e
    if len(result) == 0:
        return [f"No reviewers added for Pull Number {pr.number}"]
    return result


