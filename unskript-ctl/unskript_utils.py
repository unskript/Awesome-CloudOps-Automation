#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#

UNSKRIPT_EXECUTION_DIR="/unskript/data/execution/"
PSS_DB_PATH="/unskript/db/unskript_pss.db"
GLOBAL_CTL_CONFIG="/etc/unskript/unskript_ctl_config.yaml"
CREDENTIAL_DIR="/.local/share/jupyter/metadata/credential-save"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ARG_START = '\x1B[1;20;42m'
    ARG_END = '\x1B[0m'
