##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Dict, Optional
from pydantic import BaseModel, Field
from google.cloud.compute_v1.services.disks import DisksClient
from google.cloud.compute_v1.types import Snapshot


class InputSchema(BaseModel):
    project: str = Field(..., description='GCP Project Name', title='GCP Project')
    zone: str = Field(
        ...,
        description='GCP Zone where instance list should be gotten from',
        title='Zone',
    )
    disk: str = Field(
        ..., description='The name of the disk to create a snapshot of.', title='Disk name'
    )
    snapshot_name: str = Field(
        '',
        description='The name of the snapshot to create. If not provided, a name will be automatically generated.',
        title='Snapshot name',
    )



def gcp_create_disk_snapshot_printer(output):
    if output is None:
        return
    print(output)

def gcp_create_disk_snapshot(handle, project: str, zone:str, disk: str, snapshot_name: str) -> str:
    """gcp_create_disk_snapshot Returns the confirmation of snapshot creation.

    :type project: string
    :param project: Google Cloud Platform Project

    :type zone: string
    :param zone: Zone to which the instance list in the project should be fetched.

    :type disk: string
    :param disk: The name of the disk to create a snapshot of.

    :type snapshot_name: string
    :param snapshot_name: The name of the snapshot to create. If not provided, a name will be automatically generated.

    :rtype: String of snapshot creation confirmation
    """
    disks_client = DisksClient(credentials=handle)

    snapshot = Snapshot(name=snapshot_name)
    try:
        disks_client.create_snapshot(
            project=project, zone=zone, disk=disk, snapshot_resource=snapshot
        )
    except Exception as e:
        raise e
    return f"Snapshot {snapshot_name} created."


