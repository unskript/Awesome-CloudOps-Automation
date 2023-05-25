##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, List
from pydantic import BaseModel, Field
from unskript.thirdparty.pingdom import swagger_client as pingdom_client

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    checkNames: Optional[List[str]] = Field(
        default=None,
        title='Check names',
        description='''Name of the checks, . Eg: ["Google", "app"]''')
    transaction: Optional[bool] = Field(
        default=False,
        title='Transaction',
        description='''Set to true if the checks are transaction checks. Default is false''')


def pingdom_get_checkids_by_name_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_get_checkids_by_name(handle, checkNames=None, transaction: bool = False) -> List[int]:
    """pingdom_get_checkids_by_name .

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type checkNames: str
        :param checkNames: Name of the checks.

        :type transaction: bool
        :param transaction: Set to true if the checks are transaction checks. Default is false.

        :rtype: list of checknames.
    """
    if checkNames is None:
        checkNames = []
    if transaction:
        check = pingdom_client.TMSChecksApi(api_client=handle)
        result = check.get_all_checks_with_http_info(_return_http_data_only=True)
        res = result.checks
        if checkNames:
            res = [check.id for check in res if check.name in checkNames]
        else:
            res = [check.id for check in res]

    else:
        check = pingdom_client.ChecksApi(api_client=handle)
        result = check.checks_get_with_http_info(_return_http_data_only=True)
        res = result.checks
        if checkNames:
            res = [check.id for check in res if check.name in checkNames]
        else:
            res = [check.id for check in res]

    return res
