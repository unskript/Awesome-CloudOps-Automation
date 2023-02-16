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
    CloudOps automation made simple!
    <br />
    <a href="https://docs.unskript.com/unskript-product-documentation/open-source/cloudops-automation-with-unskript"><strong>Explore the docs »</strong></a>
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
Simplify CloudOps automation for developers and DevOps engineers. 

## Vision 
A single repository to satisfy all your day-to-day CloudOps automation needs. Automate your workflows with our `Actions` that build automated `Runbooks`. 

>Are you looking for a script to automate your Kubernetes management? A script to restart the pod that is OOMkilled?  We've got you covered. 



___
<br>

# Quick Start Guide

Get up and running quickly:

## Get started with Docker:

```
docker run -it -p 8888:8888 \
 -v $HOME/.unskript:/data \
 --user root \
 docker.io/unskript/awesome-runbooks:latest
```

## [Cloud Sandbox](https://us.app.unskript.io/)
* A free Cloud version of the OSS offering.

## Open and Use a xRunBook
Once your Docker image is up and running, unSkript will be running locally on your computer at http://127.0.0.1:8888/lab/tree/Welcome.ipynb.  A table lists the xRunBooks that are available, with a link to the description and a link to the local version of the xRunBook.

Click on the URL of the xRunBook you would like to explore. It will open in a new browser tab. To run this XRunBook:

1. Check the `Parameters` button at the top of the page. This lists all of the input parameters, and the default values.  Change them if needed.
2. Click on each Action in the xRunBook.  The `Configurations` button will show if Credentials are needed, and which inputs are used for each action. [How to Add Credentials](https://docs.unskript.com/unskript-product-documentation/guides/connectors).
3. Once each Action has been assigned Credentials and inputs, run each Action (in order) to run your xRunBook.

## Included xRunBooks 

These xRunBooks are included in every install.  Use them as is, or make a copy to modify for your use!

| **Category**                                                                                               | **Runbooks**                                                                                                                                                                 | **URL**                                                                                                    |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |



# Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Check out our [Contribution Guidelines](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/CONTRIBUTING.md) for more details. 

## How to Contribute?

1. Work with us on any of our [open issues](https://github.com/unskript/awesome-cloudops-automation/issues).
2. Create a new Action. Read the [Action developer guide](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/DEVELOPERGUIDE.md) for more details.
3. Combine Actions into a xRunBook.  Your xRunBook will be featured on the ReadMe.  [What's a xRunBook?](https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/Anatomy-of-Runbook.md)



## Contribution Tips:
1. Use the [Docker environment](#get-started-with-docker), or our free [cloud sandbox](https://us.app.unskript.io/profiles/6c38d3da1cde7b3c0623d138f525a5508a3260c8) for testing your contribution.
2. Join our [Slack Community](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) so you can present yourself and get support.



## Create a new xRunBook:
  
  - **Using Docker**:
    1. Your RunBooks are stored locally at ```$HOME/.unskript/runbooks``` Copy an existing xRunBook, rename it and then restart Docker.
    2. Point your browser to `http://127.0.0.1:8888/doc/tree/<YOUR_RUNBOOK_NAME.ipynb>` to begin editing.
  - **unSkript Sandbox**:
    1. The onboarding flow will drop you into Runbook creation with sandbox credentials
    2.  Start building your lego from the proposed handle (GCP, k8s et al)
  1. Submit Your xRunBook to the repository Follow the [submission steps](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source) to remove credentials, etc. from your xRunBook.
  2. Submit a PR!

## Import a xRunBook
  1. xRunBooks are stored locally at ```$HOME/.unskript/runbooks``` . Place your existing RunBook in this directory.
  2. Restart your Docker instance.
  3. Point your browser to `http://127.0.0.1:8888/doc/tree/<YOUR_RUNBOOK_NAME.ipynb>` to begin using your xRunBook.

## Create a new Action:

1. Creating a new Action is simple:  
   1. If you will not use external credentials, click *+Add Action* at the top of the menu.
   2. If you will be using an existing credential, add an existing ACtion for that service (like AWS), and edit the code to create your new Action.
    3. If you are creating a new credential, reach out to the team - we'd love to help!
2. [Creating Custom Actions](https://docs.unskript.com/unskript-product-documentation/guides/actions/create-custom-actions) describes the steps to create your own Action.
3.  To submit to OSS, follow the [Submit An Action](https://docs.unskript.com/unskript-product-documentation/guides/contribute-to-open-source#actions) instructions.  


<br/>


# Community
[Join the CloudOps Community Slack Channel](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation) to connect with other users, contributors and awesome people behind awesome CloudOps automation project. 

<br/>

# Roadmap

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
