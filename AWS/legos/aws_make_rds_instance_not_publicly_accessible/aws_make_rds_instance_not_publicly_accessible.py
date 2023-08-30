##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    db_instance_identifier: str = Field(
        ...,
        description='The DB instance identifier for the DB instance to be deleted. This parameter isn’t case-sensitive.',
        title='RDS Instance Identifier',
    )
    region: str = Field(
        ..., description='AWS region of instance identifier', title='AWS Region'
    )



def aws_make_rds_instance_not_publicly_accessible_printer(output):
    if output is None:
        return
    print(output)


def aws_make_rds_instance_not_publicly_accessible(handle, db_instance_identifier: str, region: str) -> str:
    """
    aws_make_rds_instance_not_publicly_accessible makes the specified RDS instance not publicly accessible.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :type db_instance_identifier: string
    :param db_instance_identifier: Identifier of the RDS instance.

    :type region: string
    :param region: Region of the RDS instance.

    :rtype: Response of the operation.
    """
    try:
        rdsClient = handle.client('rds', region_name=region)
        rdsClient.modify_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            PubliclyAccessible=False
        )
    except Exception as e:
        raise e
    return f"Public accessiblilty is being changed to False..."


