##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import botocore.config
from unskript.connectors.aws import aws_get_paginator
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions

class InputSchema(BaseModel):
    time_period_in_days: Optional[int] = Field(
        default=30,
        title="Threshold (in days)",
        description="(in days) The threshold to filter the unused log strams.")
    region: Optional[str] = Field(
        title='Region',
        description='AWS Region')


def aws_filter_unused_log_streams_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def aws_filter_unused_log_streams(handle, region: str = "", time_period_in_days: int = 30) -> Tuple:
    """aws_filter_unused_log_streams Returns an array of unused log strams for all log groups.

        :type region: string
        :param region: Used to filter the volume for specific region.
        
        :type time_period_in_days: int
        :param time_period_in_days: (in days) The threshold to filter the unused log strams.

        :rtype: Array of unused log strams for all log groups.
    """
    result = []
    now = datetime.utcnow()
    all_regions = [region]
    if not region:
        all_regions = aws_list_all_regions(handle)

    for reg in all_regions:
        try:
            start_time = now - timedelta(days=time_period_in_days)
            config = botocore.config.Config(retries={'max_attempts': 10})
            ec2Client = handle.client('logs', region_name=reg, config=config)
            response = aws_get_paginator(ec2Client, "describe_log_groups", "logGroups")
            for log_group in response:
                log_group_name = log_group['logGroupName']
                response1 = aws_get_paginator(ec2Client, "describe_log_streams", "logStreams",
                                            logGroupName=log_group_name,
                                            orderBy='LastEventTime',
                                            descending=True)

                for log_stream in response1:
                    unused_log_streams = {}
                    last_event_time = log_stream.get('lastEventTimestamp')
                    if last_event_time is None:
                        # The log stream has never logged an event
                        unused_log_streams["log_group_name"] = log_group_name
                        unused_log_streams["log_stream_name"] = log_stream['logStreamName']
                        unused_log_streams["region"] = reg
                        result.append(unused_log_streams)
                    elif datetime.fromtimestamp(last_event_time/1000.0) < start_time:
                        # The log stream has not logged an event in the past given days
                        unused_log_streams["log_group_name"] = log_group_name
                        unused_log_streams["log_stream_name"] = log_stream['logStreamName']
                        unused_log_streams["region"] = reg
                        result.append(unused_log_streams)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
