from typing import List
from pydantic import BaseModel, Field
import pprint
from tabulate import tabulate

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    query: str = Field(
        title='Query',
        description='Query to read data')
    db_name: str = Field(
        title='Database name',
        description='Name of the database to use')
    schema_name: str = Field(
        title='Schema name',
        description='Name of the Schema to use')


def snowflake_read_query_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def snowflake_read_query(handle, query: str, db_name: str, schema_name: str) -> List:
    """snowflake_read_query Runs query with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type query: str
        :param query: Query to read data.

        :type db_name: str
        :param db_name: Name of the database to use.

        :type schema_name: str
        :param schema_name: Name of the Schema to use

        :rtype: List if success. Exception on error.
      """
    # Input param validation.

    cur = handle.cursor()
    cur.execute("USE DATABASE " + db_name)
    cur.execute("USE SCHEMA " + schema_name)
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    handle.close()
    return res
