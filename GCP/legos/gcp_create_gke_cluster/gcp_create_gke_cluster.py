import pprint
from typing import List, Dict
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
    node_count: str = Field(
        title = "Initial Node Count",
        description = "Node count of GKE cluster."
    )


def get_gcp_instance_list_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)

def create_gke_cluster(handle, project_id: str, zone: str, cluster_name: str, node_count: int) -> Dict:
    """create_gke_cluster Returns the dict of cluster info

        :type project_id: string
        :param project_id: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the cluster in the project should be fetched.

        :type cluster_name: string
        :param cluster_name: Name of the GKE cluster.

        :type initial_node_count: int
        :param initial_node_count: Node count of GKE cluster.

        :rtype: Dict of cluster info
    """
    # Create a client
    client = container_v1.ClusterManagerClient(credentials=handle)
    try:
        response = client.create_cluster(project_id=project_id, 
                                     zone=zone,
                                     cluster={'name':cluster_name,
                                              'initial_node_count':node_count})
    except Exception as error:
        response = {"error":error}

    return response