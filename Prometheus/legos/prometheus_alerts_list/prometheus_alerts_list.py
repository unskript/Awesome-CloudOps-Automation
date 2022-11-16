##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import List
from tabulate import tabulate
from pydantic import BaseModel

lego_title="Get All Prometheus Alerts"
lego_description="Get All Prometheus Alerts"
lego_type="LEGO_TYPE_PROMETHEUS"


class InputSchema(BaseModel):
    pass


def prometheus_alerts_list_printer(output):
    if output is None:
        return
    alerts = []
    for alert in output:
        for key, value in alert.items():
            alerts.append([key, value])
    print("\n")
    print(tabulate(alerts))



def prometheus_alerts_list(handle) -> List[dict]:
  """prometheus_alerts_list Returns all alerts.

    :type handle: object
    :param handle: Object returned from task.validate(...).

    :return: Alerts list.
  """
  try:
      params = {
          "type": "alert"
      }
      response = handle.all_alerts(params)
  except Exception as e:
      print(f'Alerts failed,  {e.__str__()}')
      return [{"error": e.__str__()}]

  result = []

  if len(response['groups']) != 0:
    for rules in response['groups']:
        for rule in rules['rules']:
            res = {}
            res['name'] = rule['name']
            result.append(res)
  return result
