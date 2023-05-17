##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Optional, Dict
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter()

class InputSchema(BaseModel):
    appid: Optional[str] = Field(
        title='Application id',
        description='The application id'
    )


def hadoop_get_cluster_apps_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def hadoop_get_cluster_apps(handle, appid: str = "") -> Dict:
    """hadoop_get_cluster_apps get cluster apps

        :type appid: str
        :param appid: The application id.

        :rtype: Dict of cluster apps
    """
    return handle.get_cluster_apps(appid = appid if appid else None)
