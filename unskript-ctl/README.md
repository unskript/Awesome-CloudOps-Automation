# unSkript CLI


unskript-ctl is a command line tool which allows you to run checks against your
resources, be it infrastructure or your own services.

Here are the options that are supported by the uskript-ctl command
```
unskript-ctl.sh
usage: unskript-ctl [-h] [--create-credential ...] {run,list,show,debug} ...

Welcome to unSkript CLI Interface VERSION: 1.1.0 BUILD_NUMBER: 1.1.0

positional arguments:
  {run,list,show,debug}
                        Available Commands
    run                 Run Options
    list                List Options
    show                Show Options
    debug               Debug Option

options:
  -h, --help            show this help message and exit
  --create-credential ...
                        Create Credential [-creds-type creds_file_path]
```

## Run options
Using the **run** option, you can run check(s), scripts and runbooks.
Also, if you want to get the report of the run in an email or slack, you can
use the **--report** option.

```
usage: unskript-ctl run [-h] [--script SCRIPT] [--report] {check} ...

positional arguments:
  {check}
    check          Run Check Option

options:
  -h, --help       show this help message and exit
  --script SCRIPT  Script name to run
  --report         Report Results
```

```
usage: unskript-ctl run check [-h] [--name NAME] [--type TYPE] [--all]

options:
  -h, --help   show this help message and exit
  --name NAME  Check name to run
  --type TYPE  Type of Check to run
  --all        Run all checks
```

## List options
```
usage: unskript-ctl list [-h] [--credential] {checks,failed-checks} ...

positional arguments:
  {checks,failed-checks}
    checks              List Check Options
    failed-checks       List Failed check options

options:
  -h, --help            show this help message and exit
  --credential          List All credentials
```

```
usage: unskript-ctl list checks [-h] [--all]
                                [--type {aws,gcp,k8s,elasticsearch,grafana,redis,jenkins,github,netbox,nomad,jira,kafka,mongodb,mysql,postgresql,rest,slack,ssh,vault,salesforce}]

options:
  -h, --help            show this help message and exit
  --all                 List All Checks
  --type {aws,gcp,k8s,elasticsearch,grafana,redis,jenkins,github,netbox,nomad,jira,kafka,mongodb,mysql,postgresql,rest,slack,ssh,vault,salesforce}
                        List All Checks of given connector type
```

```
usage: unskript-ctl list failed-checks [-h] [--all]
                                       [--type {aws,gcp,k8s,elasticsearch,grafana,redis,jenkins,github,netbox,nomad,jira,kafka,mongodb,mysql,postgresql,rest,slack,ssh,vault,salesforce}]

options:
  -h, --help            show this help message and exit
  --all                 Show All Failed Checks
  --type {aws,gcp,k8s,elasticsearch,grafana,redis,jenkins,github,netbox,nomad,jira,kafka,mongodb,mysql,postgresql,rest,slack,ssh,vault,salesforce}
                        List All Checks of given connector type
```



## Show options
```
usage: unskript-ctl show [-h] {audit-trail,failed-logs} ...

positional arguments:
  {audit-trail,failed-logs}
    audit-trail         Show Audit Trail option
    failed-logs         Show Failed Logs option

options:
  -h, --help            show this help message and exit
```
```
usage: unskript-ctl show audit-trail [-h] [--all]
                                     [--type {aws,gcp,k8s,elasticsearch,grafana,redis,jenkins,github,netbox,nomad,jira,kafka,mongodb,mysql,postgresql,rest,slack,ssh,vault,salesforce}]
                                     [--execution_id EXECUTION_ID]

options:
  -h, --help            show this help message and exit
  --all                 List trail of all checks across all connectors
  --type {aws,gcp,k8s,elasticsearch,grafana,redis,jenkins,github,netbox,nomad,jira,kafka,mongodb,mysql,postgresql,rest,slack,ssh,vault,salesforce}
                        Show Audit trail for checks for given connector
  --execution_id EXECUTION_ID
                        Execution ID for which the audit trail should be shown
```
```
usage: unskript-ctl show failed-logs [-h] [--execution_id EXECUTION_ID]

options:
  -h, --help            show this help message and exit
  --execution_id EXECUTION_ID
                        Execution ID for which the logs should be fetched
```

## Debug options

Using the **debug** option, you can connect this pod to the upstream VPN
server, so that you can access this pod from the control unSkript portal.
```
usage: unskript-ctl debug [-h] [--start ...] [--stop]

options:
  -h, --help   show this help message and exit
  --start ...  Start debug session. Example [--start --config /tmp/config.ovpn]
  --stop       Stop debug session
```