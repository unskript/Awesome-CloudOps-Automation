##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
from pymongo.errors import *

'''
Collection of utility function used by MongoDB legos
'''

def reachable(handle) -> bool:
    retval = False
    try:
        handle.server_info()
        retval = True
    except (pymongo.errors.AutoReconnect, pymongo.errors.ServerSelectionTimeoutError) as e:
        print("[UNSKRIPT]: Reconnection / Server Selection Timeout Error: ", e.__str__())
        raise e
    except Exception as e:
        print("[UNSKRIPT]: Error Connecting: ", e.__str__())
        raise e

    return retval
