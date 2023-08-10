##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from kafka import KafkaConsumer, TopicPartition
from typing import Optional, Tuple
from pydantic import BaseModel, Field




class InputSchema(BaseModel):
    group_id: str = Field(..., description='Consumer group ID', title='Consumer group ID')
    threshold: Optional[int] = Field(
        2, description='Lag threshold for alerting.', title='Threshold (no. of messages)'
    )



def kafka_get_topics_with_lag_printer(output):
    print("Topics with lag:")
    status, topics_with_lag = output
    if status:
        print("None of the topics are experiencing a lag")
    else:
        for item in topics_with_lag:
            print(f"Topic '{item['topic']}'\n Partition {item['partition']}: {item['lag']} lag (no. of messages)")


def kafka_get_topics_with_lag(handle, group_id: str, threshold: int = 2) -> Tuple:
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

    consumer = KafkaConsumer(bootstrap_servers=handle.config['bootstrap_servers'], group_id=group_id)

    try:
        for topic in consumer.topics():
            partitions = consumer.partitions_for_topic(topic)
            for partition in partitions:
                tp = TopicPartition(topic, partition)
                end_offset = consumer.end_offsets([tp])[tp]
                committed = consumer.committed(tp)
                # If condition handles the case where committed is None
                lag = end_offset - (committed if committed is not None else 0)
                if lag > threshold:
                    result.append({"topic": topic, "partition": partition, "lag": lag})
    except Exception as e:
        print("An error occurred:", e)
    finally:
        consumer.close()
        
    if len(result) != 0:
        return (False, result)
    return (True, None)


