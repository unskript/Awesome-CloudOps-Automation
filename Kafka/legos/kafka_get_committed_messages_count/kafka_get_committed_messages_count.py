##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import TopicPartition
from kafka import KafkaConsumer
from typing import Dict
from pydantic import BaseModel, Field



from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    group_id: str = Field(..., description='Consumer group ID to which this consumer belongs', title='Consumer group ID')



def kafka_get_committed_messages_count_printer(output):
    if output is None:
        return

    for group_id, topics in output.items():
        print(f"Group ID: {group_id}")
        for topic_name, partitions in topics.items():
            print(f"  Topic: {topic_name}")
            for partition, number_of_messages in partitions.items():
                print(f"    Partition {partition}: {number_of_messages} committed messages")
        print()

def kafka_get_committed_messages_count(handle, group_id: str) -> Dict:
    """
    kafka_get_committed_messages_count Fetches committed messages (consumer offsets) for a specific consumer group and topics, or all topics if none are specified.

    :type handle: object
    :param handle: Handle containing the KafkaConsumer instance.

    :type group_id: str
    :param group_id: Consumer group ID 

    :rtype: Dictionary of committed messages by consumer group, topic, and partition
    """

    # Create KafkaConsumer with the configuration
    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group_id)

    committed_messages_count = {}

    # Get all topic subscriptions for the consumer group
    topics = list(consumer.topics())

    for tp in topics:
        for partition in consumer.partitions_for_topic(tp):
            tp_obj = TopicPartition(tp, partition)
            # Fetch the committed offset for the partition
            committed_offset = consumer.committed(tp_obj)
            # Fetch the earliest available offset for the partition
            earliest_offset = consumer.beginning_offsets([tp_obj])[tp_obj]

            # If committed offset is not None, calculate the number of committed messages
            if committed_offset is not None:
                number_of_messages = committed_offset - earliest_offset
            else:
                number_of_messages = 0

            # Store the number of committed messages in the result dictionary
            committed_messages_count.setdefault(group_id, {}).setdefault(tp, {})[partition] = number_of_messages

    # Close the consumer connection
    consumer.close()

    return committed_messages_count


