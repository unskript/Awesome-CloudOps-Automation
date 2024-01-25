*  unskript-ctl.sh run --info 
```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run --info
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run check --name <NAME>

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```


*  unskript-ctl.sh run check --type <TYPE>

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --type k8s 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run --script <SCRIPT>

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run --script "/usr/local/bin/lb_pvc.sh" 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unksirpt-ctl.sh run --script <SCRIPT> --info
```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run --script "/usr/local/bin/lb_pvc.sh"  --info
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```


*  unskript-ctl.sh run check --name <NAME> --info 

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes  --info
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run check --type <TYPE> --info 
```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --type k8s  --info
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py

```

*  unskript-ctl.sh run check --name <NAME> --script <SCRIPT>
```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes  --script "/usr/local/bin/lb_pvc.sh"  
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run check --type <TYPE> --script <SCRIPT>
```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --type k8s  --script "/usr/local/bin/lb_pvc.sh"  
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```
*  unskript-ctl.sh run check --name <NAME> check --type <TYPE> 

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes ; /usr/local/bin/unskript-ctl.sh run check --type k8s 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```


*  unskript-ctl.sh run check --type <TYPE> check --name <NAME> --script <SCRIPT>

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes ; /usr/local/bin/unskript-ctl.sh run check --type k8s  --script "/usr/local/bin/lb_pvc.sh"  
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run check --type <TYPE> --script <SCRIPT> --info 

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --type k8s --info --script "/usr/local/bin/lb_pvc.sh" 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run check --name <NAME> --script <SCRIPT> --info 
```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes --info --script "/usr/local/bin/lb_pvc.sh" 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py

```

*  unskript-ctl.sh run check --name <NAME> check --type <TYPE> --info  

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes  --info; /usr/local/bin/unskript-ctl.sh run check --type k8s  --script "/usr/local/bin/lb_pvc.sh" 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```

*  unskript-ctl.sh run check --name <NAME> check --type <TYPE> --script <SCRIPT> --info 

```
Schedule: cadence 0 0 * * *, job name: lightbeam
Schedule: Programming crontab 0 0 * * * /usr/local/bin/unskript-ctl.sh run check --name k8s_get_offline_nodes  --info; /usr/local/bin/unskript-ctl.sh run check --type k8s --info --script "/usr/local/bin/lb_pvc.sh" 
Adding audit log deletion cron job entry, 0 0 * * * /opt/conda/bin/python /usr/local/bin/unskript_audit_cleanup.py
```