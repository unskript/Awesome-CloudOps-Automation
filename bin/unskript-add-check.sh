#!/bin/bash

# Add check script
#     This script can be used to create new checks.

TOPDIR=$(git rev-parse --show-toplevel)
AWESOME_DIRECTORY=Awesome-CloudOps-Automation
/usr/bin/env python $TOPDIR/$AWESOME_DIRECTORY/unskript-ctl/unskript-add-check.py "$@"
