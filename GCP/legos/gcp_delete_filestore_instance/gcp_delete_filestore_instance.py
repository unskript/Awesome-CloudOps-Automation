##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from google.cloud import filestore_v1

class InputSchema(BaseModel):
    project_name: str = Field(
        title = "GCP Project Name(ID)",
        description = "GCP Project Name"
    )
    location: str = Field(
        title = "Location",
        description = "GCP locations map to GCP zones Eg: us-west1-b"
    )
    instance_id: str = Field(
        title = "Instance ID",
        description = "Name of the instance to be deleted"
    )

def gcp_delete_filestore_instance_printer(output):
    if output is None:
        return
    pprint.pprint(output)
    

def gcp_delete_filestore_instance(handle, instance_id:str, project_name:str, location:str) -> Dict:
    """gcp_delete_filestore_instance Returns status of details of the deleted Filestore Instance

        :type instance_id: string
        :param instance_id: Name of the instance to create

        :type project_name: string
        :param project_name: GCP Project Name

        :type location: string
        :param location: GCP locations map to GCP zones Eg: us-west1-b

        :rtype: Status of Deleted Filestore Instance
    """
    try:
        client = filestore_v1.CloudFilestoreManagerClient(credentials=handle)
        name = "projects/"+ project_name +"/locations/"+ location +"/instances/"+ instance_id
        request = filestore_v1.DeleteInstanceRequest(name=name)
        operation = client.delete_instance(request=request)
        print("Waiting for operation to complete...")
        operation.result()
        result_dict={"Message":"Filestore Instance deleted"}
    except Exception as e:
        raise e
    return result_dict