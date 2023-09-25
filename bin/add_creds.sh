#!/bin/bash

# Add creds script
#     This script can be used to add credentials.

if test -f "/usr/local/bin/add_creds.py"; then
	/usr/bin/env python ./add_creds.py "$@"
else
	TOPDIR=$(git rev-parse --show-toplevel)
    	AWESOME_DIRECTORY=Awesome-CloudOps-Automation
	/usr/bin/env python $TOPDIR/$AWESOME_DIRECTORY/unskript-ctl/add_creds.py "$@"
fi
