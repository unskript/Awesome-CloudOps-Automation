[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Twitter][twitter-shield]][twitter-url]
![Actions][actions-shield]
![Runbooks][runbooks-shield]

# Runbooks.sh
### Empowering Cloud Automation, Together
**[Explore our docs](https://docs.unskript.com)**   
*[Visit our blog](https://unskript.com/blog)* . *[Report Bug](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=bug_report.md&title=)* . *[Request Feature](https://github.com/unskript/Awesome-CloudOps-Automation/issues/new?assignees=&labels=&template=feature_request.md&title=)*

# 🚀 Quick Start Guide

We recommend using our docker setup which comes with Jupyter runtime along with pre-built [actions](https://docs.unskript.com/unskript-product-documentation/actions/what-is-an-action) and [runbooks](https://docs.unskript.com/unskript-product-documentation/readme/what-is-a-runbook). Build your own actions and runbooks with ease!

## Get Started

1. Launch Docker
```
docker run -it -p 8888:8888 --user root unskript/awesome-runbooks:latest
```
2. Point your browser to http://127.0.0.1:8888/awesome.



## Advanced Usage

In this section, we'll explore advanced configurations that enable:

1. Custom Action and Runbook creation
2. Custom Action creation using OpenAI integration

### Custom Action and Runbook Creation

1. Clone this repository to your local machine.
```bash
git clone https://github.com/unskript/Awesome-CloudOps-Automation
cd Awesome-CloudOps-Automation
```

2. Launch Docker 
  - Use this command to create custom runbooks and actions. (update the first -v line if you used a different directory in step 1).

```bash
docker run -it -p 8888:8888 \
 -v $HOME/Awesome-CloudOps-Automation/custom:/unskript/data \
 -v $HOME/.unskript:/unskript/credentials \
 -e ACA_AWESOME_MODE=1 \
 --user root \
 docker.io/unskript/awesome-runbooks:latest
```

3. Point your browser to http://127.0.0.1:8888/awesome.

### Custom Action Creation using OpenAI Integration

1. Clone this repository to your local machine if you haven't already.
```bash
git clone https://github.com/unskript/Awesome-CloudOps-Automation
cd Awesome-CloudOps-Automation
```

2. Launch Docker with OpenAI parameters:

  - Use this command to create custom GenAI actions (update the first -v line if you used a different directory in step 1).

```bash
docker run -it -p 8888:8888 \
 -v $HOME/Awesome-CloudOps-Automation/actions:/unskript/data/actions \
 -v $HOME/Awesome-CloudOps-Automation/runbooks:/unskript/data/runbooks \
 -v $HOME/.unskript:/unskript/credentials \
 -e ACA_AWESOME_MODE=1 \
 -e OPENAI_ORGANIZATION_ID=<your openAI org> \
 -e OPENAI_API_KEY=<your API key> \
 -e OPENAI_MODEL=GPT-4 \
 --user root \
 docker.io/unskript/awesome-runbooks:latest

```

The OPENAI parameters are used to initialize Generative AI creation with ChatGPT. They can be omitted from the command, but the generativeAI features will not be available.  For a list of models, visit [openAI](https://platform.openai.com/docs/models/overview).

3. Point your browser to http://127.0.0.1:8888/awesome.


You can find more information around how to use and play with our runbooks in the documentation here. You can find a list of all the runbooks along with links in the [repository page](/xrunbooks-directory.md) or simply use [unSkript CLI](unskript-ctl/README.md). 

## 📚 Documentation

Dive deeper into Runbooks.sh by visiting our comprehensive [documentation](https://docs.unskript.com/unskript-product-documentation/guides/getting-started). Here, you'll find everything you need to know about using the platform, creating custom runbooks, developing plugins, and much more.

# About the Project
Runbooks.sh is a powerful, community-driven, open-source runbook automation platform designed to simplify cloud infrastructure management and streamline operations across diverse environments. Few of the highlighting features:

- **Extensive Library**: Access hundreds of pre-built actions and runbooks to kickstart your automation journey.
- **Customization**: Create and modify actions and runbooks tailored to your unique requirements.
- **Generative AI Action Creation** Fully integrated with ChatGPT to create custom Actions in minutes.
- **Diverse Compatibility**: Seamlessly integrate with various cloud providers, platforms, and tools.
- **User-friendly Interface**: A Jupyter-based environment that simplifies runbook creation and execution.
- **Active Community**: Join a vibrant community of users and contributors committed to improving the project.

## 🏆 Mission
Our mission is to simplify CloudOps automation for DevOps and SRE teams by providing an extensive, community-driven repository of actions and runbooks that streamline day-to-day operations. 

## 👁️ Vision 
Our vision is to be the one-stop solution for all CloudOps automation needs, allowing DevOps and SRE teams to automate their workflows with ease, improve efficiency, and minimize toil.

## 🤝 Contributing
We welcome contributions from developers of all skill levels! Check out our [Contribution Guidelines](.github/CONTRIBUTING.md) to learn how you can contribute.

## 📖 License
Except as otherwise noted, this project is licensed under the *[Apache License, Version 2.0](/License)* .

## 🌐 Join Our Community
Connect with other users and contributors by joining our [Slack workspace](https://communityinviter.com/apps/cloud-ops-community/awesome-cloud-automation). Share your experiences, ask questions, and collaborate on this exciting project!

## 📣 Stay Informed
Keep up-to-date with the latest news, updates, and announcements by following us on [Twitter](https://twitter.com/UnSkript) and [Linkedin](https://www.linkedin.com/company/unskript-inc/).

Together, let's make Runbooks.sh the go-to solution for runbook automation and cloud infrastructure management!

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
[actions-shield]: https://img.shields.io/badge/ActionsCount-476-orange?style=for-the-badge 
[runbooks-shield]:https://img.shields.io/badge/xRunbooksCount-61-green?style=for-the-badge
