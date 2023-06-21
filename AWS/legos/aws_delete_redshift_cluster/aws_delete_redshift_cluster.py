##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    cluster_identifier: str = Field(
        ...,
        description='The identifier of the cluster to be deleted.',
        title='Cluster Identifier',
    )
    skip_final_cluster_snapshot: Optional[bool] = Field(
        False,
        description='Determines whether a final snapshot of the cluster is created before Amazon Redshift deletes the cluster. If true, a final cluster snapshot is not created. If false, a final cluster snapshot is created before the cluster is deleted.',
        title='Skip Final Cluster Snapshot',
    )



def aws_delete_redshift_cluster_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_redshift_cluster(handle, region: str, cluster_identifier: str, skip_final_cluster_snapshot:bool=False) -> Dict:
    """aws_delete_redshift_cluster dict response.

        :type region: string
        :param region: AWS Region.

        :type cluster_identifier: string
        :param cluster_identifier: The identifier of the cluster to be deleted.

        :type skip_final_cluster_snapshot: boolean
        :param skip_final_cluster_snapshot: Determines whether a final snapshot of the cluster is created before Amazon Redshift deletes the cluster. If true, a final cluster snapshot is not created. If false, a final cluster snapshot is created before the cluster is deleted.

        :rtype: dict of response
    """
    try:
        redshiftClient = handle.client('redshift', region_name=region)
        response = redshiftClient.delete_cluster(
            ClusterIdentifier=cluster_identifier,
            SkipFinalClusterSnapshot=skip_final_cluster_snapshot
            )
        return response
    except Exception as e:
        raise Exception(e)


