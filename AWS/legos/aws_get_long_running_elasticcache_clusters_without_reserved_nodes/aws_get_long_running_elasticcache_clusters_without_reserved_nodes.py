##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', description='AWS Region to get the ElasticCache Cluster', title='AWS Region'
    )
    threshold: Optional[float] = Field(
        10,
        description='Threshold(in days) to find long running ElasticCache clusters. Eg: 30, This will find all the clusters that have been created a month ago.',
        title='Threshold(in days)',
    )



def aws_get_long_running_elasticcache_clusters_without_reserved_nodes_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_long_running_elasticcache_clusters_without_reserved_nodes(handle, region: str = "", threshold:int = 10) -> Tuple:
    """aws_get_long_running_elasticcache_clusters_without_reserved_nodes finds ElasticCache Clusters that are long running and have no reserved nodes

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the Cluster.

        :type threshold: integer
        :param threshold: Threshold(in days) to find long running ElasticCache clusters. Eg: 30, This will find all the clusters that have been created a month ago.

        :rtype: status, list of clusters, nodetype and their region.
    """
    result = []
    reservedNodesPerRegion = {}
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    # Get the list of reserved node per region per type. We just need to maintain
    # what type of reserved nodes are present per region. So, reservedNodesPerRegion
    # would be like:
    # <region>:{<nodeType>:True/False}
    for reg in all_regions:
        try:
            elasticacheClient = handle.client('elasticache', region_name=reg)
            response = elasticacheClient.describe_reserved_cache_nodes()
            reservedNodesPerType = {}
            if response['ReservedCacheNodes']:
                for node in response['ReservedCacheNodes']:
                    reservedNodesPerType[node['CacheNodeType']] = True
            else:
                continue
            reservedNodesPerRegion[reg] = reservedNodesPerType
        except Exception:
            pass

    for reg in all_regions:
        try:
            elasticacheClient = handle.client('elasticache', region_name=reg)
            for cluster in elasticacheClient.describe_cache_clusters()['CacheClusters']:
                cluster_age = datetime.now(timezone.utc) - cluster['CacheClusterCreateTime']
                if cluster_age > timedelta(days=threshold):
                    # Check if the cluster node type is present in the reservedNodesPerRegion map.
                    reservedNodes = reservedNodesPerRegion.get(reg)
                    if reservedNodes is not None:
                        if reservedNodes.get(cluster['CacheNodeType']) is True:
                            continue
                    cluster_dict = {}
                    cluster_dict["region"] = reg
                    cluster_dict["cluster"] = cluster['CacheClusterId']
                    cluster_dict["node_type"] = cluster['CacheNodeType']
                    result.append(cluster_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
