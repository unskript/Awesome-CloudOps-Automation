from __future__ import annotations

##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import KafkaProducer, KafkaConsumer
from typing import Tuple
from pydantic import BaseModel



from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def kafka_topic_partition_health_check_printer(output):
    status, issues = output

    if status:
        print("All topics and partitions are healthy!")
    else:
        print("Issues detected with topics or partitions:\n")
        for issue in issues:
            print(f"Issue Type: {issue['issue_type']}")
            print(f"Description: {issue['description']}\n")


def kafka_topic_partition_health_check(handle) -> Tuple:
    """
    Checks the health of the Kafka topics and their partitions.This check checks if the topics have any partitions at all.

    :type handle: KafkaProducer
    :param handle: Handle containing the KafkaProducer instance.

    :rtype: Status, Tuple containing a status and an optional list of issues with topics and their partitions.
    """

    issues = []

    # Using KafkaConsumer to get topic details
    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'])
    for topic in consumer.topics():
        partitions = consumer.partitions_for_topic(topic)
        if not partitions or len(partitions) == 0:
            issues.append({
                'issue_type': f'Topic: {topic}',
                'description': 'No partitions available.'
            })

    consumer.close()

    if len(issues) != 0:
        return (False, issues)
    return (True, None)



