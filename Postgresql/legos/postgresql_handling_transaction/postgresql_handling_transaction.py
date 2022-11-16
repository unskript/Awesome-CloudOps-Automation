##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
import pprint

import psycopg2
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=2)
class InputSchema(BaseModel):
    transaction: str = Field(
        title='Commands',
        description='''
            PostgreSQL commands to be run inside a transaction. The commands should be ; separated. For eg:
            UPDATE test SET name = 'test-update3' WHERE _id = 3;
            UPDATE test SET name = 'test-update3' WHERE _id = 4;
        ''')


def postgresql_handling_transaction(handle, transaction:str):
  """postgresql_handling_transactions Runs postgres query with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type transaction: str
        :param transaction: PostgreSQL commands to be run inside a transaction.

        :rtype: Transaction Success message. Error if failed.
    """
  # Input param validation.

  command = "BEGIN;" + "\n" + transaction + "\n" + "COMMIT;"
  try:
      cur = handle.cursor()
      cur.execute(command)
      # close communication with the PostgreSQL database server
      cur.close()
      # commit the changes
      handle.commit()
      pp.pprint("Transaction completed successfully ")
  except (Exception, psycopg2.DatabaseError) as error:
      pp.pprint("Error in transaction Reverting all other operations of a transactions {}".format(error))
      handle.rollback()
  finally:
      if handle:
          handle.close()
          pp.pprint("PostgreSQL connection is closed")

  return
