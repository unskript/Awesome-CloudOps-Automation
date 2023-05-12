
<p align="center">
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
<p align="center">
  <h3 align="center">Action Development Guide</h3>
  <p align="center">
    CloudOps automation made simple!
    <br />
    <br />
    <a href="https://unskript.com/blog">Visit our blog</a>
    ·
    <a href="https://www.youtube.com/channel/UCvtSYNHVvuogq2u-F7UDMkw">YouTube Tutorials</a>
    .
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>


# Actions

Actions are the atomic units of xRunBooks.  All xRunBooks are composed of Actions, and each Action is a step that progresses the xRunBook.

In this document, we'll walk through the anatomy of a Lego/Action, how they are created, and how they work.

> TL;dr: If you build your Action with the Docker Open source, and save it to your computer, these files will be generated for you. You'll have to modify two files before making a contribution: 
  * the JSON file (to update the parameters)
  * the Readme (tell us what your action does and how it works)


# Lego Authoring Guidelines

## Directory Structure

The Directory structure is:

1. CONNECTOR is a directory of xRunBooks and Lego/Actions that are run for a particular service/API/etc. (for example: Redis, AWS or Slack)
2. Inside the CONNECTOR Directory will be two files for each xRunBook (a JSON file and the actual rRunBook in the .ipynb file), and the Lego subdirectory will hold all of the Actions.

In this document, we'll walk through the steps in creating an Action.

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

 1. Every Directory under the CONNECTOR will have __init__.py file (Essential to distinguish as a module/sub-module).  

 2. Every CONNECTOR will have a legos Directory. (Example: AWS/legos)

 3. Underneath of legos directory, Every Lego will have the same Name Directory Example: aws_delete_volume will have aws_delete_volume.py underneath of it. 

 4. Every Lego Directory will have:
    1. [README.md](#readmemd)
    2. [JSON File](#json-file)
    3. [py file](#python-file) 
    
    You may have additional files if your readme has images.


## README.md

The  README.md explains what the Action is supposed to do, It should contain:

  1. **Action Title** 
      ```
        Example:
          <h2>Delete AWS EBS Volume </h2>
      ```

  2.  **Description**: explains what the Lego is intended to do.

      ```
      This Action deletes AWS EBS volume and gives a list of deletion status.
      ```

  3. **Action Details**: here we explain the Action signature, what are the different input fields to the Action.  It's also nice to add an example of how the Action might be used:

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
    
 5. **Action Input**: explains how many parameters are needed for the LeActiongo. Which of them are Mandatory, which of them are optional. 

 ```

This Action take three inputs handle, volume_id and region. All three are required.
 ```

 6. **Action Output** A sample output from the Action upon completion.  Ensure to remove sensitive values. 


## Action JSON file

If you created your Action with the Docker build of unSkript, the JSON file is generated for you. 

Here is an example JSON file:
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
    "action_supports_iteration": true,
    "action_categories": []
  }
  
```
All of these fields are Mandatory.

* **Action Title**: The human readable title of your Lego
* **Action Description**: a text description of what the Lego does
* **Action Type**:
* Action Entry Function:
* **Action Needs Credential**: Boolean - are the credentials for this connector required?
* **Action Output Type**: A string? a List?  what does the output look like?
* **Action Supports Poll**: can we poll this Action if it takes a while to finish?
* **action_supports_iteration**: Can we run this Action many times with multiple inputs?
* **action_categories**: categories that appear in teh documentation - for added visibility of your action.


## Python file

This is the Python file that is run in the xRunBook.  Examples can be found in the various Lego directories in this repository.

The fastest way to create the Python file is to create your Action in the Docker build of unSkript. WHen you save your Action (from the three dot menu next to the "Run Action" button), it will be saved locally on your computer

## __init__.py

This can be copied from any other Action directory and pasted in.



