##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from unskript.legos.aws.aws_list_all_regions.aws_list_all_regions import aws_list_all_regions
from unskript.connectors.aws import aws_get_paginator
import pprint


class InputSchema(BaseModel):
    region: Optional[str] = Field(
        default='',
        title='AWS Region',
        description='AWS Region.'
    )


def aws_find_old_gen_emr_clusters_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_find_old_gen_emr_clusters(handle, region: str = "") -> Tuple:
    """aws_find_old_gen_emr_clusters Gets list of old generation EMR clusters.

        :type region: string
        :param region: AWS Region.

        :rtype: Tuple with list of old generation EMR clusters.
    """
    result = []
    all_regions = [region]
    old_gen_type_prefixes = ['m1.', 'c1.', 'cc1.', 'm2.', 'cr1.', 'cg1.', 't1.']
    if not region:
        all_regions = aws_list_all_regions(handle)
    for reg in all_regions:
        try:
            emr_Client = handle.client('emr', region_name=reg)
            response = aws_get_paginator(emr_Client, "list_clusters", "Clusters")
            for cluster in response:
                instance_groups_list = aws_get_paginator(emr_Client, "list_instance_groups", "InstanceGroups",
                                                        ClusterId=cluster['Id'])
                for instance_group in instance_groups_list:
                    cluster_dict = {}
                    if instance_group['InstanceType'].startswith(tuple(old_gen_type_prefixes)):
                        cluster_dict["cluster_id"] = cluster['Id']
                        cluster_dict["region"] = reg
                        result.append(cluster_dict)
                        break
        except Exception as error:
            pass

    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)