##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import TopicPartition, KafkaConsumer, KafkaAdminClient
from typing import Dict, Optional
from pydantic import BaseModel, Field



class InputSchema(BaseModel):
    group_id: Optional[str] = Field(..., description='Consumer group ID to which this consumer belongs', title='Consumer group ID')
    topics: Optional[list] = Field(..., description='List of topic names.', title='List of topics')


def kafka_get_topic_health_printer(output):
    if output is None:
        print("No data found for the Kafka topic health!")
        return
    
    # Iterating through each group in the output
    for group_id, topics in output.items():
        print(f"Group ID: {group_id}")
        # Iterating through each topic in the group
        for topic_name, partitions in topics.items():
            print(f"  Topic: {topic_name}")
            # Iterating through each partition in the topic
            for partition, info in partitions.items():
                # Checking if the topic exists flag is true or false to print accordingly
                topic_exists_msg = "Yes" if info["topic_exists"] else "No"
                print(f"    Partition {partition}: {info['number_of_messages']} messages, Topic exists: {topic_exists_msg}")
        print()


def kafka_get_topic_health(handle, group_id: str="", topics: list=[]) -> Dict:
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


    admin_client = KafkaAdminClient(bootstrap_servers=handle.config['bootstrap_servers'])

    topic_health_info = {}

    try:
        if not group_id:
            consumer_groups_info = admin_client.list_consumer_groups()
            consumer_groups = [group[0] for group in consumer_groups_info]
        else:
            consumer_groups = [group_id]
    except Exception as e:
        print(f"Failed to list consumer groups: {e}")
        return {}

    for group in consumer_groups:
        consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group)
        group_topics = topics if topics else list(consumer.topics())

        for topic in group_topics:
            partitions = consumer.partitions_for_topic(topic)
            if not partitions:
                topic_health_info.setdefault(group, {})[topic] = {"-1": {"number_of_messages": 0, "topic_exists": False}}
                continue

            for partition in partitions:
                try:
                    tp = TopicPartition(topic, partition)
                    earliest_offset = consumer.beginning_offsets([tp])[tp]
                    latest_offset = consumer.end_offsets([tp])[tp]
                    number_of_messages = latest_offset - earliest_offset
                except Exception as e:
                    print(f"Failed to fetch offsets for partition {partition} of topic {topic} in group {group}: {e}")
                    continue

                topic_health_info.setdefault(group, {}).setdefault(topic, {})[partition] = {
                    "number_of_messages": number_of_messages,
                    "topic_exists": True
                }
        
        consumer.close()
    
    return topic_health_info