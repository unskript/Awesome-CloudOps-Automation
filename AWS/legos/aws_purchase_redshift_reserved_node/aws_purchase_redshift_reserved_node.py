##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pprint



from typing import Optional

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(
        description='AWS Region.', 
        title='Region'
    )
    reserved_node_offering_id: str = Field(
        description='The unique identifier of the reserved node offering you want to purchase.',
        title='Reserved Node Offering ID',
    )
    no_of_nodes: Optional[int] = Field(
        1,
        description='The number of reserved nodes that you want to purchase.',
        title='No od Nodes to reserve',
    )



def aws_purchase_redshift_reserved_node_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_purchase_redshift_reserved_node(handle, region: str, reserved_node_offering_id: str, no_of_nodes:int=1) -> Dict:
    """aws_purchase_redshift_reserved_node returns dict of response.

        :type region: string
        :param region: AWS Region.

        :type reserved_node_offering_id: string
        :param reserved_node_offering_id: The unique identifier of the reserved node offering you want to purchase.

        :type no_of_nodes: int
        :param no_of_nodes: The number of reserved nodes that you want to purchase.

        :rtype: dict of response metatdata of purchasing a reserved node
    """
    try:
        redshiftClient = handle.client('redshift', region_name=region)
        params = {
            'ReservedNodeOfferingId': reserved_node_offering_id,
            'NodeCount': no_of_nodes
            }
        response = redshiftClient.purchase_reserved_node_offering(**params)
        return response
    except Exception as e:
        raise Exception(e)


