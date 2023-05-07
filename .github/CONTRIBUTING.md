# Contributing
We like contributions, Thanks for taking time to contribute and helping us make this project better! The following is a set of guidelines for contributing to awesome-cloudops-automation. 
 
Please note we have a code of conduct, please follow it in all your interactions with the project.
 
## Submitting bugs
 
### Due diligence
-------------
Before submitting a bug, please do the following:
 
* Perform **basic troubleshooting** steps:
 
* **Search the GitHub issues** to make sure it's not a known
 issue.
* If you don't find a pre-existing issue, consider **checking with the slack channel** in case the problem is non-bug-related.
 
### What to put in your issue
------------------------------
 
Make sure issue you raised gets the attention it deserves: issues with missing
information may be ignored or punted back to you, delaying a fix.  The below
constitutes a bare minimum; more info is almost always better:
 
* **Which environment are you using?** Are you using the free trial, the Docker build? What browser are you using?  Including the unSkript build number (which can be seen at the top of each RunBook) will help us triage.

* **How can the developers recreate the bug on their end?** If possible,
 include a copy of your code or an example repo, the command you used to invoke it, and the full
 output of your run (if applicable.)
 
### Version control branching
-------------------------
 
* Always **make a new branch** for your work, no matter how small. This makes
 it easy for others to take just that one set of changes from your repository,
 in case you have multiple unrelated changes floating around.
 
 
* **Base your new branch off of the appropriate branch** on the main
 repository:
 
   * **Bug fixes** should be based on the branch named after the **oldest
     supported release line** the bug affects.

       * Bug fixes requiring large changes to the code or which have a chance
         of being otherwise disruptive, may need to base off of **master**
         instead. This is a judgement call -- ask the devs!
 
   * **New features** should branch off of **the 'master' branch**.
 
       * Note that depending on how long it takes for the dev team to merge
         your patch, the copy of ``master`` you worked off of may get out of
         date! If you find yourself 'bumping' a pull request that's been
         sidelined for a while, **make sure you rebase or merge to latest
         main** to ensure a speedier resolution.
 
 
## Full example
------------
 
Here's an example workflow for a project `theproject` hosted on Github, which
is currently in version 1.0.x. Your username is `yourname` and you're
submitting a basic bugfix. (This workflow only changes slightly if the project
is hosted at Bitbucket, self-hosted, or etc.)
 
### Preparing your Fork
  
1. Click 'Fork' on Github, creating e.g. `yourname/theproject`.
2. Clone your project: `git clone git@github.com:yourname/theproject`.
3. `cd theproject`
4. Create a branch: `git checkout -b foo-the-bars 1.0`.
 
### Making your Changes
 

1. Write tests expecting the correct/fixed functionality; make sure they fail.
2. Hack, hack, hack.
3. Run tests again, making sure they pass.
4. Commit your changes: `git commit -m "Foo the bars"`
 
### Creating Pull Requests
 
 
1. Push your commit to get it back up to your fork: `git push origin HEAD`
2. Visit Github, click handy "Pull request" button that it will make upon
  noticing your new branch.
3. In the description field, write down issue number (if submitting code fixing
  an existing issue) or describe the issue + your fix (if submitting a wholly
  new bugfix).
4. Hit 'submit'! And please be patient - the maintainers will get to you when
  they can.
 
## Support Channels
---
Whether you are a user or contributor, official support channels include:
- GitHub issues: https://github.com/unskript/Awesome-CloudOps-Automation/issues/new
- Slack: https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation
 
 ## Additional Section: Contribution Tips
1. Use the [Docker environment](#get-started-with-docker), or our free [cloud sandbox](https://us.app.unskript.io/profiles/6c38d3da1cde7b3c0623d138f525a5508a3260c8) for testing your contribution.
2. Join our [Slack Community](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to discuss your PR, and for support if you run into any issues.



### Create a new xRunBook
Your RunBooks are stored locally at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks``` Copy an existing xRunBook and rename it. It will appear in the Welcome page on refresh. Click to Open.
Your saved xRunBook can be found at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks```

  1. All created RunBooks have a ipynb file. You'll need to create a .json file with metadata about your RunBook.  Copy from another RunBook un the repository.
  2. Copy the saved RunBook from the Custom folder into the folder of the Connector used, and submit a PR!
  3. Submit Your xRunBook to the repository. Follow the [submission steps](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source) to remove credentials, etc. from your xRunBook.
  

### Create a new Action

#### Create a new action inside an existing RunBook.

   1. If you will not use external credentials, click *+Add Action* at the top of the menu.
   2. If you will be using an existing credential, add an existing Action for that service (like AWS), and edit the code to create your new Action.
   3. If the service you'd like to build for does not have credentials yet, please [file an issue](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=Credential%2Ctriage&template=add_credential.yml&title=%5BCredential%5D%3A+).
#### Creating and connecting your Action

1. [Creating Custom Actions](https://docs.unskript.com/unskript-product-documentation/guides/actions/create-custom-actions) describes the steps to create your own Action.
2.  To submit to OSS, follow the [Submit An Action](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source#actions) instructions.  

### Extending Docker
You can use our base docker and extend the functionality to fit your need. Follow this [document](./README_extending_docker.md) to create and build your own custom docker.
