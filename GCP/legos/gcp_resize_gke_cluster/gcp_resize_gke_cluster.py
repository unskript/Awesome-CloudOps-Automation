import pprint
from typing import Dict
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
    node_id: str = Field(
        title = "Node Name",
        description = "Name of the GKE cluster Node."
    )
    node_count: str = Field(
        title = "Initial Node Count",
        description = "Node count of GKE cluster."
    )


def gcp_resize_gke_cluster_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)


def gcp_resize_gke_cluster(
        handle,
        project_id: str,
        zone: str,
        cluster_name: str,
        node_id: str,
        node_count:int) -> Dict:
    """gcp_resize_gke_cluster Returns the dict of cluster details

        :type project_id: string
        :param project_id: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the cluster in the project should be fetched.

        :type cluster_name: string
        :param cluster_name: Name of the GKE cluster.

        :type node_id: string
        :param node_id: Name of the GKE cluster Node.

        :type node_count: int
        :param node_count: Node count of GKE cluster.

        :rtype: Dict of cluster details
    """
    # Create a client
    client = container_v1.ClusterManagerClient(credentials=handle)
    try:
        request = container_v1.SetNodePoolSizeRequest(
            project_id=project_id,
            zone=zone,
            cluster_id=cluster_name,
            node_pool_id=node_id,
            node_count=node_count,
        )

        res = client.set_node_pool_size(request=request)
        response = MessageToDict(res._pb)

    except Exception as error:
        raise error

    return response
