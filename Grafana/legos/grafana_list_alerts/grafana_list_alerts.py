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


def grafana_list_alerts(
        handle: Grafana,
        dashboard_id:int = None,
        panel_id:int = None
        ) -> List[dict]:
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
    try:
        response = handle.session.get(url,
                                     params=params)
    except Exception as e:
        print(f'Failed to get grafana rules, {str(e)}')
        raise e

    # Grafana ruler rules api response
    # https://editor.swagger.io/?url=https://raw.githubusercontent.com/grafana/grafana/main/pkg/services/ngalert/api/tooling/post.json
    result = []
    folder_names = json.loads(response.content).keys()
    for folder_name in list(folder_names):
        for alarm in json.loads(response.content)[folder_name]:
            rules = alarm.get('rules')
            if rules is not None:
                for rule in rules:
                    res = {}
                    grafana_alert = rule.get('grafana_alert')
                    if grafana_alert is not None:
                        res['id'] = grafana_alert.get('id')
                        res['name'] = alarm.get('name')
                        result.append(res)

    # Get Loki/Prometheus alerts as well.
    # First get the datasources which has type Loki or Prometheus.
    #
    url = handle.host + "/api/datasources"
    try:
        response = handle.session.get(url)
        response.raise_for_status()
    except Exception:
        # This could happen because in non-cloud grafana, there is no rbac,
        # so this api doesnt work with viewer role.
        print("Unable to get datasources")
        return result

    try:
        datasourcesList = json.loads(response.content)
    except Exception as e:
        print(f'Unable to parse datasources response, error {str(e)}')
        return result

    interestedDatasourcesList = []
    for datasource in datasourcesList:
        if datasource["type"] == "loki" or datasource['type'] == "prometheus":
            if datasource.get('uid') is not None:
                interestedDatasourcesList.append(datasource.get("uid"))

    for interestedDatasourceUID in interestedDatasourcesList:
        url = handle.host + "/api/ruler/" + interestedDatasourceUID + "/api/v1/rules"
        try:
            response = handle.session.get(url, params=params)
            response.raise_for_status()
        except Exception as e:
            print(f'Skipping {interestedDatasourceUID}, error {str(e)}')
            continue

        try:
            responseDict = json.loads(response.content)
        except Exception as e:
            print(f'Skipping uid {interestedDatasourceUID}, error {str(e)}')
            continue

        folder_names = responseDict.keys()
        for folder_name in list(folder_names):
            for alarm in responseDict[folder_name]:
                rules = alarm.get('rules')
                if rules is not None:
                    for rule in rules:
                        res = {}
                        grafana_alert = rule.get('grafana_alert')
                        if grafana_alert is not None:
                            res['id'] = grafana_alert.get('id')
                            res['name'] = alarm.get('name')
                            result.append(res)
                        # Loki have 'alert' in the key, where as recorded loki has
                        # 'record' as the key.
                        else:
                            if 'alert' in rule:
                                res['name'] = rule.get('alert')
                            else:
                                res['name'] = rule.get('record')
                            result.append(res)

    return result
