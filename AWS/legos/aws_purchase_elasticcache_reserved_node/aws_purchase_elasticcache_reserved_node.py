##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint


class InputSchema(BaseModel):
    region: str = Field(
        description='AWS Region.', 
        title='Region'
    )
    reserved_node_offering_id: str = Field(
        description='The unique identifier of the reserved cache node offering you want to purchase.',
        title='Reserved Cache Node Offering ID',
    )
    no_of_nodes: Optional[int] = Field(
        1,
        description='The number of reserved cache nodes that you want to purchase.',
        title='No of nodes to purchase',
    )



def aws_purchase_elasticcache_reserved_node_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_purchase_elasticcache_reserved_node(handle, region: str, reserved_node_offering_id: str, no_of_nodes:int=1) -> Dict:
    """aws_purchase_elasticcache_reserved_node returns dict of response.

        :type region: string
        :param region: AWS Region.

        :type reserved_node_offering_id: string
        :param reserved_node_offering_id: The unique identifier of the reserved node offering you want to purchase. Example: '438012d3-4052-4cc7-b2e3-8d3372e0e706'

        :type no_of_nodes: int
        :param no_of_nodes: The number of reserved nodes that you want to purchase.

        :rtype: dict of response metatdata of purchasing a reserved node
    """
    try:
        elasticClient = handle.client('elasticache', region_name=region)
        params = {
            'ReservedCacheNodesOfferingId': reserved_node_offering_id,
            'CacheNodeCount': no_of_nodes
            }
        response = elasticClient.purchase_reserved_cache_nodes_offering(**params)
        return response
    except Exception as e:
        raise Exception(e)


