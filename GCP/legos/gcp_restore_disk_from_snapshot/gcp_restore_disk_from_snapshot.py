##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Dict, Optional
from pydantic import BaseModel, Field
from google.cloud.compute_v1.services.disks import DisksClient
from google.cloud.compute_v1.services.snapshots import SnapshotsClient
from google.cloud.compute_v1.types import Disk, Snapshot



class InputSchema(BaseModel):
    project: str = Field(..., description='GCP Project Name', title='GCP Project')
    zone: str = Field(
        ...,
        description='GCP Zone where the disk and snapshot reside.',
        title='Zone',
    )
    disk: str = Field(
        ..., description='The name of the disk to restore.', title='Disk name'
    )
    snapshot_name: str = Field(
        ...,
        description='The name of the snapshot to restore from.',
        title='Snapshot name',
    )



def gcp_restore_disk_from_snapshot_printer(output):
    if output is None:
        return
    print(output)


def gcp_restore_disk_from_snapshot(handle, project: str, zone: str, disk: str, snapshot_name: str) -> str:
    """gcp_restore_disk_from_snapshot Returns the confirmation of disk restoration.

    :type handle: object
    :param handle: Object returned from Task Validate

    :type project: string
    :param project: Google Cloud Platform Project

    :type zone: string
    :param zone: GCP Zone where the disk and snapshot reside.

    :type disk: string
    :param disk: The name of the disk to restore.

    :type snapshot_name: string
    :param snapshot_name: The name of the snapshot to restore from.

    :rtype: String of disk restoration confirmation
    """
    disks_client = DisksClient(credentials=handle)
    snapshots_client = SnapshotsClient(credentials=handle)

    snapshot = snapshots_client.get(project=project, snapshot=snapshot_name)

    # Create a Disk object with the Snapshot as the source
    disk_to_restore = Disk(name=disk, source_snapshot=snapshot.self_link)

    try:
        # Creating a disk from snapshot
        disks_client.insert(
            project=project, zone=zone, disk_resource=disk_to_restore
        )
    except Exception as e:
        raise e

    return f"Disk {disk} restored from Snapshot {snapshot_name}."