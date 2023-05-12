#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from typing import Dict
import requests
from pydantic import BaseModel, Field
from requests.auth import HTTPDigestAuth


class InputSchema(BaseModel):
    project_name: str = Field(
        title='Project Name',
        description='Atlas Project Name'
    )
    cluster_name: str = Field(
        title='Cluster Name',
        description='Atlas Cluster Name.'
    )
    description: str = Field(
        title='Description',
        description="Description of the on-demand snapshot."
    )
    retention_in_days: int = Field(
        default=7,
        title='Retention In Days',
        description=('Number of days that Atlas should retain the '
                     'on-demand snapshot. Must be at least 1.')
    )

def mongodb_atlas_cluster_backup_printer(output):
    if output is None:
        return
    print("\n\n")
    pprint.pprint(output)


def mongodb_atlas_cluster_backup(
        handle,
        project_name: str,
        cluster_name: str,
        description: str,
        retention_in_days: int = 1) -> Dict:
    """mongodb_atlas_cluster_backup Create backup of MongoDB Cluster.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type project_name: str
        :param project_name: Atlas Project Name.

        :type cluster_name: str
        :param cluster_name: Atlas Cluster Name.

        :type description: str
        :param description: Description of the on-demand snapshot.

        :type retention_in_days: int
        :param retention_in_days: Retention In Days.

        :rtype: Dict of SnapShot.
    """
    atlas_base_url = handle.get_base_url()
    public_key = handle.get_public_key()
    private_key = handle.get_private_key()
    auth = HTTPDigestAuth(public_key, private_key)

    #Get Project ID from Project Name
    url =  atlas_base_url + f"/groups/byName/{project_name}"
    try:
        resp = requests.get(url, auth=auth)
        resp.raise_for_status()
    except Exception as e:
        return {'Get project id failed': str(e)}

    project_resp = resp.json()
    group_id = project_resp.get("id")

    body = {
        "description": description,
        "retentionInDays" : retention_in_days
    }
    url =  atlas_base_url + (f"/groups/{group_id}/clusters/{cluster_name}/backup"
                             "/snapshots/?pretty=true")
    try:
        response = requests.post(url, auth=auth, json=body)
        response.raise_for_status()
    except Exception as e:
        return {'Start snapshot failed': str(e)}
    return response.json()
