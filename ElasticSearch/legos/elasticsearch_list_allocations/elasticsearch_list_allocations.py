##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import subprocess
from subprocess import PIPE
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    pass


def elasticsearch_list_allocations_printer(output):
    if output is None:
        return
    print(output)


def elasticsearch_list_allocations(handle) -> str:
    """elasticsearch_list_allocations lists the allocations of an Elasticsearch cluster .

            :type handle: object
            :param handle: Object returned from Task Validate

            :rtype: Result String of result
    """

    output = handle.web_request("/_cat/allocation?v=true&pretty",  # Path
                                "GET",                        # Method
                                None)                         # Data

    return output.args