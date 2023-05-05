##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Optional, Dict

from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=4)

class InputSchema(BaseModel):
    dag_id: str = Field(
        title='Dag ID',
        description='The DAG ID')

    dag_run_id: Optional[str] = Field(
        None,
        title='Run ID',
        description= '''The value of this field can be set only when creating the object.
        If you try to modify the field of an existing object, the request fails with an
        BAD_REQUEST error''')

    logical_date: Optional[str] = Field(
        None,
        title='logical date',
        description='''The logical date (previously called execution date). This is the time
        or interval covered by this DAG run, according to the DAG definition
        eg: 2019-08-24T14:15:22Z''')

    conf: Optional[dict] = Field(
        None,
        title='conf',
        description='JSON object describing additional configuration parameters')


def airflow_trigger_dag_run_printer(output):
    if output is None:
        return
    print("\n")
    pp.pprint(output)


def airflow_trigger_dag_run(handle,
                            dag_id: str,
                            conf: dict = None,
                            dag_run_id: str = "",
                            logical_date: str = "") -> Dict:

    """airflow_trigger_dag_run trigger dag run

        :type dag_id: str
        :param dag_id: The DAG ID'.

        :type conf: str
        :param conf: JSON object describing additional configuration parameters.

        :type dag_run_id: str
        :param dag_run_id: The value of this field can be set only when creating the object.

        :type logical_date: str
        :param logical_date: The logical date (previously called execution date).

        :rtype: Dict of DAG run info
    """
    return handle.trigger_dag_run(dag_id,
                                  conf,
                                  dag_run_id= dag_run_id if dag_run_id else None,
                                  logical_date=logical_date if logical_date else None)
