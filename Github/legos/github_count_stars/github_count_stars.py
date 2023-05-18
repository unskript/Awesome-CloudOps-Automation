##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from github import GithubException

class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )

def github_count_stars_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_count_stars(handle, owner:str, repository:str) -> int:
    """github_count_stars counts number of stars on a repository

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: Count of number of stars on a repository
    """
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login +'/'+ repository
        repo = handle.get_repo(repo_name)
        stars = repo.get_stargazers()
        result = len(list(stars))
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
