##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
import argparse
from typing import Tuple
from pydantic import BaseModel
from kafka_utils.kafka_check.commands.offline import OfflineCmd
from kafka_utils.util.zookeeper import ZK



pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    pass

def kafka_check_offline_partitions_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def kafka_check_offline_partitions(handle) -> Tuple:

    """kafka_check_offline_partitions Checks the number of offline partitions.

        :rtype: Tuple of the check
    """
    try:
        # Initialize the check
        check_offline_partitions = OfflineCmd()
        check_offline_partitions.cluster_config = handle.cluster_config

        # Set the arguments for running the check
        args = argparse.Namespace()
        args.verbose = True
        args.head = -1
        check_offline_partitions.args = args

        # Initialize zookeper and run the check
        with ZK(handle.cluster_config) as zk:
            check_offline_partitions.zk = zk
            check_output = check_offline_partitions.run_command()

    except Exception as e:
        raise e

    if len(check_output[1]['raw']['partitions']) != 0:
        return (False, check_output)
    return (True, check_output)
    