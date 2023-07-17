##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import List, Optional
from pydantic import BaseModel, Field
from google.cloud import compute_v1

class InputSchema(BaseModel):
    project: str = Field(..., description='GCP project ID', title='Project ID')


def gcp_get_forwarding_rules_details_printer(output):
    if output is None:
        return
    print(output)

def get_backend_services(project, handle):
    client = compute_v1.BackendServicesClient(credentials=handle)
    backend_services = client.list(project=project)
    return {service.self_link: service.name for service in backend_services}

def get_target_proxy(forwarding_rule, project, handle):
    target_http_proxy = []
    if 'targetHttpProxies' in forwarding_rule.target:
        target_proxy = compute_v1.TargetHttpProxiesClient(credentials=handle).get(
            project=project,
            target_http_proxy=forwarding_rule.target.split('/')[-1]
        )
    elif 'targetHttpsProxies' in forwarding_rule.target:
        target_https_proxy = []
        target_proxy = compute_v1.TargetHttpsProxiesClient(credentials=handle).get(
            project=project, 
            target_https_proxy=forwarding_rule.target.split('/')[-1]
        )
    else:
        raise Exception('Unsupported target proxy type')
    return target_proxy


def gcp_get_forwarding_rules_details(handle, project: str) -> List:
    """gcp_get_forwarding_rules_details Returns the List of forwarding rules, its path and the associated backend service.

    :type project: string
    :param project: Google Cloud Platform Project

    :rtype: List of of forwarding rules, its path and the associated backend service..
    """
    client = compute_v1.GlobalForwardingRulesClient(credentials=handle)
    backend_services = get_backend_services(project, handle)
    result = []
    # list all global forwarding rules
    forwarding_rules = client.list(project=project)
    for forwarding_rule in forwarding_rules:
        target_proxy = get_target_proxy(forwarding_rule, project, handle)
        # get the associated URL map
        url_map = compute_v1.UrlMapsClient(credentials=handle).get(project=project, url_map=target_proxy.url_map.split('/')[-1])
        # check if any backend service is associated with this URL map
        for path_matcher in url_map.path_matchers:
            for path_rule in path_matcher.path_rules:
                if backend_services.get(path_rule.service):
                    result.append({"forwarding_rule_name":forwarding_rule.name, "backend_service":backend_services.get(path_rule.service), "path":path_rule.paths})
    return result


