##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel

pp = pprint.PrettyPrinter()

class InputSchema(BaseModel):
    pass


def hadoop_get_cluster_metrics_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def hadoop_get_cluster_metrics(handle) -> Dict:
    """hadoop_get_cluster_metrics returns the cluster matrics.
       :rtype: cluster matrics.
    """
    return handle.get_cluster_metrics()
