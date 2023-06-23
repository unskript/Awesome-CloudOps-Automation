##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
import pprint
from datetime import datetime,timedelta


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        '', description='AWS Region to get the Redshift Cluster', title='AWS Region'
    )
    duration_minutes: Optional[int] = Field(
        5,
        description='Value in minutes to determine the start time of the data points. ',
        title='Duration (in minutes)',
    )
    utilization_threshold: Optional[int] = Field(
        10,
        description='The threshold value in percent of CPU utilization of the Redshift cluster',
        title='CPU utilization threshold(in %)',
    )



def aws_find_redshift_clusters_with_low_cpu_utilization_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_redshift_clusters_with_low_cpu_utilization(handle, utilization_threshold:int=10, region: str = "", duration_minutes:int=5) -> Tuple:
    """aws_find_redshift_clusters_with_low_cpu_utilization finds Redshift Clusters that have a lower cpu utlization than the given threshold

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type region: string
        :param region: Region of the Cluster.

        :type utilization_threshold: integer
        :param utilization_threshold: The threshold percentage of CPU utilization for a Redshift Cluster.

        :type duration_minutes: integer
        :param duration_minutes: The threshold percentage of CPU utilization for a Redshift Cluster.

        :rtype: status, list of clusters and their region.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            redshiftClient = handle.client('redshift', region_name=reg)
            cloudwatchClient = handle.client('cloudwatch', region_name=reg)
            for cluster in redshiftClient.describe_clusters()['Clusters']:
                cluster_identifier = cluster['ClusterIdentifier']
                response = cloudwatchClient.get_metric_statistics(
                Namespace='AWS/Redshift',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'ClusterIdentifier',
                        'Value': cluster_identifier
                    }
                ],
                StartTime=(datetime.utcnow() - timedelta(minutes=duration_minutes)).isoformat(),
                EndTime=datetime.utcnow().isoformat(),
                Period=60,
                Statistics=['Average']
                )
                if len(response['Datapoints']) != 0:
                    cpu_usage_percent = response['Datapoints'][-1]['Average']
                    if cpu_usage_percent < utilization_threshold:
                        cluster_dict = {}
                        cluster_dict["region"] = reg
                        cluster_dict["cluster"] = cluster_identifier
                        result.append(cluster_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)


