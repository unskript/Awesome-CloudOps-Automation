##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import json

import pprint
from typing import Optional, List
from yaml import load

from pydantic import BaseModel, Field

from unskript.connectors.grafana import Grafana

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    dashboard_id: Optional[int] = Field(
        None,
        title='Dashboard ID',
        description='ID of the dashboard to limit the alerts within that dashboard.')
    panel_id: Optional[int] = Field(
        None,
        title='Panel ID',
        description='Panel ID to limit the alerts within that Panel.')


def grafana_list_alerts_printer(output):
    if output is None:
        return
    print('\n')
    pprint.pprint(output)


def grafana_list_alerts(handle: Grafana, dashboard_id:int = None,
                           panel_id:int = None) -> List[dict]:
    """grafana_list_alerts lists the configured alerts in grafana.
       You can filter alerts configured in a particular dashboard.

       :type dashboard_id: int
       :param dashboard_id: ID of the grafana dashboard.

       :type panel_id: int
       :param panel_id: Panel ID to limit the alerts within that Panel.

       :rtype: List of alerts.
    """
    url = handle.host + "/api/ruler/grafana/api/v1/rules"
    if dashboard_id or panel_id:
        param = {}
        if dashboard_id:
            param["DashboardUID"] = dashboard_id
        if panel_id:
            param["PanelID"] = panel_id
        response = handle.session.get(url,
                                      params=param)
    else:
        response = handle.session.get(url)

    result = []
    folder_names = json.loads(response.content).keys()
    for folder_name in list(folder_names):
        for alarm in json.loads(response.content)[folder_name]:
            res = {}
            res['id'] = alarm['rules'][0]['grafana_alert']['id']
            res['name'] = alarm['name']
            result.append(res)
    # Get Loki alerts as well.
    if handle.lokiURL != None:
        url = handle.lokiHost + "loki/api/v1/rules"
        response = handle.lokiSession.get(url)
        lokiAlerts = []
        responseDict = load(response.content)
        folder_names = responseDict.keys()
        for folder_name in list(folder_names):
            for alarm in responseDict[folder_name]:
                res = {}
                for rule in alarm['rules']:
                   # Loki have 'alert' in the key, where as recorded loki has 'record' as the key.
                   if 'alert' in rule:
                    res['name'] = rule['alert']
                   else:
                    res['name'] = rule['record']
                result.append(res)

    return result
