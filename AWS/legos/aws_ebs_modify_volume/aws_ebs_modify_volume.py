##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from unskript.enums.aws_k8s_enums import SizingOption
from polling2 import poll_decorator


class InputSchema(BaseModel):
    volume_id: str = Field(
        title="EBS Volume ID",
        description="EBS Volume ID to resize."
    )
    resize_option: SizingOption = Field(
        title="Resize option",
        description='''
            Option to resize the volume. 2 options supported:
            1. Add - Use this option to resize by an amount.
            2. Multiple - Use this option if you want to resize by a multiple of the current volume size.
        '''
    )
    resize_value: int = Field(
        title="Value",
        description='''
            Based on the resize option chosen, specify the value. For eg, if you chose Add option, this
            value will be a value in Gb (like 100). If you chose Multiple option, this value will be a multiplying factor
            to the current volume size. So, if you want to double, you specify 2 here.
        '''
    )
    region: str = Field(
        title="Region",
        description="AWS Region of the volume."
    )


def aws_ebs_modify_volume_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_ebs_modify_volume(
    hdl: Session,
    volume_id: str,
    resize_option: SizingOption,
    resize_value: int,
    region: str,
    ) -> str:
    """aws_ebs_modify_volume modifies the size of the EBS Volume.
    You can either increase it a provided value or by a provided multiple value.

    :type volume_id: string
    :param volume_id: ebs volume id.

    :type resize_option: SizingOption
    :param resize_option: option to resize the volume, by a fixed amount
    or by a multiple of the existing size.

    :type value: int
    :param value: The value by which the volume should be modified,
    depending upon the resize option.

    :type region: string
    :param region: AWS Region of the volume.

    :rtype: New volume size.
    """
    ec2Client = hdl.client("ec2", region_name=region)
    ec2Resource = hdl.resource("ec2", region_name=region)
    # Get the current volume size.
    Volume = ec2Resource.Volume(volume_id)
    currentSize = Volume.size
    if resize_option == SizingOption.Add:
        newSize = currentSize + resize_value
    elif resize_option == SizingOption.Mutiple:
        newSize = currentSize * resize_value

    print(f'CurrentSize {currentSize}, NewSize {newSize}')
    
    ec2Client.modify_volume(
        VolumeId=volume_id,
        Size=newSize) 
    
    # Check the modification state
    try:
        check_modification_status(ec2Client, volume_id)
    except Exception as e:
        raise f'Modify volumeID {volume_id} failed: {str(e)}'

    return f'Volume {volume_id} size modified successfully to {newSize}'


@poll_decorator(step=60, timeout=600, check_success=lambda x: x is True)
def check_modification_status(ec2Client, volumeID) -> bool:
    resp = ec2Client.describe_volumes_modifications(VolumeIds=[volumeID])
    state = resp['VolumesModifications'][0]['ModificationState']
    progress = resp['VolumesModifications'][0]['Progress']
    print(f'Volume modification state {state}, Progress {progress}')
    if state == 'completed' or state == None:
        return True
    elif state == 'failed':
        raise Exception("Get Status Failed")
    return False
