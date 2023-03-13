
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
        ..., description='Username of the GitHub user. Eg: "johnwick"', title='Owner'
    )
    repository: str = Field(
        ...,
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )



def github_list_stargazers_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_list_stargazers(handle, owner:str, repository:str) -> List:
    """github_list_stargazers returns first 100 stargazers for a Github Repository

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: List of first 100 stargazers for a Github Repository
    """
    result = []
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login +'/'+ repository
        repo = handle.get_repo(repo_name)
        stars = repo.get_stargazers_with_dates()
        for star in stars[len(list(stars))-100:]:
            stargazer_details = {}
            stargazer_details["name"] = star.user.login
            dummy_date = star.starred_at
            formatted_date = dummy_date.strftime("%d-%m-%Y")
            stargazer_details["date"] = formatted_date
            result.append(stargazer_details)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such repository or user found")
        raise e.data
    except Exception as e:
        raise e
    return result


