##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel
from kafka import KafkaProducer


class InputSchema(BaseModel):
    pass


def kafka_get_handle(handle) -> KafkaProducer:
    """kafka_get_handle returns the kafka producer client handle.

       :rtype: kafka client handle.
    """
    return handle
