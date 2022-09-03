##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
import polling2
from pydantic import BaseModel, Field
from mongodb.legos.mongodb_util import reachable

from beartype import beartype


class InputSchema(BaseModel):
    op_id: int = Field(
        title='Operation ID',
        description='Kill the operation based on operation id, Eg 12231, 323432'
    )


def mongodb_kill_queries_printer(output):
    if output is None:
        return
    print("\n\n")
    pprint.pprint(output)


def check_id_exists(handle, op_id) -> bool:
    ids = handle.admin.command(({"currentOp": True}))
    current_ids = [o['opid'] for o in ids['inprog']]
    return op_id in current_ids

@beartype
def mongodb_kill_queries(handle, op_id: int) -> Dict:
    """mongodb_kill_queries can kill queries (read operations) that are
       running on more than one shard in a cluster.

        :type handle: object
        :param handle: Object returned by task.validate(...).

        :type op_id: int
        :param op_id: Operation ID as integer that needs to be killed

        :rtype: Result of the killOp operation for the given op_id in a Dict form.
    """
    # Check the MongoDB
    try:
        reachable(handle)
    except Exception as e:
        raise e
    try:
        resp = handle.admin.command("killOp", op=op_id)
        if resp.get('ok') == 1:
            # Let us make sure when the KillOp was issued, it
            # really did kill the query identified by the id.
            # Poll for 10 seconds, if it does not return False
            # raise Exception. else return success message
            try:
                polling2.poll(lambda: check_id_exists(handle, op_id),
                              check_success=polling2.is_value(False),
                              step=1,
                              timeout=10)
                return {'info': f'Successfully Killed OpID {op_id}', 'ok': 1}
            except Exception as e:
                raise e
        else:
            raise Exception("Unable to Get Response from server for killOp command")
    except Exception as e:
        raise e
