#!/bin/bash

# Add creds script
#     This script can be used to add credentials.

if test -f "/usr/local/bin/unskript-add-check.py"; then
	cd /usr/local/bin
	/usr/bin/env python /usr/local/bin/unskript-add-check.py "$@"
else
	TOPDIR=$(git rev-parse --show-toplevel)
    	AWESOME_DIRECTORY=Awesome-CloudOps-Automation
	/usr/bin/env python $TOPDIR/$AWESOME_DIRECTORY/unskript-ctl/unskript-add-check.py "$@"
fi
