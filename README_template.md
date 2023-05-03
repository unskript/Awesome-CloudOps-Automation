[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]


<br />
<p align="center">
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
<p align="center">
  <h3 align="center">Awesome CloudOps Automation</h3>
  <p align="center">
    [[BADGE]]
  
  <p align="center">
    CloudOps automation made simple!
    <br />
    <a href="https://docs.unskript.com/unskript-product-documentation/open-source/cloudops-automation-with-unskript"><strong>Explore the docs</strong></a>
    <br />
      <a href="https://www.youtube.com/channel/UCvtSYNHVvuogq2u-F7UDMkw"><strong>unSkript on YouTube</strong></a>
    <br />
    <br />
    <a href="https://unskript.com/blog">Visit our blog</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>
</p>


## Mission
Simplify CloudOps automation for DevOps and SRE teams

## Vision 
A single repository to satisfy all your day-to-day CloudOps automation needs. Automate your workflows with our *Actions* that build automated *RunBooks*. 

With hundreds of Actions and RunBooks included in the repository, you can get started quickly with minimal toil.

>**Better. Faster. Smarter SRE.**

___
<br>

# Quick Start Guide



## Open Source Docker

Our Docker install is and will always be open source. It includes a Jupyter runtime and all of the prebuilt Actions and RunBooks. Build your own Actions and RunBooks

### Get Started
1.  Clone this repository to your local machine to your $HOME directory. 

```
cd $HOME
git clone https://github.com/unskript/Awesome-CloudOps-Automation 
cd Awesome-CloudOps-Automation
```

