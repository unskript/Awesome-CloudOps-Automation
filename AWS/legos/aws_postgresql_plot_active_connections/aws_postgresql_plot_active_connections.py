##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt


class InputSchema(BaseModel):
    cluster_identifier: str = Field(
        title='DB Identifier',
        description='RDS DB Identifier.')
    max_connections: int = Field(
        title='Max Connections',
        description='Configured max connections.')
    time_since: int = Field(
        title='Time Since',
        description=('Starting from now, window (in seconds) for which you '
                     'want to get the datapoints for.')
                     )
    region: str = Field(
        title='Region',
        description='AWS Region of the Postgres DB Cluster.')


def aws_postgresql_plot_active_connections(
        handle,
        cluster_identifier: str,
        max_connections: int,
        time_since: int,
        region: str
        ) -> None:
    """aws_postgresql_plot_active_connections Plots the active connections
       normalized by the max connections.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type cluster_identifier: string
          :param cluster_identifier: RDS DB Identifier.

          :type max_connections: string
          :param max_connections: Configured max connections.

          :type time_since: int
          :param time_since: Starting from now, window (in seconds) for which
          you want to get the datapoints for.

          :type region: string
          :param region: AWS Region of the Postgres DB Cluster.

          :rtype: All the results of the query.
      """
    # Input param validation.

    # Get the list of instances in this cluster and their types.
    rds_client = handle.client('rds', region_name=region)

    try:
        describe_db_clusters_resp = rds_client.describe_db_clusters(
            DBClusterIdentifier=cluster_identifier
            )
    except Exception as e:
        print(f'describe_db_clusters for cluster {cluster_identifier} hit an exception, {str(e)}')
        raise e
    cluster_info = describe_db_clusters_resp['DBClusters'][0]
    cluster_instances = []
    for value in cluster_info['DBClusterMembers']:
        cluster_instances.append(value['DBInstanceIdentifier'])

    cloud_watch_client = handle.client('cloudwatch', region_name=region)

    plt.figure(figsize=(10, 10))
    plt.ylabel('ActiveConnections/MaxConnections')
    for cluster_instance in cluster_instances:
        ts, data_points = get_normalized_active_connections(
            cloud_watch_client,
            cluster_instance,
            time_since, max_connections
            )
        plt.plot(ts, data_points, label=cluster_instance)
    plt.legend(loc=1, fontsize='medium')
    plt.show()


def get_normalized_active_connections(
        cloudWatch_client,
        db_instance_id,
        time_since,
        max_connections
        ):
    # Gets metric statistics.
    res = cloudWatch_client.get_metric_statistics(
        Namespace="AWS/RDS",
        MetricName="DatabaseConnections",
        Dimensions=[{"Name": "DBInstanceIdentifier", "Value": db_instance_id}],
        Period=6000,
        StartTime=datetime.utcnow() - timedelta(seconds=time_since),
        EndTime=datetime.utcnow(),
        Statistics=[
            "Average"
        ]
    )

    data = {}
    for datapoints in res['Datapoints']:
        data[datapoints['Timestamp']] = datapoints["Average"] / max_connections

    # Sorts data.
    data_keys = data.keys()
    times_stamps = list(data_keys)
    times_stamps.sort()
    sorted_values = []
    for value in times_stamps:
        sorted_values.append(data[value])

    return (times_stamps, sorted_values)
