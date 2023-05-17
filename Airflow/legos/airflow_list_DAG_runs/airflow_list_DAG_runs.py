##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Dict
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=4)

class InputSchema(BaseModel):
    dag_id: Optional[str] = Field(
        default=None,
        title='Dag ID',
        description='The DAG ID')


def airflow_list_DAG_runs_printer(output):
    if output is None:
        return
    print("\n")
    pp.pprint(output)


def airflow_list_DAG_runs(handle,  dag_id: str = "") -> Dict:
    """airflow_list_DAG_runs list dag runs

        :type dag_id: str
        :param dag_id: The DAG ID.

        :rtype: Dict of Dag runs
    """
    return handle.list_DAG_runs(dag_id=dag_id if dag_id else None)
