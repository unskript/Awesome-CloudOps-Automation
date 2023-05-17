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
    reserved_instance_offering_id: str = Field(
        description='The ID of the Reserved DB instance offering to purchase. Example: 438012d3-4052-4cc7-b2e3-8d3372e0e706',
        title='Reserved Instance Offering ID',
    )
    db_instance_count: Optional[int] = Field(
        1, 
        description='The number of instances to reserve.', 
        title='Instance Count'
    )



def aws_purchase_rds_reserved_instance_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_purchase_rds_reserved_instance(handle, region: str, reserved_instance_offering_id: str, db_instance_count:int=1) -> Dict:
    """aws_purchase_rds_reserved_instance returns dict of response.

        :type region: string
        :param region: AWS Region.

        :type reserved_instance_offering_id: string
        :param reserved_instance_offering_id: The unique identifier of the reserved instance offering you want to purchase.

        :type db_instance_count: int
        :param db_instance_count: The number of reserved instances that you want to purchase.

        :rtype: dict of response metatdata of purchasing a reserved instance
    """
    try:
        redshiftClient = handle.client('redshift', region_name=region)
        params = {
            'ReservedDBInstancesOfferingId': reserved_instance_offering_id,
            'DBInstanceCount': db_instance_count
            }
        response = redshiftClient.purchase_reserved_db_instances_offering(**params)
        return response
    except Exception as e:
        raise Exception(e)


