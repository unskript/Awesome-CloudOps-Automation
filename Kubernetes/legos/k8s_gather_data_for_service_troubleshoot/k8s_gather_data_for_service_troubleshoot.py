#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import pprint
import json
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    service_name: str = Field(
        title="Service Name",
        description="K8S Service Name to gather data"
    )
    namespace: str = Field(
        title='Namespace',
        description='k8s Namespace')


def k8s_gather_data_for_service_troubleshoot_printer(output):
    if not output:
        return
    pprint.pprint(output)

def k8s_gather_data_for_service_troubleshoot(handle, servicename: str, namespace: str) -> dict:
    """k8s_gather_data_for_service_troubleshoot This utility function can be used to gather data
       for a given service in a namespace. 

       :type handle: object
       :param handle: Object returned from task.validate(...) function

       :type servicename: str
       :param servicename: Service Name that needs gathering data

       :type namespace: str
       :param namespace: K8S Namespace

       :rtype: Dictionary containing the result
    """
    if not namespace or not servicename :
        raise Exception("Namespace and Servicename are mandatory parameter")

    # Get Service Detail
    describe_cmd = f'kubectl describe svc {servicename} -n {namespace}'
    describe_output = handle.run_native_cmd(describe_cmd)
    retval = {}
    if not describe_output.stderr:
        retval['describe'] = describe_output.stdout

    # To Get the Ingress rule, we first find out the name of the ingress
    # Find out the ingress rules in the given namespace, find out the
    # Matching rule in the ingress that matches the service name and append it
    # to the `ingress` key.
    rule_name = ''
    ingress_rules_for_service = []
    ingress_rule_name_cmd = f"kubectl get ingress -n {namespace} -o name"
    ingress_rule_name_output = handle.run_native_cmd(ingress_rule_name_cmd)
    if not ingress_rule_name_output.stderr:
        rule_name = ingress_rule_name_output.stdout

    ingress_rules_cmd = f"kubectl get ingress -n {namespace}" + \
        ' -o jsonpath="{.items[*].spec.rules}"'
    ingress_rules_output = handle.run_native_cmd(ingress_rules_cmd)
    if not ingress_rules_output.stderr:
        rules = json.loads(ingress_rules_output.stdout)
        for r in rules:
            h = r.get('host')
            for s_p in r.get('http').get('paths'):
                if s_p.get('backend').get('service').get('name') == servicename:
                    ingress_rules_for_service.append([
                        h,
                        s_p.get('backend').get('service').get('port'),
                        s_p.get('path')
                        ])

    if ingress_rules_for_service:
        retval['ingress'] = []
        for ir in ingress_rules_for_service:
            if len(ir) >= 3:
                retval['ingress'].append({'name': rule_name,
                            'namespace': namespace, 
                            'host': ir[0],
                            'port': ir[1],
                            'path': ir[-1]})


    return retval
