import pprint
from typing import List, Dict
from pydantic import BaseModel, Field
from google.cloud import container_v1
from google.protobuf.json_format import MessageToDict


class InputSchema(BaseModel):
    project_id: str = Field(
        title = "GCP Project",
        description = "GCP Project Name"
    )
    zone: str = Field(
        title = "Zone",
        description = "GCP Zone where instance list should be gotten from"
    )
    cluster_name: str = Field(
        title = "Cluster Name",
        description = "Name of the GKE cluster."
    )


def gcp_describe_gke_cluster_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)


def gcp_describe_gke_cluster(handle, project_id: str, zone: str, cluster_name: str) -> Dict:
    """gcp_describe_gke_cluster Returns the dict of cluster details

        :type project_id: string
        :param project_id: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the cluster in the project should be fetched.

        :type cluster_name: string
        :param cluster_name: Name of the GKE cluster.

        :rtype: Dict of cluster details
    """
    # Create a client
    client = container_v1.ClusterManagerClient(credentials=handle)
    try:
        res = client.get_cluster(project_id=project_id, zone=zone,
                                        cluster_id=cluster_name)

        response = MessageToDict(res._pb)

    except Exception as error:
        response = {"error":error}

    return response
