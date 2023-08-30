##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
import datetime
from pydantic import BaseModel, Field
from tabulate import tabulate
from github import GithubException, BadCredentialsException, UnknownObjectException


class InputSchema(BaseModel):
    owner: Optional[str] = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository'
    )
    threshold: Optional[int] = Field(
        description=("Threshold number of days to check for a stale PR. Eg: 45 -> "
                     "All PR's older than 45 days will be displayed"),
        title='Threshold (in Days)'
    )


def github_list_stale_pull_requests_printer(output_tuple):
    if output_tuple is None or output_tuple[1] is None:
        return
    success, output = output_tuple
    if not success:
        headers = ["PR Number", "Title"]
        table = [[pr["number"], pr["title"]] for pr in output]
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("No stale pull requests found.")


def github_list_stale_pull_requests(handle, repository: str, threshold: int = 14,  owner:str = "") -> Tuple:
    """github_list_stale_pull_requests returns stale pull requests

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :type owner: string (Optional)
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type threshold: int (Optional)
        :param threshold: Threshold number of days to find stale PR's

        :rtype: Status, List of stale pull requests
    """
    result = []
    try:
        if len(owner)==0 or owner is None:
            owner = handle.get_user().login
        owner = handle.get_user().login
        repo = handle.get_repo(f"{owner}/{repository}")
        prs = repo.get_pulls()

        # Check if there are no open pull requests
        if prs.get_page(0) == []:
            print("No pull requests are open at the moment.")
            return (True, None)

        today = datetime.datetime.now()

        for pr in repo.get_pulls():
            print(pr)
            creation_date = pr.created_at
            diff = (today - creation_date).days
            if diff >= threshold:
                result.append({"number": pr.number, "title": pr.title})

    except Exception as e:
        raise e

    return (False, result) if result else (True, None)