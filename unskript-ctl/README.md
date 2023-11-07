# unSkript CLI


unskript-ctl is a command line tool which allows you to run checks against your
resources, be it infrastructure or your own services.

Here are the options that are supported by the uskript-ctl command
```
unskript-ctl.sh
usage: unskript-ctl [-h] [-l ...] [-r ...] [-s ...] [-d ...] [--create-credential ...]

Welcome to unSkript CLI Interface VERSION: 0.1.0

optional arguments:
  -h, --help            show this help message and exit
  -l ..., --list ...    List Options
  -r ..., --run ...     Run Options
  -s ..., --show ...    Show Options
  -d ..., --debug ...   Debug Options
  --create-credential ...
                        Create Credential [-creds-type creds_file_path]
```

## List options
```
usage: unskript_ctl.py [-h] [-r] [--failed-checks ...] [-c ...] [--credential]

optional arguments:
  -h, --help            show this help message and exit
  -r, --runbooks        List Runbooks
  --failed-checks ...   List Failed checks
  -c ..., --checks ...  List Checks
  --credential          List Credential
```

## Run options
Using the **--run** option, you can run check(s), scripts and runbooks.
Also, if you want to get the report of the run in an email or slack, you can
use the **--report** option.

```
usage: unskript_ctl.py [-h] [--script SCRIPT] [--runbook [RUNBOOK ...]] [--check [CHECK ...]] [--report]

optional arguments:
  -h, --help            show this help message and exit
  --script SCRIPT       Run script
  --runbook [RUNBOOK ...]
                        Run the given runbook FILENAME [-RUNBOOK_PARM1 VALUE1] etc..
  --check [CHECK ...]   Run checks
  --report              Report results
```

## Show options
```
usage: unskript_ctl.py [-h] [--audit-trail ...] [--failed-logs ...]

optional arguments:
  -h, --help         show this help message and exit
  --audit-trail ...  Show Audit Trail
  --failed-logs ...  Show Failed Logs
```

## Debug options

Using the **--debug** option, you can connect this pod to the upstream VPN
server, so that you can access this pod from the control unSkript portal.
```
usage: unskript_ctl.py [-h] [--start ...] [--stop]

optional arguments:
  -h, --help   show this help message and exit
  --start ...  Start debug session. Example [--start --config /tmp/config.ovpn]
  --stop       Stop current debug session
```