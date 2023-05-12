##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint
from datetime import datetime,timedelta, timezone


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', 
        description='AWS Region to get the Redshift Cluster', 
        title='AWS Region'
    )
    threshold: Optional[float] = Field(
        10,
        description='Threshold(in days) to find long running redshift clusters. Eg: 30, This will find all the clusters that have been created a month ago.',
        title='Threshold(in days)',
    )



def aws_get_long_running_redshift_clusters_without_reserved_nodes_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_long_running_redshift_clusters_without_reserved_nodes(handle, region: str = "", threshold:int = 10) -> Tuple:
    """aws_get_long_running_redshift_clusters_without_reserved_nodes finds Redshift Clusters that are long running and have no reserved nodes

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the Cluster.

        :type threshold: integer
        :param threshold: Threshold(in days) to find long running redshift clusters. Eg: 30, This will find all the clusters that have been created a month ago.

        :rtype: status, list of clusters, nodetype and their region.
    """
    result = []
    reservedNodesPerRegion = {}
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            redshiftClient = handle.client('redshift', region_name=reg)
            response = redshiftClient.describe_reserved_nodes()
            reservedNodesPerType = {}
            if response['ReservedNodes']:
                for node in response['ReservedNodes']:
                    reservedNodesPerType[node['NodeType']] = True
            else:
                continue
            reservedNodesPerRegion[reg] = reservedNodesPerType
        except Exception:
            pass
    for reg in all_regions:
        try:
            redshiftClient = handle.client('redshift', region_name=reg)
            for cluster in redshiftClient.describe_clusters()['Clusters']:
                cluster_age = datetime.now(timezone.utc) - cluster['ClusterCreateTime']
            if cluster['ClusterStatus'] == 'available' and cluster_age > timedelta(days=threshold):
                # Check if the cluster node type is present in the reservedNodesPerRegion map.
                reservedNodes = reservedNodesPerRegion.get(reg)
                if reservedNodes != None:
                    if reservedNodes.get(cluster['NodeType']) == True:
                        continue
                cluster_dict = {}
                cluster_dict["region"] = reg
                cluster_dict["cluster"] = cluster['ClusterIdentifier']
                cluster_dict["node_type"] = cluster['NodeType']
                result.append(cluster_dict)
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)