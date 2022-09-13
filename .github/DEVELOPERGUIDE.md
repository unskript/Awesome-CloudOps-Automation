
<p align="center">
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
<p align="center">
  <h3 align="center">Lego Development Guide</h3>
  <p align="center">
    CloudOps automation made simpler!
    <br />
    <br />
    <a href="https://medium.com/unskript">Visit our blog</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>


## Lego Authoring Guidelines

The Directory structure Followed on Awesome-CloudOps-Automation is 

```
CONNECTOR
    |- __init__.py
    |-  RUNBOOKS 
    |-  legos
          |- __init__.py
          |- LEGO1
          |     |- __init__.py
          |     |- README.md
          |     |- LEGO1.json 
          |     |- LEGO1.py
          |     |- LEGO1_SUPPORTING.png/gif/jpeg 
          | 
          |- LEGO2
                |- __init__.py
                |- README.md
                |- LEGO2.json
                |- LEGO2.py
                |- LEGO2_SUPPORTING.png/gif/jpeg 
```          
          
          
Example:
```
AWS
 |- Resize_PVC.ipynb
 |- __init__.py
 |- legos
      |- __init__.py
      |- aws_delete_volume
             |- __init__.py
             |- README.md
             |- aws_delete_volume.json
             |- aws_delete_volume.py

```
 1. Every Directory under the CONNECTOR will have __init__.py file (Essential to distinguish as a module/sub-module)

 2. Every CONNECTOR will have a legos Directory. (Example: AWS/legos)

 3. Underneath of legos directory, Every Lego will have the same Name Directory Example: aws_delete_volume will have aws_delete_volume.py underneath of it. 

 4. Every Lego Directory will have 

    1. A README.md explaining what the LEGO is supposed to do, It should contain

      a. Lego Title. 
      
        Example:
          <h2>Delete AWS EBS Volume </h2>

      b. Description,  explaining what the Lego is intended to do

      c. Lego Details,  here we explain the Lego signature, what are the different input fields to the Lego. And should also be substituted with an Example. 

         Like:
           aws_delete_volumes(handle: object, volume_id: str, region: str)

           handle: Object of type unSkript AWS Connector
           volume_id: Volume ID needed to delete particular volume
           region: Used to filter the volume for specific region
        
         Example Usage:
           aws_delete_volumes(handle,
                           "vol-039ce61146a4d7901",
                           "us-west-2")
    
 5. README.md should have a Lego Input Section. That basically explains how many parameters is needed for the Lego. Which of them are Mandatory, which of them are optional. 

 6. README.md should have a Lego Output Section. Either you can take a screenshot of the Actual Lego being run on a Runbook and include it in the Runbook or just copy paste it below the Lego Output Section. 

     Example: 
     ## Lego Output
     Here is a sample output
       ```
        Sample Output For the Lego
       ```

###  Legos' Corresponding JSON file

Example:

{
    "action_title": "Filter AWS EC2 Instance",
    "action_description": "Filter AWS EC2 Instance",
    "action_type": "LEGO_TYPE_AWS",
    "action_entry_function": "aws_filter_ec2_by_tags",
    "action_needs_credential": true,
    "action_output_type": "ACTION_OUTPUT_TYPE_LIST",
    "action_supports_poll": true,
    "action_supports_iteration": true
  }
  

Here action_title represents the Action Title

Most are self explanatory fields. All of these fields are Mandatory.

* Actual Lego (Python) file

This would be the actual Python file

    Example

    ##
    ##  Copyright (c) 2021 unSkript, Inc
    ##  All rights reserved.
    ##
    import pprint
    from typing import List
    from pydantic import BaseModel, Field
    from unskript.connectors.aws import aws_get_paginator
    from beartype import beartype

    class InputSchema(BaseModel):
        tag_key: str = Field(
            title='Tag Key',
            description='The key of the tag.')
        tag_value: str = Field(
            title='Tag Value',
            description='The value of the key.')
        region: str = Field(
            title='Region',
            description='AWS Region.')

    @beartype
    def aws_filter_ec2_by_tags_printer(output):
        if output is None:
            return
        pprint.pprint({"Instances": output})


    @beartype
    def aws_filter_ec2_by_tags(handle, tag_key: str, tag_value: str, region: str) -> List:
        """aws_filter_ec2_by_tags Returns an array of instances matching tags.

            :type handle: object
            :param handle: Object returned by the task.validate(...) method

            :type tag_key: string
            :param tag_key: AWS Tag Key that was used ex: ServiceName, ClusterName, etc..

            :type tag_value: string
            :param tag_value: The Value for the Above Key, example "vpn-1" so the Lego will search
                            only the required texts in the Lego.
            
            :type region: string
            :param region: The AWS Region, For example `us-west-2`

            :rtype: Array of instances matching tags.
        """
        # Input param validation.

        ec2Client = handle.client('ec2', region_name=region)
        res = aws_get_paginator(ec2Client, "describe_instances", "Reservations",
                                Filters=[{'Name': 'tag:' + tag_key, 'Values': [tag_value]}])

        result = []
        for reservation in res:
            for instance in reservation['Instances']:
                result.append(instance['InstanceId'])
        return result



