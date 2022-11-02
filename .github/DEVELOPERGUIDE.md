
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


# Legos (AKA Actions)

Legos (also known as Actions) are the atomic units of xRunBooks.  All xRunBooks are composed of Legos, and each Lego is a step that porgresses the xRunBook.

In this document, we'll walk through the anatomy of a Lego/Action, how they are created, and how they work.

# Lego Authoring Guidelines

## Directory Structure

The Directory structure followed on Awesome-CloudOps-Automation is:

1. CONNECTOR is a directory of xRunBooks and Lego/Actions that are run for a particular service/API/etc. (for example: Redis, AWS or Slack)
2. Inside the CONNECTOR Directory will by Jupyter files for each xRunBook, and a subDirectory will hold all of the legos.

In this document, we'll walk through the steps in creating a Lego/Action.

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
          
          
Here's an Example structure for AWS, with a Lego called aws_delete_volume:
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

 4. Every Lego Directory will have:
    1. [README.md](#readmemd)
    2. [JSON File](#json-file)
    3. [py file](#python-file) 
    
    You may have additional files if your readme has images.


## README.md

The  README.md explains what the LEGO is supposed to do, It should contain:

  1. **Lego Title** 
      ```
        Example:
          <h2>Delete AWS EBS Volume </h2>
      ```

  2.  **Description**: explains what the Lego is intended to do.

      ```
      This Lego deletes AWS EBS volume and gives a list of deletion status.
      ```

  3. **Lego Details**: here we explain the Lego signature, what are the different input fields to the Lego.  It's also nice to add an example of how the Lego might be used:

      ```
      aws_delete_volumes(handle: object, volume_id: str, region: str)

      handle: Object of type unSkript AWS Connector
      volume_id: Volume ID needed to delete particular volume
      region: Used to filter the volume for specific region
      ```
        
      Example Usage:

           aws_delete_volumes(handle,
                           "vol-039ce61146a4d7901",
                           "us-west-2")
    
 5. **Lego Input**: explains how many parameters are needed for the Lego. Which of them are Mandatory, which of them are optional. 

 ```

This Lego take three inputs handle, volume_id and region. All three are required.
 ```

 6. **Lego Output** A sample output from the Lego/Action upon completion.  Ensure to remove sensitive values. 


## Lego JSON file

The JSON file lists 
Example:

```json
{
    "action_title": "Delete AWS EBS Volume by Volume ID",
    "action_description": "Delete AWS Volume by Volume ID",
    "action_type": "LEGO_TYPE_AWS",
    "action_entry_function": "aws_delete_volumes",
    "action_needs_credential": true,
    "action_output_type": "ACTION_OUTPUT_TYPE_LIST",
    "action_supports_poll": true,
    "action_supports_iteration": true
  }
  
```
All of these fields are Mandatory.

* **Action Title**: The human readable title of your Lego
* **Action Description**: a text description of what the Lego does
* **Action Type**:
* Action Entry Function:
* **Action Needs Credential**: Boolean - are the credentials for this connector required?
* **Action Output Type**:
* **Action Supports Poll**:


## Python file

This is the Python file that is run in the xRunBook.  Examples can be found in the various Lego directories in this repository.


##