##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field
from google.cloud import filestore_v1
from beartype import beartype
from google.protobuf.json_format import MessageToDict
from typing import List, Dict
import pprint

class InputSchema(BaseModel):
    instance_id: str = Field(
        title = "Instance ID",
        description = "Name of the instance to create"
    )
    project_name: str = Field(
        title = "GCP Project Name(ID)",
        description = "GCP Project Name"
    )
    location: str = Field(
        title = "Location",
        description = "GCP locations map to GCP zones Eg: us-west1-b"
    )
    network: str = Field(
        'default',
        title = "Network",
        description = "Name of the Google Compute Engine VPC network"
    )
    description: str = Field(
        '',
        max_length= 2048,
        title = "Description",
        description = "Description of the instance (2048 characters or less)"
    )
    name: str = Field(
        title = "Name",
        description = "Resource name of the instance"
    )
    capacity: int = Field(
        title = "Capacity",
        description = "File share capacity in gigabytes (GB). Eg: 1024 "
    )
    tier: str = Field(
        title = "Tier",
        description = "Service tier for instance Eg: STANDARD"
    )

def gcp_create_filestore_instance_printer(output):
    if output is None:
        return
    pprint.pprint(output)
    
def gcp_create_filestore_instance(handle, instance_id:str, project_name:str, location:str, network:str, tier:str, description:str, name:str, capacity:int ) -> Dict:
    """gcp_create_filestore_instance Returns a Dict of details of the newly created Filestore Instance

        :type instance_id: string
        :param instance_id: Name of the instance to create

        :type project_name: string
        :param project_name: GCP Project Name

        :type location: string
        :param location: GCP locations map to GCP zones Eg: us-west1-b

        :type network: string
        :param network: Name of the Google Compute Engine VPC network

        :type tier: string
        :param tier: Service tier for instance Eg: STANDARD

        :type description: string
        :param description: Description of the instance (2048 characters or less)

        :type name: string
        :param name: Resource name of the instance

        :type capacity: int
        :param capacity: File share capacity in gigabytes (GB). Eg: 1024

        :rtype: Dict of Filestore Instance Details
    """
    try:
        instance_details_dict= {"networks": [{"network": network,"modes": ["MODE_IPV4"]}],"tier": tier.upper(),"description": description,"file_shares": [{"name": name,"capacity_gb": capacity}]}
        parent_path = "projects/"+project_name+"/locations/"+location
        client = filestore_v1.CloudFilestoreManagerClient(credentials=handle)
        request = filestore_v1.CreateInstanceRequest(parent=parent_path,instance=instance_details_dict,instance_id=instance_id)
        operation = client.create_instance(request=request)
        print("Waiting for operation to complete...")
        response = operation.result()
        result_dict = MessageToDict(response._pb)
    except Exception as e:
        result_dict= {"Error": e}
    return result_dict