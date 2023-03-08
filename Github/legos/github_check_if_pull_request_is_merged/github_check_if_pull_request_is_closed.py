##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, List,Tuple
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


def github_check_if_pull_request_is_merged_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_check_if_pull_request_is_merged(handle, owner:str, repository:str, pull_request_number: int) -> Tuple:
    """github_check_if_pull_request_is_merged returns status, 

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type pull_request_number: int
        :param pull_request_number: Pull request number. Eg: 167

        :rtype: Status, List of details of pull requests if it is not merged
    """
    result = []
    prs_dict = {}
    pr_number = int(pull_request_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        check = pr.is_merged()
        if check is False:
            prs_dict["pull_number"] = pr.number
            prs_dict["pull_title"] = pr.title
            prs_dict["pull_changed_files"] = pr.changed_files
            prs_dict["pull_review_comments"] = pr.review_comments
            prs_dict["pull_commits"] = pr.commits
            result.append(prs_dict)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such pull number or repository or user found")
        raise e.data
    except Exception as e:
        raise e
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)

