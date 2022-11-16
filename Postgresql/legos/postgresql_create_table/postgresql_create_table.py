##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import Dict

import psycopg2
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    commands: list = Field(
        title='Commands to create tables',
        description='''
            Postgres create table.
            For eg. ["CREATE TABLE test (_id SERIAL PRIMARY KEY, _name VARCHAR(255) NOT NULL)",
            "CREATE TABLE foo (_id SERIAL PRIMARY KEY)"]
        ''')


def postgresql_create_table_printer(output):
    print("\n")
    print(output)
    return output


def postgresql_create_table(handle, commands: tuple) -> Dict:
    """postgresql_create_table Runs postgres query with the provided parameters.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type commands: tuple
        :param commands: Commands to create tables.

        :rtype: All the results of the query.
      """
    # Input param validation.

    output = {}
    try:
        cur = handle.cursor()
        # create table one by one
        for command in tuple(commands):
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        handle.commit()
        output['result'] = 'Tables Created Sucessfully'
    except (Exception, psycopg2.DatabaseError) as error:
        output["result"] = error
    finally:
        if handle:
            handle.close()

    return output
