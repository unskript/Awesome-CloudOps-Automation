import pprint
from typing import List
from pydantic import BaseModel, Field
from google.cloud import container_v1

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


def gcp_list_nodes_in_gke_cluster_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)

def gcp_list_nodes_in_gke_cluster(handle, project_id: str, zone: str, cluster_name: str) -> List:
    """gcp_list_nodes_in_gke_cluster Returns the list of cluster nodes

        :type project_id: string
        :param project_id: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the cluster in the project should be fetched.

        :type cluster_name: string
        :param cluster_name: Name of the GKE cluster.

        :rtype: list of cluster nodes
    """
    # Create a client
    node_list = []
    client = container_v1.ClusterManagerClient(credentials=handle)
    try:
        response = client.list_node_pools(project_id=project_id, zone=zone,
                                        cluster_id=cluster_name)
        for nodes in response.node_pools:
            node_list.append(nodes.name)
    except Exception as error:
        raise error

    return node_list
