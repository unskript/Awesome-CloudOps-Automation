
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException
import datetime
import pprint


class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"', 
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository'
    )
    threshold_days: int = Field(
        description="Threshold number of days to check for a stale PR. Eg: 45 -> All PR's older than 45 days will be displayed",
        title='Threshold Days'
    )



def github_list_stale_pull_requests_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_list_stale_pull_requests(handle, owner:str, repository:str, threshold_days:int) -> List:
    """github_list_stale_pull_requests returns stale pull requests

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type threshold_days: int
        :param threshold_days: Threshold number of days to find stale PR's

        :rtype: List of stale pull requests
    """
    result = []
    age = int(threshold_days)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login+'/'+repository
        repo = handle.get_repo(repo_name)
        prs = repo.get_pulls()
        for pr in prs:
            prs_dict = {}
            creation_date = pr.created_at
            today = datetime.datetime.now()
            diff = (today - creation_date).days
            if diff >= age:
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
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)

