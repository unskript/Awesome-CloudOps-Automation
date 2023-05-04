##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from urllib.parse import urlparse
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session

class InputSchema(BaseModel):
    alarm_name: str = Field(
        title="Alarm name",
        description="Cloudwatch alarm name.",
    )
    region: str = Field(
        title="Region",
        description="AWS Region of the cloudwatch.")
    url: str = Field(
        title="URL",
        description=("URL where the alarm notification needs to be sent. "
                     "URL should start with http or https.")


def aws_cloudwatch_attach_webhook_notification_to_alarm_printer(output):
    if output is None:
        return
    pprint.pprint({"Subscription ARN" : output})


def aws_cloudwatch_attach_webhook_notification_to_alarm(
    hdl: Session,
    alarm_name: str,
    region: str,
    url: str
) -> str:
    """aws_cloudwatch_attach_webhook_notification_to_alarm returns subscriptionArn

        :type alarm_name: string
        :param alarm_name: Cloudwatch alarm name.

        :type url: string
        :param url: URL where the alarm notification needs to be sent.

        :type region: string
        :param region: AWS Region of the cloudwatch.

        :rtype: Returns subscriptionArn
    """
    cloudwatchClient = hdl.client("cloudwatch", region_name=region)

    # Get the configured SNS(es) to this alarm.
    alarmDetail = cloudwatchClient.describe_alarms(
        AlarmNames=[alarm_name]
    )
    if alarmDetail is None:
        return f'Alarm {alarm_name} not found in AWS region {region}'
    # Need to get the AlarmActions from either composite or metric field.
    if len(alarmDetail['CompositeAlarms']) > 0:
        snses = alarmDetail['CompositeAlarms'][0]['AlarmActions']
    else:
        snses = alarmDetail['MetricAlarms'][0]['AlarmActions']

    #Pick any sns to configure the url endpoint.
    if len(snses) == 0:
        return f'No SNS configured for alarm {alarm_name}'

    snsArn = snses[0]
    print(f'Configuring url endpoint on SNS {snsArn}')

    snsClient = hdl.client('sns', region_name=region)
    # Figure out the protocol from the url
    try:
        parsedURL = urlparse(url)
    except Exception as e:
        print(f'Invalid URL {url}, {e}')
        raise e

    if parsedURL.scheme != 'http' and parsedURL.scheme != 'https':
        return f'Invalid URL {url}'

    protocol = parsedURL.scheme
    try:
       response = snsClient.subscribe(
            TopicArn=snsArn,
            Protocol=protocol,
            Endpoint=url,
            ReturnSubscriptionArn=True)
    except Exception as e:
        print(f'Subscribe to SNS topic arn {snsArn} failed, {e}')
        raise e
    subscriptionArn = response['SubscriptionArn']
    print(f'URL {url} subscribed to SNS {snsArn}, subscription ARN {subscriptionArn}')
    return subscriptionArn
