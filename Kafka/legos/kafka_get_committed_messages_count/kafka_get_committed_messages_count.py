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

    try:
        if group_id:
            consumer_groups = [group_id]
        else:
            consumer_groups_info = admin_client.list_consumer_groups()
            consumer_groups = [group[0] for group in consumer_groups_info]
    except Exception as e:
        print(f"Failed to list consumer groups: {e}")
        return {}

    for group in consumer_groups:
        with KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group) as consumer:
            topics = consumer.topics()

            for topic in topics:
                partitions = consumer.partitions_for_topic(topic)

                for partition in partitions:
                    try:
                        tp = TopicPartition(topic, partition)
                        committed_offset = consumer.committed(tp)
                        earliest_offset = consumer.beginning_offsets([tp])[tp]
                        number_of_messages = committed_offset - earliest_offset if committed_offset is not None else 0
                        committed_messages_count.setdefault(group, {}).setdefault(topic, {})[partition] = number_of_messages
                    except Exception as e:
                        print(f"Failed to fetch offsets for partition {partition} of topic {topic} in group {group}: {e}")
                        continue


    return committed_messages_count

