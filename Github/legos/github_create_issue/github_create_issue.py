##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
from typing import Dict
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
    title: str = Field(
        description='Title if the Github Issue',
        title='Title of the Issue'
    )
    description: str = Field(
        description='Description of the Github Issue',
        title='Title of the Issue'
    )
    assignee: str = Field(
        description='Username of the Github User to assign this issue to ',
        title='Username of the Assignee'
    )



def github_create_issue_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_create_issue(
        handle,
        owner:str,
        repository:str,
        title:str,
        description:str,
        assignee: str
        ) -> Dict:
    """github_create_issue returns details of newly created issue

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type title: string
        :param title: Title if the Github Issue

        :type description: string
        :param description: Description of the Github Issue

        :type assignee: string
        :param assignee: Username of the Assignee
        
        :rtype: Dict of newly created issue
    """
    issue_details = {}
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login + '/' + repository
        repo = handle.get_repo(repo_name)
        res = repo.create_issue(title=title, body=description, assignee=assignee)
        issue_details["title"] = res.title
        issue_details["issue_number"] = res.number
        issue_details["assignee"] = res.assignee.login
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return issue_details
