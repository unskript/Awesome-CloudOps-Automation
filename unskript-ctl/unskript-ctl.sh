#!/bin/bash

# unSkript Control Script
#     This script can be used to list all available runbook
#     and Run the runbook

cd /usr/local/bin
if [ -f "/opt/conda/bin/python" ];
then
    /opt/conda/bin/python ./unskript_ctl.py "$@"
elif [ -f "/opt/unskript/bin/python" ];
then
    /opt/unskript/bin/python ./unskript_ctl.py "$@"
else
    /usr/bin/env python ./unskript_ctl.py "$@"
fi
