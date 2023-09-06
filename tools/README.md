<center>
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h1> Tools Directory </h1>
</center>


# Static analysis on Runbooks

This tool can be used to run Static analysis on given given runbook. 

Here are the options to run the tool. You can either run static analysis on all the cells in a given runbook or just custom cells in the given runbook. (A custom cell is a code cell that is not created using unSkript Actions)
```
➭ ./runbook_sa.sh -h
usage: runbook-sa [-h] [-ra RA_RUNBOOKS] [-rc RC_RUNBOOKS]

Welcome to Runbook Static Analysis Tool VERSION: 0.1.0

options:
  -h, --help            show this help message and exit
  -ra RA_RUNBOOKS, --run-on-all-cells RA_RUNBOOKS
                        Run Static Analysis on cells in the notebook -ra Runbook1,Runbook2, etc..
  -rc RC_RUNBOOKS, --run-on-custom-cells RC_RUNBOOKS
                        Run Static Analysis only on cells in the notebook -rc Runbook1,Runbook2, etc..

This tool needs pyflakes and jupyter-lab to run
```

Here is a sample output

```
 ./runbook_sa.sh -rc notebook.ipynb
Analyzing notebook.ipynb

./custom_cell_contents_0.py:68:5 'json' imported but unused
./custom_cell_contents_0.py:100:35 undefined name 'namespace'
./custom_cell_contents_0.py:103:88 undefined name 'all_alpha_nodes'
./custom_cell_contents_0.py:154:5 local variable 'kubectl_delete_pvc_command' is assigned to but never used
./custom_cell_contents_0.py:179:5 local variable 'curl_cmds' is assigned to but never used
./custom_cell_contents_0.py:180:54 undefined name 'max_uid'
./custom_cell_contents_0.py:181:60 undefined name 'max_ts'
./custom_cell_contents_0.py:182:55 undefined name 'max_nsid'
./custom_cell_contents_0.py:185:36 undefined name 'zero_leader_node'
```