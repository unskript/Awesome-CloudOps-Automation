##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import KafkaProducer, KafkaConsumer
from typing import Dict
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


def kafka_get_cluster_health(handle: KafkaProducer) -> Dict:
    """
    kafka_get_cluster_health fetches the health of the Kafka cluster including brokers, topics, and partitions.

    :type handle: KafkaProducer
    :param handle: Handle containing the KafkaProducer instance.

    :rtype: Dictionary containing the brokers, topics, and partitions.
    """

    result = []

    # Check the brokers
    connected_to_brokers = handle.bootstrap_connected()
    if not connected_to_brokers:
        result.append({
            'issue_type': 'Broker',
            'description': 'Unable to connect to bootstrap brokers.'
        })

    # Now, using KafkaConsumer to get topic details
    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'])
    for topic in consumer.topics():
        partitions = consumer.partitions_for_topic(topic)
        if not partitions or len(partitions) == 0:
            result.append({
                'issue_type': f'Topic: {topic}',
                'description': 'No partitions available.'
            })

    consumer.close()

    if result:
        return (False, result)
    return (True, None)

def kafka_get_cluster_health_printer(output):
    status, issues = output

    if status:
        print("Kafka cluster is healthy!")
    else:
        print("Issues detected in the Kafka cluster:\n")
        for issue in issues:
            print(f"Issue Type: {issue['issue_type']}")
            print(f"Description: {issue['description']}\n")
