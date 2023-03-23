
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
from typing import Optional, List, Dict
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


def github_get_issue_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_get_issue(handle, owner:str, repository:str, issue_number:int) -> Dict:
    """github_get_issue returns details of the issue

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type issue_number: int
        :param issue_number: Issue number. Eg: 345

        :rtype: Dict of issue details
    """
    issue_no = int(issue_number)
    issue_details = {}
    try:
        owner = handle.get_user(owner)
        repo_name = owner.login + '/' + repository
        repo = handle.get_repo(repo_name)
        issues = repo.get_issues()
        for issue in issues:
            if issue.number == issue_no:
                issue_details["title"] = issue.title
                issue_details["issue_number"] = issue.number
                if type(issue.assignee) == 'NoneType':
                    issue_details["assignee"] = issue.assignee.login
                else:
                    issue_details["assignee"] = issue.assignee
                issue_details["body"] = issue.body
                issue_details["state"] = issue.state
                dummy_date = issue.updated_at
                formatted_date = dummy_date.strftime("%d-%m-%Y")
                issue_details["updated_at"] = formatted_date
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such repository or user found")
        raise e.data
    except Exception as e:
        raise e
    return issue_details