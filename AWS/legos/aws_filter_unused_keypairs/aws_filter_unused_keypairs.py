##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator

class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default="",
        title='Region',
        description='Name of the AWS Region')


def aws_filter_unused_keypairs_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_filter_unused_keypairs(handle, region: str = None) -> Tuple:
    """aws_filter_unused_keypairs Returns an array of KeyPair.

        :type region: object
        :param region: Object containing global params for the notebook.

        :rtype: Object with status, result of unused key pairs, and error.
    """
    all_keys_dict = {}
    used_keys_dict = {}
    key_pairs_all = []
    used_key_pairs = []
    result = []
    all_regions = [region]
    if region is None or len(region)==0:
        all_regions = aws_list_all_regions(handle=handle)
    for r in all_regions:
        try:
            ec2Client = handle.client('ec2', region_name=r)
            key_pairs_all = list(map(
                lambda i: i['KeyName'],
                ec2Client.describe_key_pairs()['KeyPairs']
                ))
            res = aws_get_paginator(ec2Client, "describe_instances", "Reservations")
            for reservation in res:
                for keypair in reservation['Instances']:
                    if 'KeyName'in keypair and keypair['KeyName'] not in used_key_pairs:
                        used_key_pairs.append(keypair['KeyName'])
            used_keys_dict["region"]=r
            used_keys_dict["key_name"]=used_key_pairs
            all_keys_dict["region"]=r
            all_keys_dict["key_name"]=key_pairs_all
            final_dict = {}
            final_list=[]
            for k,v in all_keys_dict.items():
                if v!=[]:
                    if k=="key_name":
                        for each in v:
                            if each not in used_keys_dict["key_name"]:
                                final_list.append(each)
                if len(final_list)!=0:
                    final_dict["region"]=r
                    final_dict["unused_keys"]=final_list
            if len(final_dict)!=0:
                result.append(final_dict)
        except Exception:
            pass

    if len(result) != 0:
        return (False, result)
    return (True, None)
