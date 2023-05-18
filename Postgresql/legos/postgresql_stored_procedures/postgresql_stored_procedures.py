##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import Any, List
import psycopg2
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    stored_procedure_name: str = Field(
        title='Stored procedure name.',
        description='PostgreSQL stored procedure name.')
    params: list = Field(
        None,
        title='Parameters',
        description='Parameters to the Stored Procedure in list format. For eg: [1, 2]')


def postgresql_stored_procedures(handle, stored_procedure_name: str, params: List = List[Any]):
    """postgresql_stored_procedures Runs postgres query with the provided parameters.

          :type handle: object
          :param handle: Object returned from task.validate(...).

          :type stored_procedure_name: str
          :param stored_procedure_name: PostgreSQL stored procedure name.

          :type params: List
          :param params: Parameters to the Stored Procedure  in list format.

          :rtype: All the results of the Stored Procedure .
      """
    # Input param validation.

    try:
        cur = handle.cursor()

        if params:
            query = f"CALL {stored_procedure_name}"
            cur.execute(query, params)
        else:
            query = f"CALL {stored_procedure_name}"
            cur.execute(query)

        # commit the transaction
        handle.commit()
        # Close communication with the PostgreSQL database
        cur.close()
        print("Call PostgreSQL Stored Procedures successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error : {error}")
    finally:
        if handle:
            handle.close()
            print("PostgreSQL connection is closed")
