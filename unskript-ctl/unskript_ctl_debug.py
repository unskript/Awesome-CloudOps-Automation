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
import sys
import os
import time
import psutil 
import subprocess 

from tabulate import tabulate
from argparse import ArgumentParser, REMAINDER, SUPPRESS
from unskript_utils import *
from db_utils import * 

def start_debug(args):
    """start_debug Starts Debug session. This function takes
       the remote configuration as input and if valid, starts
       the debug session.
    """
    if not args:
        print("ERROR: Insufficient information provided")
        return 
    
    remote_config = args[0]
    remote_config = remote_config.replace('-','')

    if remote_config != "config":
        print(f"ERROR:The Allowed Parameter is --config, Given Flag is not recognized, --{remote_config}")
        return 
    try:
        remote_config_file = args[1]
    except:
        print(f"ERROR: Not able to find the configuration to start debug session")
        return 
    
    if os.path.exists(remote_config_file) is False:
        print(f"ERROR: Required Remote Configuration not present. Ensure {remote_config_file} file is present.")
        return 
    
    command = [f"openvpn --config {remote_config_file}"]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)

    # Lets give few seconds for the subprocess to spawn
    time.sleep(5)

    # Lets verify if the openvpn process is really running
    running = False
    for proc in psutil.process_iter(['pid', 'name']):
        # Search for openvpn process.
        if proc.info['name'] == "openvpn":
            # Lets make sure we ensure Tunnel Interface is Created and Up!
            intf_up_result = subprocess.run(["ip", "link", "show", "tun0"],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            if intf_up_result.returncode == 0:
                running = True
            break

    if running is True:
        print ("Successfully Started the Debug Session")
    else:
        print (f"Error Occured while starting the Debug Session {process}")

def stop_debug():
    """stop_debug Stops the Active Debug session.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        # Search for openvpn process. On Docker, we dont expect
        # Multiple process of openvpn to run.
        if proc.info['name'] == "openvpn":
            process = psutil.Process(proc.info['pid'])
            process.terminate()
            process.wait()

    print("Stopped Active Debug session successfully")



def debug_session_main():
    """debug_session_main: This function handles the debug sub option
    for unskript-ctl
    """
    dp = ArgumentParser()
    dp.add_argument("-d",
                        "--debug-session",
                        action="store_true",
                        help="Debug Options")
    dp.add_argument('--start',
                    help='Start debug session. Example [--start --config /tmp/config.ovpn]',
                    type=str,
                    nargs=REMAINDER)
    dp.add_argument('--stop',
                    help="Stop current debug session",
                    action='store_true')
    
    dpargs = dp.parse_args()
    if len(sys.argv) <= 2:
        dp.print_help()
        sys.exit(1)
    
    if dpargs.start not in ('', None):
        start_debug(dpargs.start)
    elif dpargs.stop == True:
        stop_debug()

    pass


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-d",
                         "--debug-session",
                        nargs=REMAINDER,
                        help="Debug Options")
    args = parser.parse_args()

    if len(sys.argv) <= 2: 
        parser.print_help()
        sys.exit(1)
    
    if args.debug_session:
        debug_session_main()