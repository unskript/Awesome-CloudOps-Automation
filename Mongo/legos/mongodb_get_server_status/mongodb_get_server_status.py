##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel
from tabulate import tabulate


class InputSchema(BaseModel):
    pass


def mongodb_get_server_status_printer(output):
    if output is None:
        return

    essential_metrics = ['version', 'uptime', 'localTime', 'connections', 'extra_info', 'asserts', 'opcounters']
    pretty_output = []

    for metric in essential_metrics:
        if metric in output:
            if type(output[metric]) is dict:
                for submetric, value in output[metric].items():
                    pretty_output.append([f"{metric}.{submetric}", str(value)])
            else:
                pretty_output.append([metric, str(output[metric])])

    print("\n")
    print(tabulate(pretty_output, headers=['Metric', 'Value'], tablefmt='fancy_grid'))
    return output


def mongodb_get_server_status(handle) -> Dict:
    """mongodb_get_server_status returns the mongo server status.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :rtype: Dict with server status.
    """
    try:
        res = handle.admin.command("serverStatus")
        return res
    except Exception as e:
        return {"Error": e}
