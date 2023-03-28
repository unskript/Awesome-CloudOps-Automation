##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from kafka_utils.kafka_check.commands.replica_unavailability import ReplicaUnavailabilityCmd
from kafka_utils.util.zookeeper import ZK
from pydantic import BaseModel, Field
from typing import Dict
import pprint
import argparse


pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    pass

def kafka_check_replicas_available_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def kafka_check_replicas_available(handle) -> Dict:
    
    """kafka_check_replicas_available Checks if the number of replicas not available for communication is equal to zero.

        :rtype: Dict
    """
    try:
        # Initialize the check
        check_replica_unavailability = ReplicaUnavailabilityCmd()
        check_replica_unavailability.cluster_config = handle.cluster_config

        # Set the arguments for running the check
        args = argparse.Namespace()
        args.verbose = True
        args.head = -1
        check_replica_unavailability.args = args

        # Initialize zookeper and run the check
        with ZK(handle.cluster_config) as zk:
            check_replica_unavailability.zk = zk
            check_output = check_replica_unavailability.run_command()

    except Exception as e:
        raise e

    return check_output[1]
