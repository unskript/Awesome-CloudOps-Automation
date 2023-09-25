##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import KafkaProducer, KafkaConsumer
from typing import Tuple
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def kafka_broker_health_check_printer(output):
    status, issues = output

    if status:
        print("All brokers are connected and healthy!")
    else:
        print("Issues detected with brokers:\n")
        for issue in issues:
            print(f"Issue Type: {issue['issue_type']}")
            print(f"Description: {issue['description']}\n")


def kafka_broker_health_check(handle) -> Tuple:
    """
    Checks the health of the Kafka brokers function by determining if the Kafka producer 
    can establish a connection with the bootstrap brokers of a Kafka cluster.

    :type handle: KafkaProducer
    :param handle: Handle containing the KafkaProducer instance.

    :rtype: Tuple containing a status and an optional list of issues with brokers.
    """

    issues = []

    # Check the brokers
    connected_to_brokers = handle.bootstrap_connected()
    if not connected_to_brokers:
        issues.append({
            'issue_type': 'Broker',
            'description': 'Unable to connect to bootstrap brokers.'
        })

    if len(issues) != 0:
        return (False, issues)
    return (True, None)

