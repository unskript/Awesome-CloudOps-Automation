##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import TopicPartition, KafkaConsumer
from typing import Dict
from pydantic import BaseModel, Field



class InputSchema(BaseModel):
    group_id: str = Field(..., description='Consumer group ID to which this consumer belongs', title='Consumer group ID')
    topics: list = Field(..., description='List of topic names.', title='List of topics')


def kafka_get_topic_health_printer(output):
    for topic_name, partitions in output.items():
        print(f"Topic: {topic_name}")
        for partition, info in partitions.items():
            print(f"  Partition {partition}: {info['number_of_messages']} messages, Topic exists: {info['topic_exists']}")
        print()


def kafka_get_topic_health(handle, group_id: str, topics: list) -> Dict:
    """
    kafka_get_topic_health fetches the health and total number of messages for the specified topics.

    :type handle: object
    :param handle: Handle containing the KafkaConsumer instance.

    :type group_id: str
    :param group_id: Consumer group ID 

    :type topics: list
    :param topics: List of topic names.

    :rtype: Dictionary containing the health status and number of messages by topic and partition
    """

    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group_id)

    topic_info = {}

    # Get all available topics
    available_topics = consumer.topics()

    for tp in topics:
        # Check if the topic exists
        if tp in available_topics:
            for partition in consumer.partitions_for_topic(tp) or []:
                tp_obj = TopicPartition(tp, partition)
                # Fetch the earliest and latest available offsets for the partition
                earliest_offset = consumer.beginning_offsets([tp_obj])[tp_obj]
                latest_offset = consumer.end_offsets([tp_obj])[tp_obj]

                # Calculate the number of messages
                number_of_messages = latest_offset - earliest_offset

                # Store the number of messages and topic existence status in the result dictionary
                topic_info.setdefault(tp, {})[partition] = {
                    "number_of_messages": number_of_messages,
                    "topic_exists": "Yes"
                }
        else:
            # If topic doesn't exist, add a special entry to indicate this
            topic_info[tp] = {
                -1: {
                    "number_of_messages": 0,
                    "topic_exists": "No"
                }
            }
    consumer.close()

    return topic_info


