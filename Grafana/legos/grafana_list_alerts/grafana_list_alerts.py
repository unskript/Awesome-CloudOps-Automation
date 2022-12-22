##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import json

import pprint
from typing import Optional, List

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
    params = None
    if dashboard_id or panel_id:
        param = {}
        if dashboard_id:
            param["DashboardUID"] = dashboard_id
        if panel_id:
            param["PanelID"] = panel_id
        params = param

    response = handle.session.get(url,
                                 params=params)

    result = []
    folder_names = json.loads(response.content).keys()
    for folder_name in list(folder_names):
        for alarm in json.loads(response.content)[folder_name]:
            res = {}
            res['id'] = alarm['rules'][0]['grafana_alert']['id']
            res['name'] = alarm['name']
            result.append(res)
    # Get Loki alerts as well.
    # First get the datasources which has type Loki.
    url = handle.host + "/api/datasources"
    try:
        response = handle.session.get(url)
        response.raise_for_status()
    except Exception as e:
        # This could happen because in non-cloud grafana, there is no rbac, so this api doesnt work with viewer role.
        print("Unable to get datasources")
        return result

    try:
        datasourcesList = json.loads(response.content)
    except Exception as e:
        print(f'Unable to parse datasources response, error {str(e)}')
        return result

    lokiDatasourcesList = []
    for datasource in datasourcesList:
        if datasource["type"] == "loki":
            lokiDatasourcesList.append(datasource["uid"])

    for lokiDatasourceUID in lokiDatasourcesList:
        url = handle.host + "/api/ruler/" + lokiDatasourceUID + "/api/v1/rules"
        try:
            response = handle.session.get(url, params=params)
            response.raise_for_status()
        except Exception as e:
            print(f'Failed to get rules for datasource uid {lokiDatasourceUID}, error {str(e)}')
            continue

        try:
            responseDict = json.loads(response.content)
        except Exception as e:
            print(f'Unable to parse rules response, uid {lokiDatasourceUID}, error {str(e)}')
            continue

        folder_names = responseDict.keys()
        for folder_name in list(folder_names):
            for alarm in responseDict[folder_name]:
                for rule in alarm['rules']:
                    res = {}
                    # Loki have 'alert' in the key, where as recorded loki has 'record' as the key.
                    if 'alert' in rule:
                        res['name'] = rule['alert']
                    else:
                        res['name'] = rule['record']
                    result.append(res)

    return result
