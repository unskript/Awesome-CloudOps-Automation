
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
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
    issue_number: int = Field(
        ...,
        description='Issue Number. Eg: "367"',
        title='Issue Number',
    )
    assignee: int = Field(
        ...,
        description='Username of the assignee.',
        title='Assignee Username',
    )


def github_assign_issue_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_assign_issue(
        handle,
        owner:str,
        repository:str,
        issue_number:int,
        assignee:str
        ) -> str:
    """github_assign_issue assigns an issue to user

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type issue_number: int
        :param issue_number: Issue number. Eg: 345

        :type assignee: string
        :param assignees: Username of the assignee.

        :rtype: Status of assigning an issue to a user
    """
    issue_no = int(issue_number)
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login + '/' + repository
        repo = handle.get_repo(repo_name)
        issue = repo.get_issue(issue_no)
        result = issue.add_to_assignees(assignee)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such repository or user found") from e
        raise e.data
    except Exception as e:
        raise e
    if result is None:
        return f"Issue {issue_no} assigned to {assignee}"
    return f"Unable to assign Issue {issue_no} to {assignee}"
