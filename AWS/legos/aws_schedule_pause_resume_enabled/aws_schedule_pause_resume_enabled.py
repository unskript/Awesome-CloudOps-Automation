# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(
        title='Region',
        description='AWS Region of the EBS volume')
    iam_role_arn: str = Field(
        title='IAM Role',
        description='The ARN of the IAM role.')
    cluster_name: str = Field(
        title='Redshift Cluster Name',
        description='The name of the Redshift cluster.')
    pause_schedule_expression: str = Field(
        title='Cron Expression for Pause',
        description='The cron expression for the pause schedule.')
    resume_schedule_expression: str = Field(
        title='Cron Expression for Resume',
        description='The cron expression for the resume schedule.')


def aws_schedule_pause_resume_enabled_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_schedule_pause_resume_enabled(handle,
                                      iam_role_arn: str,
                                      cluster_name: str,
                                      region: str,
                                      pause_schedule_expression: str,
                                      resume_schedule_expression: str) -> List:
    """aws_schedule_pause_resume_enabled schedule pause and resume enabled.

    :type iam_role_arn: str
    :param iam_role_arn: The ARN of the IAM role.

    :type cluster_name: str
    :param cluster_name: The name of the Redshift cluster.

    :type region: str
    :param region: AWS Region.

    :type pause_schedule_expression: str
    :param pause_schedule_expression: The cron expression for the pause schedule.

    :type resume_schedule_expression: str
    :param resume_schedule_expression: The cron expression for the resume schedule.

    :rtype: List
    :return: A list of pause and resume enabled status.
    """
    result = []
    pause_action_name = f"{cluster_name}-scheduled-pause"
    resume_action_name = f"{cluster_name}-scheduled-resume"

    try:
        redshift_client = handle.client('redshift', region_name=region)
        # Schedule pause action
        response_pause = redshift_client.create_scheduled_action(
            ScheduledActionName=pause_action_name,
            TargetAction={
                'PauseCluster': {'ClusterIdentifier': cluster_name}
            },
            Schedule=pause_schedule_expression,
            IamRole=iam_role_arn,
            Enable=True
        )
        result.append(response_pause)
        # Schedule resume action
        response_resume = redshift_client.create_scheduled_action(
            ScheduledActionName=resume_action_name,
            TargetAction={
                'ResumeCluster': {'ClusterIdentifier': cluster_name}
            },
            Schedule=resume_schedule_expression,
            IamRole=iam_role_arn,
            Enable=True
        )
        result.append(response_resume)

    except Exception as error:
        raise Exception(error)

    return result