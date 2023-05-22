##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint
import psycopg2
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=2)
class InputSchema(BaseModel):
    query: str = Field(
        title='Delete Query',
        description='Postgres delete query.')


def postgresql_delete_query(handle, query:str):
  """postgresql_delete_query Runs postgres query with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type query: str
        :param query: Postgresql Delete query.

        :rtype: All the results of the query.
    """
  # Input param validation.

  delete_statement = query
  try:
      cur = handle.cursor()
      cur.execute(delete_statement)
      # get the number of updated rows
      rows_deleted = cur.rowcount

      # Commit the changes to the database
      handle.commit()
      # Close communication with the PostgreSQL database
      cur.close()
      print("\n")
      pp.pprint("Deleted Record successfully")
      pp.pprint(f"The number of deleted rows: {rows_deleted}")

  except (Exception, psycopg2.DatabaseError) as error:
      pp.pprint(f"Error : {error}")
  finally:
      if handle:
          handle.close()
          pp.pprint("PostgreSQL connection is closed")
