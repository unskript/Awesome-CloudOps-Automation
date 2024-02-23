##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import KafkaConsumer, TopicPartition
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from kafka.admin import KafkaAdminClient
import time



class InputSchema(BaseModel):
    group_id: Optional[str] = Field(..., description='Consumer group ID', title='Consumer group ID')
    threshold: Optional[int] = Field(
        10, description='The threshold on the difference between 2 sample sets of lag data collected.', title='Threshold (no. of messages)'
    )
    sliding_window_interval: Optional[int] = Field(
        30, description='The cadence (in seconds) at which the lag data needs to be collected', title='Sliding window interval'
    )



def kafka_get_topics_with_lag_printer(output):
    print("Topics with lag:")
    status, topics_with_lag = output
    if status:
        print("None of the topics are experiencing a lag")
    else:
        for item in topics_with_lag:
            print(f"Group '{item['group']}' | Topic '{item['topic']}' | Partition {item['partition']}: {item['lag']} lag (no. of messages)")


def kafka_get_topics_with_lag(handle, group_id: str = "", threshold: int = 10, sliding_window_interval = 30) -> Tuple:
    """
    kafka_get_topics_with_lag fetches the topics with lag in the Kafka cluster.

    :type handle: KafkaProducer
    :param handle: Handle containing the KafkaProducer instance.

    :type group_id: str
    :param group_id: Consumer group ID.

    :type threshold: int, optional
    :param threshold: Lag threshold for alerting.

    :rtype: Status and a List of objects with topics with lag information.
    """

    result = []

    admin_client = KafkaAdminClient(bootstrap_servers=handle.config['bootstrap_servers'])

    if group_id:
        consumer_groups = [group_id]
    else:
        consumer_groups = [group[0] for group in admin_client.list_consumer_groups()]

    # cached_kafka_info stores the kafka info like groups, topics, partitions.
    # Only end_offsets and committed needs to be fetched to get the latest value.
    # Its organized as groups->topics->partitions
    cached_kafka_info = {}
    # sample_data captures the snapshots for lag data. It stores for each iteration.
    # The value stored is group,topic,partition as the key and lag as the value
    sample_data = []
    sample_data_dict = {}
    for group in consumer_groups:
        consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group)
        if consumer is None:
            continue
        cached_kafka_info[group] = {'consumer': consumer}
        
        try:
            for topic in consumer.topics():
                partitions = consumer.partitions_for_topic(topic)
                cached_kafka_info[group].update({'topics': {topic:partitions}})
                for partition in partitions:
                    tp = TopicPartition(topic, partition)
                    end_offset = consumer.end_offsets([tp])[tp]
                    committed = consumer.committed(tp)
                    # Handle the case where committed is None
                    lag = end_offset - (committed if committed is not None else 0)
                    key = f'{group}:{topic}:{partition}'
                    sample_data_dict[key] = lag
        except Exception as e:
            print(f'An error occurred:{e}, group {group}')

    sample_data.append(sample_data_dict)
    # Second iteration
    time.sleep(sliding_window_interval)

    for group, value in cached_kafka_info.items():
        consumer = value.get('consumer')
        if consumer is None:
            continue
        topics = value.get('topics')
        for topic, partitions in topics.items():
            for partition in partitions:
                tp = TopicPartition(topic, partition)
                end_offset = consumer.end_offsets([tp])[tp]
                committed = consumer.committed(tp)
                # Handle the case where committed is None
                lag = end_offset - (committed if committed is not None else 0)
                key = f'{group}:{topic}:{partition}'
                sample_data_dict[key] = lag
        consumer.close()
    sample_data.append(sample_data_dict)

    for key, value in sample_data[0].items():
        # Get the value from the second sample, if present
        new_value = sample_data[1].get(key)
        if new_value is None:
            continue
        if new_value - value > threshold:
            key_split = key.split(":")
            result.append({"group": key_split[0], "topic": key_split[1], "partition": key_split[2], "incremental": new_value - value})

    if len(result) != 0:
        return (False, result)
    return (True, None)


