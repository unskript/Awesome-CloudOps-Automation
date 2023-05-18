#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import collections
from typing import Dict
import pprint
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')
    podname: str = Field(
        title='Pod',
        description='K8S Pod Name')


def k8s_desribe_pod_printer(output):
    if output is None:
        return 

    pprint.pprint(output)

def k8s_describe_pod(handle, namespace: str, podname: str) -> Dict:
    """k8s_describe_pod get Kubernetes POD details

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type podname: str
        :param podname: K8S Pod Name.

        :rtype: Dict of POD details
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    def cleanNullTerms(_dict):
        """Delete None values recursively from all of the dictionaries"""
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                cleanNullTerms(value)
            elif value is None:
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    if isinstance(v_i, dict):
                        cleanNullTerms(v_i)

        return _dict

    data = {}
    try:
        resp = coreApiClient.read_namespaced_pod(
            name=podname, namespace=namespace)
        resp = resp.to_dict()
        del resp['metadata']['managed_fields']
        resp = cleanNullTerms(resp)
        data["Name"] = resp['metadata']['name']
        data["Namespace"] = namespace
        data["Priority"] = resp['spec']['priority']
        data["Node"] = resp['spec']['node_name']
        data["Start Time"] = resp['status']['start_time']
        data["Labels"] = resp['metadata']['labels']
        if "annotations" in resp['metadata']:
            data["Annotations"] = resp['metadata']['annotations']
        data["Status"] = resp['status']['phase']
        data["IP"] = resp['status']['pod_ip']
        data["IPS"] = resp['status'].get('pod_i_ps')
        data["Controlled By"] = resp['metadata']['owner_references'][0]['kind'] + \
            "/" + resp['metadata']['owner_references'][0]['name']
        data["Containers"] = ''
        ####
        for container in resp['spec']['containers']:
            data['  ' + container['name']] = ''
            for c in container:
                data['      ' + c] = container[c]
        # Container Index Represents the Number of containers in a given POD
        container_index = 0
        msglist = []
        for c in resp['status']['container_statuses']:
            data[' ' + c['name']] = ''
            data['   ' + 'Container ID'] = c['container_id']
            data['   ' + 'Image'] = c['image']
            data['   ' + 'Image ID'] = c['image_id']
            data['   ' + 'Port'] = resp['spec']['containers'][container_index]['ports']
            if 'command' in resp['spec']['containers'][container_index]:
                data['   ' + 'Command'] = resp['spec']['containers'][container_index]['command']
            if 'args' in resp['spec']['containers'][container_index]:
                data['   ' + 'Args'] = resp['spec']['containers'][container_index]['args']
            data['   ' + 'State'] = ''
            if c['state']['running'] is None and c['state']['waiting'] is not None:
                data['     ' + 'Reason'] = c['state']['waiting']['reason']
                if c['last_state']['terminated'] is not None:
                    msglist.append(c['last_state']['terminated']['message'])
            container_index += 1
        data['Conditions'] = ''
        for c in resp["status"]["conditions"]:
            data["Type"] = "Status"
            data[c["type"]] = bool(c["status"])

        data['Volumes:'] = ''
        for container in resp["spec"]["volumes"]:
            for c in container:
                data['      ' + c] = container[c]
        data['QoS Class:'] = resp['status'].get('qos_class')
        tolerations = []
        for toleration in resp['spec']['tolerations']:
            tolerations.append(toleration["key"] + ":" + toleration["effect"] + " op=" + \
                         toleration["operator"] + " for " + str(toleration["toleration_seconds"]))
        data['Tolerations'] = tolerations
        data['Events'] = msglist
    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason
        raise e

    print('\n')    
    data = collections.OrderedDict(data)
    return data
