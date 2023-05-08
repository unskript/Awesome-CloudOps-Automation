##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from github import GithubException

class InputSchema(BaseModel):
    owner: str = Field(
        ..., description='Username of the GitHub user. Eg: "johnwick"', title='Owner'
    )
    repository: str = Field(
        ...,
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )


def github_list_webhooks_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_list_webhooks(handle, owner:str, repository: str) -> List:
    """github_list_webhooks returns details of webhooks for a repository

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: List of details of webhooks for a repository
    """
    result = []
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login +'/'+ repository
        repo = handle.get_repo(repo_name)
        webhooks = repo.get_hooks()
        for hook in webhooks:
            hooks = {}
            hooks['url'] = hook.url
            hooks['id'] = hook.id
            hooks['active'] = hook.active
            hooks['events'] = hook.events
            hooks['config'] = hook.config
            result.append(hooks)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