2.  Launch Docker.  (if you used a different directory in #1, update that in the first ```-v``` line.)

```
docker run -it -p 8888:8888 \
 -v $HOME/Awesome-CloudOps-Automation/custom:/data \
 -v $HOME/.unskript:/unskript \
 -e ACA_AWESOME_MODE=1 \
 --user root \
 docker.io/unskript/awesome-runbooks:latest
```

2a. If you wish a non-development version of the Docker (where your RunBooks and Credentials are not synced to the local machine), omit the ```-v``` and ```-e``` lines.

* [YouTube Playlist with step by step guides](https://www.youtube.com/watch?v=QT0sghAo_t0&list=PLG7TPzTSJYkfCAtWKpdTjlRcyS21mXsE2)

---
## Cloud Free Trial
* Our Cloud Free Trial features everything found in Open Source, plus some basic enterprise features like [scheduling](https://docs.unskript.com/unskript-product-documentation/guides/xrunbooks/schedules) and [environments](https://docs.unskript.com/unskript-product-documentation/guides/proxies/connect-your-environment). 
* [Free Trial: Cloud](https://us.app.unskript.io/) 
* [YouTube Tutorials using Free Trial](https://www.youtube.com/watch?v=QjqAcJEiQNo&list=PLG7TPzTSJYkeOIAOj9iaxCaczKHX_qwZ_)

---
<br/>

# Open and Use a xRunBook

Once Docker is running, your unSkript install can be found at http://127.0.0.1:8888/awesome.
A table lists the xRunBooks that are available. Click on the URL of the xRunBook you would like to explore. 


1. Check the `Parameters` button at the top of the page. This lists all of the input parameters, and the default values.  Change them as needed.
2. Click on each Action in the xRunBook.  The `Configurations` button will show if Credentials are needed, and the inputs required for the Action to be run. [How to Add Credentials](https://docs.unskript.com/unskript-product-documentation/guides/connectors).
3. Once each Action has been assigned Credentials and inputs, run each Action (in order) to run your xRunBook.



## Included xRunBooks
<details>
  <summary><b>See Full List</b></summary>

  These xRunBooks are included in every install.  Use them as is, or make a copy to modify for your use!

  | **Category**                                                                                               | **Runbooks**                                                                                                                                                                 | **URL**                                                                                                    |
  | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
  [[DYNAMIC_LIST]]
</details>

<br/>
<br/>


# Contribute to Awesome-CloudOps-Automation

All contributions are **greatly appreciated**. Check out our [Contribution Guidelines](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/CONTRIBUTING.md) for more details. 

## How to Contribute?

1. Work with us on any of our [open issues](https://github.com/unskript/awesome-cloudops-automation/issues).
2. Create a new Action. Read the [Action developer guide](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/DEVELOPERGUIDE.md) for more details.
3. Combine Actions into a xRunBook.  Your xRunBook will be featured on the ReadMe.  [What's a xRunBook?](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/Anatomy-of-Runbook.md)



## Contribution Tips:
1. Use the [Docker environment](#get-started-with-docker), or our free [cloud sandbox](https://us.app.unskript.io/profiles/6c38d3da1cde7b3c0623d138f525a5508a3260c8) for testing your contribution.
2. Join our [Slack Community](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to discuss your PR, and for support if you run into any issues.



## Create a new xRunBook:
Your RunBooks are stored locally at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks``` Copy an existing xRunBook and rename it. It will appear in the Welcome page on refresh. Click to Open.
Your saved xRunBook can be found at ```$HOME/Awesome-CloudOps-Automation/custom/runbooks```

  1. All created RunBooks have a ipynb file. You'll need to create a .json file with metadata about your RunBook.  Copy from another RunBook un the repository.
  2. Copy the saved RunBook from the Custom folder into the folder of the Connector used, and submit a PR!
  3. Submit Your xRunBook to the repository. Follow the [submission steps](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source) to remove credentials, etc. from your xRunBook.
  

## Create a new Action:

### Create a new action inside an existing RunBook.

   1. If you will not use external credentials, click *+Add Action* at the top of the menu.
   2. If you will be using an existing credential, add an existing Action for that service (like AWS), and edit the code to create your new Action.
   3. If the service you'd like to build for does not have credentials yet, please [file an issue](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=Credential%2Ctriage&template=add_credential.yml&title=%5BCredential%5D%3A+).
### Creating and connecting your Action

1. [Creating Custom Actions](https://docs.unskript.com/unskript-product-documentation/guides/actions/create-custom-actions) describes the steps to create your own Action.
2.  To submit to OSS, follow the [Submit An Action](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source#actions) instructions.  

## Extending Docker
You can use our base docker and extend the functionality to fit your need. Follow this [document](./README_extending_docker.md) to create and build your own custom docker.

<br/>

## unSkript CLI

With `unskript-ctl.sh` (called unSkript cuttle) allows you to
  * List Existing Runbook
  * List All Existing Health Checks
  * List All Existing Health Check per connector
  * Run All Existing Health Checks 
  * Run All Existing Health Checks per connector
  * Run an existing Runbook


Here are the Options that are supported by the CTL Command
```
unskript-ctl.sh 
usage: unskript-ctl [-h] [-lr] [-rr RUN_RUNBOOK] [-rc RUN_CHECKS] [-df DISPLAY_FAILED_CHECKS] [-lc LIST_CHECKS] [-sa SHOW_AUDIT_TRAIL]

Welcome to unSkript CLI Interface VERSION: 0.1.0

optional arguments:
  -h, --help            show this help message and exit
  -lr, --list-runbooks  List Available Runbooks
  -rr RUN_RUNBOOK, --run-runbook RUN_RUNBOOK
                        Run the given runbook
  -rc RUN_CHECKS, --run-checks RUN_CHECKS
                        Run all available checks [all | connector | failed]
  -df DISPLAY_FAILED_CHECKS, --display-failed-checks DISPLAY_FAILED_CHECKS
                        Display Failed Checks [all | connector]
  -lc LIST_CHECKS, --list-checks LIST_CHECKS
                        List available checks, [all | connector]
  -sa SHOW_AUDIT_TRAIL, --show-audit-trail SHOW_AUDIT_TRAIL
                        Show audit trail [all | connector | execution_id]
```


# Community
[Join the CloudOps Community Slack Channel](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to connect with other users, contributors and awesome people behind awesome CloudOps automation project. 

<br/>

# Road Map

See the [open issues](https://github.com/unskript/awesome-cloudops-automation/issues) for a list of proposed features (and known issues).


<br/>

# License
Except as otherwise noted this project is licensed under the `Apache License, Version 2.0` .

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 .

Unless required by applicable law or agreed to in writing, project distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


[contributors-shield]: https://img.shields.io/github/contributors/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[contributors-url]: https://github.com/unskript/awesome-cloudops-automation/graphs/contributors
[github-actions-shield]: https://img.shields.io/github/workflow/status/unskript/awesome-cloudops-automation/e2e%20test?color=orange&label=e2e-test&logo=github&logoColor=orange&style=for-the-badge
[github-actions-url]: https://github.com/unskript/awesome-cloudops-automation/actions/workflows/docker-tests.yml
[forks-shield]: https://img.shields.io/github/forks/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[forks-url]: https://github.com/unskript/awesome-cloudops-automation/network/members
[stars-shield]: https://img.shields.io/github/stars/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[stars-url]: https://github.com/unskript/awesome-cloudops-automation/stargazers
[issues-shield]: https://img.shields.io/github/issues/unskript/awesome-cloudops-automation.svg?style=for-the-badge
[issues-url]: https://github.com/unskript/awesome-cloudops-automation/issues
[twitter-shield]: https://img.shields.io/badge/-Twitter-black.svg?style=for-the-badge&logo=twitter&colorB=555
[twitter-url]: https://twitter.com/unskript
[awesome-shield]: https://img.shields.io/badge/awesome-cloudops-orange?style=for-the-badge&logo=bookstack 
