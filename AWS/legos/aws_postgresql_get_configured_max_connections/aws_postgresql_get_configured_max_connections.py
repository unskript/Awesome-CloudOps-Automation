##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint


class InputSchema(BaseModel):
    cluster_identifier: str = Field(
        title='DB Identifier',
        description='RDS Cluster DB Identifier.')
    region: str = Field(
        title='Region',
        description='AWS Region of the Postgres DB Cluster.')


def aws_postgresql_get_configured_max_connections_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_postgresql_get_configured_max_connections(handle, cluster_identifier: str, region: str) -> str:
    """aws_postgresql_get_configured_max_connection Get the configured max connection.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type cluster_identifier: string
          :param cluster_identifier: RDS Cluster DB Identifier.

          :type region: string
          :param region: AWS Region of the Postgres DB Cluster.

          :rtype: All the results of the query.
      """
    # Input param validation.

    ec2_client = handle.client('ec2', region_name=region)

    # Get the list of instance types and their memory info.
    paginator = ec2_client.get_paginator('describe_instance_types')
    page_iterator = paginator.paginate()

    instance_type_memory_map = {}
    try:
        for page in page_iterator:
            for instance_type in page['InstanceTypes']:
                instance_type_memory_map[instance_type['InstanceType']] = instance_type['MemoryInfo']['SizeInMiB']
    except Exception as e:
        print(f'describe_instance_types hit an exception {str(e)}')
        raise e

    rds_client = handle.client('rds', region_name=region)
    try:
        describe_db_clusters_resp = rds_client.describe_db_clusters(DBClusterIdentifier=cluster_identifier)
    except Exception as e:
        print(f'describe_db_clusters for cluster {cluster_identifier} hit an exception, {str(e)}')
        raise e

    cluster_info = describe_db_clusters_resp['DBClusters'][0]
    cluster_parameter_group_name = cluster_info['DBClusterParameterGroup']
    cluster_instances = []
    for info in cluster_info['DBClusterMembers']:
        cluster_instances.append(info['DBInstanceIdentifier'])

    # Now get the type of the DBInstance Identifier.
    # ASSUMPTION: All nodes are of the same type.
    try:
        describe_instance_resp = rds_client.describe_db_instances(DBInstanceIdentifier=cluster_instances[0])
    except Exception as e:
        print(f'describe_db_instance for cluster {cluster_instances[0]} failed, {str(e)}')
        raise e

    cluster_instance_type = describe_instance_resp['DBInstances'][0]['DBInstanceClass'].lstrip('db.')
    cluster_instance_memory = instance_type_memory_map[cluster_instance_type]

    # Get the max connections for this postgresql. 2 options here:
    # 1. If the max connection is configured via parameter group, get it from there.
    # 2. If its default, its LEAST({DBInstanceClassMemory/9531392}, 5000)
    paginator = rds_client.get_paginator('describe_db_parameters')
    operation_parameters = {'DBParameterGroupName': cluster_parameter_group_name}
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for parameter in page['Parameters']:
            if parameter['ParameterName'] == 'max_connections':
                if parameter['ParameterValue'].startswith('LEAST'):
                    return str(int(min(cluster_instance_memory * 1048576 / 9531392, 5000)))
                else:
                    return parameter['ParameterValue']
