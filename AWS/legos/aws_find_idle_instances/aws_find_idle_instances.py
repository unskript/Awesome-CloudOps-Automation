##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from typing import Dict, Tuple
import pprint
import datetime

from typing import Optional

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    idle_cpu_threshold: int = Field(
        5, 
        description='Idle CPU threshold (in percent)', 
        title='Idle CPU Threshold'
    )
    idle_duration: int = Field(
       6, 
       description='Idle duration (in hours)', 
       title='Idle Duration'
    )
    region: Optional[str] = Field(
        '',
        description='AWS Region to get the instances from. Eg: "us-west-2"',
        title='Region',
    )


def aws_find_idle_instances_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def is_instance_idle(instance_id , idle_cpu_threshold, idle_duration, cloudwatchclient):
    try:
        now = datetime.datetime.utcnow()
        start_time = now - datetime.timedelta(hours=idle_duration)
        cpu_utilization_stats = cloudwatchclient.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start_time.isoformat(),
            EndTime=now.isoformat(),
            Period=3600,
            Statistics=["Average"],
        )
        if not cpu_utilization_stats["Datapoints"]:
            return False
        average_cpu = sum([datapoint["Average"] for datapoint in cpu_utilization_stats["Datapoints"]]) / len(cpu_utilization_stats["Datapoints"])
    except Exception as e:
        raise e
    return average_cpu < idle_cpu_threshold

def aws_find_idle_instances(handle, idle_cpu_threshold:int, idle_duration:int, region:str='') -> Tuple:
    """aws_find_idle_instances finds idle EC2 instances

    :type region: string
    :param region: AWS Region to get the instances from. Eg: "us-west-2"

    :type idle_cpu_threshold: int
    :param idle_cpu_threshold: (in percent) Idle CPU threshold (in percent)

    :type idle_duration: int
    :param idle_duration: (in hours) Idle CPU threshold (in hours)

    :rtype: Tuple with status result and list of Idle Instances.
    """
    result = []
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            ec2client = handle.client('ec2', region_name=reg)
            cloudwatchclient = handle.client("cloudwatch", region_name=reg)
            all_instances = ec2client.describe_instances()
            for instance in all_instances['Reservations']:
                for i in instance['Instances']:
                    if i['State']["Name"] == "running" and is_instance_idle(i['InstanceId'], reg, idle_cpu_threshold,idle_duration, cloudwatchclient ):
                        idle_instances = {}
                        idle_instances["instance"] = i['InstanceId']
                        idle_instances["region"] = reg
                        result.append(idle_instances)
        except Exception:
            pass
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)



