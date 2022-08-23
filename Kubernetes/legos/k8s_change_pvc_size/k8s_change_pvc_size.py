#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Optional
from unskript.enums.aws_k8s_enums import SizingOption
import pprint

class InputSchema(BaseModel):
    namespace: str = Field(
        title="Namespace",
        description="Namespace of the PVC."
    )
    name: str = Field(
        title="PVC Name",
        description="Name of the PVC."
    )
    resize_option: Optional[SizingOption] = Field(
        default=SizingOption.Add,
        title="Resize option",
        description='''
            Option to resize the volume. 2 options supported:
            1. Add - Use this option to resize by an amount.
            2. Multiple - Use this option if you want to resize by a multiple of the current volume size.
        '''
    )
    resize_value: float = Field(
        title="Value",
        description='''
            Based on the resize option chosen, specify the value. For eg, if you chose Add option, this
            value will be a value in Gi (like 100). If you chose Multiple option, this value will be a multiplying factor
            to the current volume size. So, if you want to double, you specify 2 here.
        '''
    )

def k8s_change_pvc_size_printer(output):
    if output is None:
        return

    pprint.pprint(output)



def k8s_change_pvc_size(handle, namespace: str, name: str, resize_option: SizingOption, resize_value: float) -> str:
    # Get the current size.
    kubectl_command = f'kubectl get pvc {name} -n {namespace}  -o jsonpath={{.status.capacity.storage}}'
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        print(
            f"Error while executing command ({kubectl_command}): {result.stderr}")
        return str(f"Error Changing PVC Size {kubectl_command}: {result.stderr}")

    currentSize = result.stdout
    currentSizeInt = int(currentSize.rstrip("Gi"))
    if resize_option == SizingOption.Add:
        newSizeInt = currentSizeInt + resize_value
    else:
        newSizeInt = currentSizeInt * resize_value
    newSize = str(newSizeInt) + "Gi"
    print(f'Current size {currentSize}, new Size {newSize}')
    kubectl_command = f'kubectl patch pvc {name} -n {namespace} -p \'{{"spec":{{"resources":{{"requests": {{"storage": "{newSize}"}}}}}}}}\''
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        print(
            f"Error while executing command ({kubectl_command}): {result.stderr}")
        return str(f"Error Changing PVC Size {kubectl_command}: {result.stderr}")
    print(f'PVC {name} size changed to {newSize} successfully')
    return result.stdout
