##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel
import pprint

class InputSchema(BaseModel):
    pass

def nomad_list_jobs_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def nomad_list_jobs(handle):
    """nomad_list_jobs returns the nomad jobs.

        :type handle: object
        :param handle: Object returned from task.validate(...).

          :rtype: List of Nomad jobs.
    """
    result = handle.jobs.get_jobs()
    return result
