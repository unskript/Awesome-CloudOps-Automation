from typing import Dict
from pydantic import BaseModel, Field
import pprint

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    query: str = Field(
        title='Query',
        description='Query to write data')
    db_name: str = Field(
        title='Database name',
        description='Name of the database to use')
    schema_name: str = Field(
        title='Schema name',
        description='Name of the Schema to use')

def snowflake_write_query_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def snowflake_write_query(handle, query: str, db_name: str, schema_name: str) -> Dict:
    """snowflake_write_query Runs query with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type query: str
        :param query: Query to read data.

        :type db_name: str
        :param db_name: Name of the database to use.

        :type schema_name: str
        :param schema_name: Name of the Schema to use

        :rtype: Dict if success. Exception on error.
      """
    # Input param validation.
    result = {}
    cur = handle.cursor()
    cur.execute("USE DATABASE " + db_name)
    cur.execute("USE SCHEMA " + schema_name)
    cur.execute(query)
    result["Result"] = "The query executed successfully!"
    cur.close()
    handle.close()
    return result
