##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
from typing import Dict
import matplotlib.pyplot as plt
#from pymongo.errors import *

from pydantic import BaseModel
from Mongo.legos.mongodb_util import reachable


class InputSchema(BaseModel):
    pass


def plotData(output, keywords):
    plt.figure(figsize=(24,20), dpi=80)
    row = 0
    col = 0
    for idx, keyword in enumerate(keywords):
        data = output.get(keyword)
        names = list(data.keys())
        values = list(data.values())
        plot = plt.subplot2grid((3,4), (row, col), colspan=1, rowspan=1)
        plot.bar(range(len(data)), values, tick_label=names)
        plot.set_title(keyword)
        col += 1
        if idx % 2:
            row += 1
            col = 0

    plt.show()


def mongodb_get_server_status_printer(output):
    print("Uptime (seconds): ", output.get('uptime'))
    print("UptimeEstimate (seconds): ", output.get('uptimeEstimate'))
    print("Version: ", output.get('version'))
    print("PID : ", output.get('pid'))
    print("Process : ", output.get('process'))
    print("Host : ", output.get('host'))
    print("Local Time: ", output.get('localTime'))

    plotData(output, ['asserts', 'connections', 'mem', 'opcounters'])


def mongodb_get_server_status(handle) -> Dict:
    """mongodb_get_server_status returns the mongo server status.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method

        :rtype: Dict containg server status.
    """
    # Check the MongoDB
    try:
        reachable(handle)
    except Exception as e:
        raise e

    # Result will store output from handle.admin.command(...)
    # We will use this
    result = {}
    try:
        result = handle.admin.command("serverStatus")
    except Exception as e:
        raise e

    return result
