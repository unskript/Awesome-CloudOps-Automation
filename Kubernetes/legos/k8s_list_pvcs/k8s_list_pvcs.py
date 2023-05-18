#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from typing import Optional, List
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='Kubernetes namespace')

def k8s_list_pvcs_printer(output):
    if output is None:
        return

    pprint.pprint(output)

def k8s_list_pvcs(handle, namespace: str = '') -> List:
    """k8s_list_pvcs list pvcs

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :rtype: List
    """
    if namespace == '':
        kubectl_command = ('kubectl get pvc -A --output=jsonpath=\'{range .items[*]}'
                           '{@.metadata.namespace}{","}{@.metadata.name}{"\\n"}{end}\'')
    else:
        kubectl_command = ('kubectl get pvc -n ' + namespace + ' --output=jsonpath=\''
                    '{range .items[*]}{@.metadata.namespace}{","}{@.metadata.name}{"\\n"}{end}\'')
    result = handle.run_native_cmd(kubectl_command)
    if result is None or hasattr(result, "stderr") is False or result.stderr is None:
        print(
            f"Error while executing command ({kubectl_command}): {result.stderr}")
        return []
    names_list = [y for y in (x.strip() for x in result.stdout.splitlines()) if y]
    output = []
    for i in names_list:
        ns, name = i.split(",")
        output.append({"Namespace": ns, "Name":name})
    return output
