##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import KafkaConsumer, TopicPartition, KafkaAdminClient
from typing import Dict, Optional
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    group_id: Optional[str] = Field(..., description='Consumer group ID to which this consumer belongs', title='Consumer group ID')



def kafka_get_committed_messages_count_printer(output):
    if output is None:
        print("No data found to get kafka committed messages count ! ")
        return

    for group_id, topics in output.items():
        print(f"Group ID: {group_id}")
        for topic_name, partitions in topics.items():
            print(f"  Topic: {topic_name}")
            for partition, number_of_messages in partitions.items():
                print(f"    Partition {partition}: {number_of_messages} committed messages")
        print()

def kafka_get_committed_messages_count(handle, group_id: str = "") -> Dict:
    """
    Fetches committed messages (consumer offsets) for all consumer groups and topics,
    or for a specific group if provided.
    """
    admin_client = KafkaAdminClient(bootstrap_servers=handle.config['bootstrap_servers'])
    committed_messages_count = {}

    if group_id:
        consumer_groups = [group_id]
    else:
        consumer_groups = [group[0] for group in admin_client.list_consumer_groups()]

    # Prepare a cache for Kafka info to minimize calls
    cached_kafka_info = {}

    # Iterate once to fetch and cache required info
    for group in consumer_groups:
        consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group)
        topics = consumer.topics()
        cached_kafka_info[group] = {'consumer': consumer, 'topics': {}}

        for topic in topics:
            partitions = consumer.partitions_for_topic(topic)
            cached_kafka_info[group]['topics'][topic] = partitions

            for partition in partitions:
                tp = TopicPartition(topic, partition)
                committed_offset = consumer.committed(tp)
                earliest_offset = consumer.beginning_offsets([tp])[tp]
                number_of_messages = committed_offset - earliest_offset if committed_offset is not None else 0
                committed_messages_count.setdefault(group, {}).setdefault(topic, {})[partition] = number_of_messages

        # Close the consumer to free up resources
        consumer.close()

    return committed_messages_count

