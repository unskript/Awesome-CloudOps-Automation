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


def gcp_list_gke_cluster_printer(output):
    if len(output) == 0:
        return
    pprint.pprint(output)

def gcp_list_gke_cluster(handle, project_id: str, zone: str) -> List:
    """gcp_list_gke_cluster Returns the list of cluster

        :type project_id: string
        :param project_id: Google Cloud Platform Project

        :type zone: string
        :param zone: Zone to which the cluster in the project should be fetched.

        :rtype: list of cluster
    """
    # Create a client
    cluster_list = []
    client = container_v1.ClusterManagerClient(credentials=handle)
    try:
        response = client.list_clusters(project_id=project_id, zone=zone)
        for cluster in response.clusters:
            cluster_list.append(cluster.name)
    except Exception as error:
        cluster_list.append(error)
    
    return cluster_list
