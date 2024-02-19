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
        5, description='The cadence (in seconds) at which the lag data needs to be collected', title='Sliding window interval'
    )



def kafka_get_topics_with_lag_printer(output):
    print("Topics with lag:")
    status, topics_with_lag = output
    if status:
        print("None of the topics are experiencing a lag")
    else:
        for item in topics_with_lag:
            print(f"Group '{item['group']}' | Topic '{item['topic']}' | Partition {item['partition']}: {item['lag']} lag (no. of messages)")


def kafka_get_topics_with_lag(handle, group_id: str = "", threshold: int = 10, sliding_window_interval = 5) -> Tuple:
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

    admin_client = KafkaAdminClient(bootstrap_servers=handle.config['bootstrap_servers'])
    consumer_groups = [group_id] if group_id else [group[0] for group in admin_client.list_consumer_groups()]

    # Fetch topics and partitions once and reuse, to minimize network calls
    global_consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'])
    all_topics_partitions = {topic: list(global_consumer.partitions_for_topic(topic)) for topic in global_consumer.topics()}
    global_consumer.close()

    consumer_config = {
        'bootstrap_servers': handle.config['bootstrap_servers'],
        'fetch_min_bytes': 100000, 
        'fetch_max_wait_ms': 500,  
        'session_timeout_ms': 10000,
        'heartbeat_interval_ms': 3000,
        'max_partition_fetch_bytes': 2 * 1048576
    }
    # sample_data captures the snapshots for lag data. It stores for each iteration.
    # The value stored is group,topic,partition as the key and lag as the value
    sample_data = []
    # Since we need to collect 2 sample sets for now, we do it in a loop
    for i in range(2):
        sample_data_dict = {}
        for group in consumer_groups:
            consumer = KafkaConsumer(group_id=group, **consumer_config)
            try:
                # Use cached topics and partitions to reduce network calls
                for topic, partitions in all_topics_partitions.items():
                    for partition in partitions:
                        tp = TopicPartition(topic, partition)
                        end_offset = consumer.end_offsets([tp])[tp]
                        committed = consumer.committed(tp)
                        lag = end_offset - (committed if committed is not None else 0)
                        key = f'{group}:{topic}:{partition}'
                        sample_data_dict[key] = lag
            except Exception as e:
                raise e
            finally:
                consumer.close()
        sample_data.append(sample_data_dict)
        if i == 0:
            time.sleep(sliding_window_interval)

    result = []
    for key, initial_value in sample_data[0].items():
        final_value = sample_data[1].get(key, initial_value)  # Default to initial if not found in second sample
        if final_value - initial_value > threshold:
            group, topic, partition = key.split(":")
            result.append({
                "group": group,
                "topic": topic,
                "partition": int(partition),
                "lag": final_value - initial_value
            })

    return (False, result) if result else (True, None)