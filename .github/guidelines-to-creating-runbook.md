[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 

<h1>Guideline for creating reusable runbooks </h1>

<br>

## 1 Introduction

A Runbook is a collection of `Actions` which accomplish a well defined task. A runbook is intended to be written once and used multiple times. So re-usability means the runbook needs to be `parameterized`.  Parameterization of a runbook is the process wherein we define what are the Inputs expected to the runbook. For instance, if we are authoring a runbook to list and delete all unused key-pairs in AWS, then we can think of `AWS region` as an `input parameter` for this runbook. 

This document lists such guidelines when creating  re-usable runbooks.


## 2 Guidelines

1. To make runbook portable and re-usable we should not hard-code any values like `aws region` in the runbook. It should instead be taken as an input parameter to the runbook.
2. It is customary to have a `markdown` cell preceding the `Action` cell wherein we explain what is being done in the `Action` cell. Like any good code, Runbook with adequate `markdown` cells increases readability of the runbook.
3. A runbook should have a clear `Steps` markdown cell wherein every step that is taken in the runbook is clearly explained. 
4. A runbook can have unSkript `Action` and/or custom `Action` cells. But every `Action` cell should be preceded with a `markdown` cell explaining what is the intent of the `Action` cell.
5. A runbook shall list all the outputs clearly formatted and easy to read and understand. 
6. A runbook shall have a `Conclusion` markdown cell which summarizes what was done in the runbook. We may also include any links to help in debugging the issue that the runbook set out to solve. 


## 3 Runbook Etiquette

1. Make sure there are no hard-coded values in the runbook. No magic variables in the runbook. Any variable being used should be well documented in the `Action` cell or in the `Markdown` cell.
2. Keep the structure of the runbook in the form of `Markdown` followed by `Action`
3. A Remediation section would help user know what are the next steps to take to resolve the issue at hand. 
4. If a remediation is known Eg: Pruning un-used key-pairs in a region, then the runbook should provide an `Action` to achieve the desired remediation to the user.  If it is not known, then the Runbook should offer Links to where further troubleshooting can be done. 