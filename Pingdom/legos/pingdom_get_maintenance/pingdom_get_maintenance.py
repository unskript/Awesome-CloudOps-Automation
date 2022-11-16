##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Dict
from unskript.thirdparty.pingdom import swagger_client as pingdom_client
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    limit: Optional[int] = Field(
        title='Number of Results',
        description='Number of Results to return')
    offset: Optional[int] = Field(
        title="Offset",
        description='Offset of the list')
    order: Optional[str] = Field(
        'asc',
        title="Order",
        description="Display ascending/descending order. Possible values: asc, desc. NOTE: This needs to specify Order By field")
    orderby: Optional[str] = Field(
        'description',
        title="Order By",
        description="Order by the specific property. Eg: description"
    )


def pingdom_get_maintenance_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def pingdom_get_maintenance(handle, limit: int = 0, offset: int = 0, order: str = 'asc',
                            orderby: str = 'description') -> Dict:
    """pingdom_get_maintenance Returns a list of Maintenance Windows
        
        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type limit: int
        :param limit: Number of returned checks.

        :type  offset int
        :param offset: Offset of returned checks.

        :type order: str
        :param order: Display ascending/descending order.

        :type orderby: str
        :param orderby:Order by the specific property.


        :rtype: Returns the list of maintenance windows
    """
    check = pingdom_client.MaintenanceApi(api_client=handle)
    result = check.maintenance_get_with_http_info(_return_http_data_only=True, order=order, orderby=orderby,
                                                  limit=limit if limit != None else None,
                                                  offset=offset if offset != None else None)
    return result
