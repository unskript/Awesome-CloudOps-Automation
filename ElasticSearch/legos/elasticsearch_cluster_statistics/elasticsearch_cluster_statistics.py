##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
import pprint
from pydantic import BaseModel, Field
from typing import List, Dict
from subprocess import PIPE, run
import json
import matplotlib.pyplot as plt
import pandas as pd


class InputSchema(BaseModel):
    pass


def plotData(output, keywords, docs, shards):
    plot1 = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
    plot2 = plt.subplot2grid((3, 3), (0, 2), colspan=2, rowspan=2)
    for idx, keyword in enumerate(keywords):
        data = output.get(keyword)
        names = list(data.keys())
        values = list(data.values())
        plot1.bar(range(len(data)), values, tick_label=names)
        plot1.set_title("Nodes")
    for i in docs:
        x = list(docs.keys())
        y = list(docs.values())
        plot2.set_title("Docs")
        plot2.bar(range(len(x)), y, tick_label=x)
    plot2.set_xticklabels(x)
    plot2.set_yticklabels([])
    plot2.bar_label(plot2.containers[0], label_type='center')
    df = pd.DataFrame(shards)
    df.plot(kind="bar", stacked=True, title="Shards")
    plt.show()


def elasticsearch_cluster_statistics_printer(output):
    if output is None:
        return
    print("Cluster Name: ", output.get('cluster_name'))
    print("Timestamp: ", output.get('timestamp'))
    print("Status: ", output.get('status'))
    for k, v in output.items():
        if k == 'indices':
            shards = output['indices']['shards']['index']
            docs = output['indices']['docs']

    plotData(output, ['_nodes'], docs, shards)


def elasticsearch_cluster_statistics(handle) -> str:
    """elasticsearch_cluster_statistics fetches basic index metrics and information about the current nodes that form the cluster.
            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result Dict of result
    """
  
    output = handle.web_request("/_cluster/stats?human&pretty&pretty",  # Path
                                "GET",                      # Method
                                None)                       # Data

    return output.args
