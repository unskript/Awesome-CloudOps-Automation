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

    cluster_health = {}

    # Get the list of available brokers
    cluster_health['brokers'] = handle.bootstrap_connected()


    # Now, using KafkaConsumer to get topic details
    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'])
    topics_details_consumer = {}
    for topic in consumer.topics(): # Notice the parentheses here
        partitions = consumer.partitions_for_topic(topic)
        topics_details_consumer[topic] = {
            "partitions": len(partitions),
        }

    consumer.close()

    # Adding the details from consumer to cluster health
    cluster_health["topics"] = topics_details_consumer

    return cluster_health

def kafka_get_cluster_health_printer(cluster_health: Dict):
    print("Brokers available:", cluster_health['brokers'])
    print("\nTopics:")
    for topic, details in cluster_health["topics"].items():
        print(f"  {topic}: {details['partitions']} partitions")
