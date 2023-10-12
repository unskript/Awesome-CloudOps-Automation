##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple, Optional
from kafka.admin import KafkaAdminClient
from kafka import KafkaConsumer, TopicPartition
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

# This would be a global or persisted store of previous lags at the last check.
# Format: { "topic-partition": [timestamp, lag] }
prev_lags = {}


def kafka_check_lag_change_printer(output):
    status, issues = output

    if status:
        print("All consumer groups are maintaining their lags!")
    else:
        print("Lag issues detected:")
        headers = ['Consumer Group', 'Topic', 'Partition', 'Description']
        table_data = [(issue['consumer_group'], issue['topic'], issue['partition'], issue['description']) for issue in issues]
        print(tabulate(table_data, headers=headers, tablefmt='grid'))


def kafka_check_lag_change(handle, group_id: str= "", threshold: int=1) -> Tuple:
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

    if group_id:
        consumer_groups = [group_id]
    else:
        consumer_groups = [group[0] for group in admin_client.list_consumer_groups()]

    for group in consumer_groups:
        consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group)

        for topic in consumer.topics():
            partitions = consumer.partitions_for_topic(topic)
            for partition in partitions:
                tp = TopicPartition(topic, partition)
                end_offset = consumer.end_offsets([tp])[tp]
                committed = consumer.committed(tp) or 0
                lag = end_offset - committed

                if lag == 0:
                    continue

                key = f"{group}-{topic}-{partition}"
                if key in prev_lags:
                    prev_timestamp, prev_lag = prev_lags[key]

                    # Only update timestamp in prev_lags if there's a change in the lag
                    if prev_lag != lag:
                        prev_lags[key] = (current_time, lag)
                    elif (current_time - prev_timestamp) >= threshold * 3600:
                        print(f"Issue detected with {key}. Adding to issues list.")
                        issues.append({
                            'consumer_group': group,
                            'topic': topic,
                            'partition': partition,
                            'description': f"Lag hasn't changed for {threshold} hours. Current Lag: {lag}"
                        })
                else:
                    prev_lags[key] = (current_time, lag)

        consumer.close()

    if issues:
        return (False, issues)
    return (True, None)



