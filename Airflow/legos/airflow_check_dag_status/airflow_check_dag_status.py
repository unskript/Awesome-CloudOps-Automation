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
        None,
        title='Dag ID',
        description='The DAG ID')


def airflow_check_dag_status_printer(output):
    if output is None:
        return
    print(type(output))
    pprint.pprint(output)


def airflow_check_dag_status(handle, dag_id: str = "") -> Dict:
    """airflow_check_dag_status check dag status

        :type dag_id: str
        :param dag_id: The DAG ID.

        :rtype: Dict of DAG status
    """
    dag = handle.check_dag_status(dag_id=dag_id if dag_id else None)
    return dag
