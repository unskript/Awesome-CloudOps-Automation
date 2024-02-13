##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from kafka import KafkaAdminClient, KafkaConsumer, TopicPartition
from pydantic import BaseModel, Field
from tabulate import tabulate
import time



class InputSchema(BaseModel):
    group_id: Optional[str] = Field(
        '',
        description='Consumer group ID to which this consumer belongs',
        title='Consumer group ID',
    )
    threshold: Optional[int] = Field(
        3,
        description="The number of hours to check if the lag hasn't changed.",
        title='Threshold (in hours)',
    )


def kafka_check_lag_change_printer(output):
    status, issues = output

    if status:
        print("All consumer groups are maintaining their lags!")
    else:
        print("Lag issues detected:")
        headers = ['Consumer Group', 'Topic', 'Partition', 'Description']
        table_data = [(issue['consumer_group'], issue['topic'], issue['partition'], issue['description']) for issue in issues]
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

    # This would be a global or persisted store of previous lags at the last check.
    # Format: { "topic-partition": [timestamp, lag] }
prev_lags = {}

def fetch_lag(handle, group_id, topic_partitions, current_time, threshold):
    issues = []
    # Utilize bootstrap_servers from handle
    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group_id)
    try:
        for tp in topic_partitions:
            end_offset = consumer.end_offsets([tp])[tp]
            committed = consumer.committed(tp) or 0
            lag = end_offset - committed

            if lag == 0:
                continue

            key = f"{group_id}-{tp.topic}-{tp.partition}"
            prev_entry = prev_lags.get(key)

            if prev_entry:
                prev_timestamp, prev_lag = prev_entry
                if prev_lag != lag:
                    prev_lags[key] = (current_time, lag)
                elif (current_time - prev_timestamp) >= threshold * 3600:
                    issues.append({
                        'consumer_group': group_id,
                        'topic': tp.topic,
                        'partition': tp.partition,
                        'description': f"Lag hasn't changed for {threshold} hours. Current Lag: {lag}"
                    })
            else:
                prev_lags[key] = (current_time, lag)
    finally:
        consumer.close()

    return issues

def kafka_check_lag_change(handle, group_id: str = "", threshold: int = 3) -> Tuple:
    """
    kafka_check_lag_change checks if the lag for consumer groups is not changing for X hours.

    :param handle: Object of type unSkript KAFKA Connector.

    :param group_id: Consumer group ID.

    :param threshold: The number of hours to check if the lag hasn't changed.

    :return: Tuple containing a status and an optional list of issues with lag.
    """
    issues = []
    current_time = time.time()

    admin_client = KafkaAdminClient(bootstrap_servers=handle.config['bootstrap_servers'])
    consumer_groups = [group_id] if group_id else [group[0] for group in admin_client.list_consumer_groups()]

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for group in consumer_groups:
            consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group)
            topics = consumer.topics()
            topic_partitions = [TopicPartition(topic, partition) for topic in topics for partition in consumer.partitions_for_topic(topic)]
            consumer.close()

            if topic_partitions:
                future = executor.submit(fetch_lag, handle, group, topic_partitions, current_time, threshold)
                futures.append(future)

        for future in as_completed(futures):
            issues.extend(future.result())

    return (False, issues) if issues else (True, None)