#!/bin/bash

# unSkript Control Script 
#     This script can be used to list all available runbook
#     and Run the runbook

exec_path=$PWD
cd /usr/local/bin
EXEC_PATH=$exec_path /usr/bin/env python ./unskript-client.py "$@"
