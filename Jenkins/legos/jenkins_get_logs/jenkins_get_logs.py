##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict, Optional
from pydantic import BaseModel, Field



class InputSchema(BaseModel):
    job_name: str = Field(
        title='Job Name',
        description='Jenkins job name.')
    build_number: Optional[int] = Field(
        0,
        title='Build Number',
        description='Specific build number of the job. By default, it gets the last build logs.')


def jenkins_get_logs_printer(output):
    if output is None:
        return
    pprint.pprint({output})


def jenkins_get_logs(handle, job_name: str, build_number: int = 0) -> Dict:
    """jenkins_get_logs returns logs for the particular job name.

        :type job_name: string
        :param job_name: Jenkins job name.

        :type build_number: int
        :param build_number: Specific build number of the job. 
        By default, it gets the last build logs.

        :rtype: Dict with builds number and logs.
    """

    # Input param validation.
    job = handle.get_job(job_name)

    if build_number == 0:
        res = job.get_last_build()
        return res.get_console()

    res = job.get_build(build_number)
    return res.get_console()
