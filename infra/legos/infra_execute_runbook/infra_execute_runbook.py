##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint

from pydantic import BaseModel, Field
from typing import Optional


class unSkriptCustomType(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            fetch_runbook_list='true'
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        return cls(f'{v}')

    def __repr__(self):
        return f'{super().__repr__()}'

class InputSchema(BaseModel):
    runbook_id: unSkriptCustomType = Field(
        title='Runbook ID',
        description='ID of the runbook'
    )
    params: Optional[str] = Field(
        title='Runbook parameters',
        description='Parameters to the runbook as json string.'
    )

def infra_execute_runbook_printer(output):
    if output is not None:
        pprint.pprint(f"Runbook execution status: {output}")

def infra_execute_runbook(handle, runbook_id: str, params: str = None) -> str:
    """execute_runbook executes particular runbook annd return execution status

        :type runbook_id: str.
        :param runbook_id: ID of the runbook to execute.

        :type params: str.
        :param params: JSON string of runbook input parameters.

        :rtype: str.
    """
    try:
        execution_status = handle.execute_runbook(runbook_id, params)
        return execution_status
    except Exception as e:
        raise e
