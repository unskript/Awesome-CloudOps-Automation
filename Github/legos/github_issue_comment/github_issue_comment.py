##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )
    issue_comment: str = Field(
        description='The Comment to add to the Issue',
        title='Issue Comment'
    )
    issue_number: str = Field(
        description='Github Issue where Comment is to be added.',
        title='Issue Number'
    )


def github_issue_comment_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_issue_comment(
        handle,
        owner:str,
        repository:str,
        issue_number:str,
        issue_comment:str
        ) -> str:
    issue_number = int(issue_number)
    owner = handle.get_user(owner)
    repo_name = owner.login +'/'+ repository
    repo = handle.get_repo(repo_name)
    # Get the issue by its number
    issue = repo.get_issue(issue_number)

    # Add a comment to the issue
    issue.create_comment(issue_comment)
    return "added comment"
