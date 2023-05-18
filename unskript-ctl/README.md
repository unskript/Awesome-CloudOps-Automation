# unSkript CLI

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

 # unskript-ctl Actions 

* [Db utils.py](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/unskript-ctl/legos/db_utils) 
* [Unskript client.py](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/unskript-ctl/legos/unskript-client) 
