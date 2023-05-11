# Contributing
Thanks for taking time to contribute and helping us make this project better! The following is a set of guidelines for contributing to Runbooks.sh. 
 
Please note we have a code of conduct, please follow it in all your interactions with the project.
 
## Submitting issues

We have several forms for your issues:
* [Bug Report](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=): Ensure you have followed the steps in the form so we can best assist you.
* [Feature Request](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=): Do you have an awesome idea to make runbooks.sh better?  We want to hear it!
* [Action Creation](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=action%2Ctriage&projects=&template=add_action.yml&title=%5BAction%5D%3A+): Do you have an idea for a new Action inside Runbooks.sh?
* [RunBook idea](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=runbook%2Ctriage&projects=&template=add_runbook.yml&title=%5BRunBook%5D%3A+): Have a request or idea for a RunBook that will make the life of an SRE better?  File it using this form.

 
 
 ## Contributing
-------------------------
 
* Always **make a new branch** for your work. 
* **Base your new branch off of the master branch** on the main
 repository.
 

### Create a new xRunBook
Your RunBooks are stored locally at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks``` Copy an existing xRunBook and rename it. It will appear in the Welcome page on refresh. Click to Open.
Your saved xRunBook can be found at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks```

  1. All created RunBooks have a ipynb file. You'll need to create a .json file with metadata about your RunBook.  Copy from another RunBook un the repository, and update the values for each parameter.
  2. Use the sanitize.py script to remove all parameters and outputs from your Runbook:
  ```shell
      python3 sanitize.py -f <ipynb file> 
  ```
  3. Copy the saved RunBook (json and ipynb) files from the Custom folder into the folder of the Connector used, and submit a PR!
  

### Create a new Action

#### Create a new action inside an existing RunBook.

   1. If you will not use external credentials, click *+Add Action* at the top of the menu.
   2. If you will be using an existing credential, add an existing Action for that service (like AWS), and edit the code to create your new Action.
   3. If the service you'd like to build for does not have credentials yet, please [file an issue](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=Credential%2Ctriage&template=add_credential.yml&title=%5BCredential%5D%3A+).
   
#### Creating and connecting your Action

1. [Creating Custom Actions](https://docs.unskript.com/unskript-product-documentation/guides/actions/create-custom-actions) describes the steps to create your own Action.
2.  To submit to OSS, follow the [Submit An Action](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source#actions) instructions.  

 
## Support Channels
---
Whether you are a user or contributor, official support channels include:
- GitHub issues: https://github.com/unskript/Awesome-CloudOps-Automation/issues/new
- Slack: https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation
 
