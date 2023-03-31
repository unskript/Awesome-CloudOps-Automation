##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from kafka_utils.kafka_check.commands.min_isr import MinIsrCmd
from kafka_utils.util.zookeeper import ZK
from pydantic import BaseModel, Field
from typing import Dict
import pprint
import argparse


pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    min_isr: int = Field(
        3,
        title='Minimum In-Sync Replicas',
        description='Default min.isr value for cases without settings in Zookeeper. The default value is 3'
    )


def kafka_check_in_sync_replicas_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def kafka_check_in_sync_replicas(handle, min_isr: int) -> Dict:
    
    """kafka_check_in_sync_replicas checks number of actual min-isr for each topic-partition with configuration for that topic.

        :type min_isr: int
        :param min_isr: Default min.isr value for cases without settings in Zookeeper. The default value is 3.

        :rtype: Dict
    """
    try:
        # Initialize the check
        check_in_sync_replicas = MinIsrCmd()
        check_in_sync_replicas.cluster_config = handle.cluster_config

        # Set the arguments for running the check
        args = argparse.Namespace()
        args.default_min_isr = min_isr
        args.verbose = True
        args.head = -1
        check_in_sync_replicas.args = args

        # Initialize zookeper and run the check
        with ZK(handle.cluster_config) as zk:
            check_in_sync_replicas.zk = zk
            check_output = check_in_sync_replicas.run_command()

    except Exception as e:
        raise e

    return check_output[1]
