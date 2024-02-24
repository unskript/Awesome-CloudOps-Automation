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
        # Fetch all consumer groups
        try:
            consumer_groups_info = admin_client.list_consumer_groups()
        except Exception as e:
            print(f"An error occured while fetching consumer groups:{e}")
            return {}
        consumer_groups = [group[0] for group in consumer_groups_info]
    

        for group in consumer_groups:
            # Create a consumer for each group to fetch topics
            consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group)
            try:
                topics = consumer.topics()
            except Exception as e:
                print(f"An error occurred while fetching topics in consumer group {group} : {e}")
                continue
            
            for topic in topics:
                try:
                    partitions = consumer.partitions_for_topic(topic)
                except Exception as e:
                    print(f"An error occurred while fetching partitions for {topic} : {e}")
                    continue
                for partition in partitions:
                    tp = TopicPartition(topic, partition)
                    # Fetch committed offset for each partition
                    committed_offset = consumer.committed(tp)
                    if committed_offset is not None:
                        # If there's a committed offset, calculate the number of messages
                        earliest_offset = consumer.beginning_offsets([tp])[tp]
                        number_of_messages = committed_offset - earliest_offset
                        committed_messages_count.setdefault(group, {}).setdefault(topic, {})[partition] = number_of_messages
                    else:
                        # If no committed offset, assume 0 messages
                        committed_messages_count.setdefault(group, {}).setdefault(topic, {})[partition] = 0

            # Close the consumer after processing to free up resources
            consumer.close()
    

    return committed_messages_count
