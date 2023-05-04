##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    instance_id: str = Field(
        ...,
        description=('The DB instance identifier for the DB instance to be deleted. '
                     'This parameter isn’t case-sensitive.'),
        title='RDS DB Identifier',
    )
    region: str = Field(
        ..., description='AWS region of instance identifier', title='AWS Region'
    )



def aws_delete_rds_instance_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_rds_instance(handle, region: str, instance_id: str) -> Dict:
    """aws_delete_rds_instance dict of response.

        :type region: string
        :param region: AWS Region.

        :type instance_id: string
        :param instance_id: The DB instance identifier for the DB instance to be deleted.
        This parameter isn’t case-sensitive.

        :rtype: dict of response of deleting an RDS instance
    """
    try:
        ec2Client = handle.client('rds', region_name=region)
        response = ec2Client.delete_db_instance(DBInstanceIdentifier=instance_id)
        return response
    except Exception as e:
        raise Exception(e) from e
