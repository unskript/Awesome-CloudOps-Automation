#!/usr/bin/env python
##
##  Copyright (c) 2022 unSkript, Inc
##  All rights reserved.
##
"""Tests for `unskript` package."""

from unskript.fwk.workflow import Task, Workflow
from unskript.legos.azure.azure_get_handle.azure_get_handle import azure_get_handle, InputSchema
from unskript.secrets import ENV_MODE, ENV_MODE_AWS


def test_azure_get_handle():
    env = {ENV_MODE: ENV_MODE_AWS, "AWS_REGION": "us-west-2"}
    secret_store_cfg = {"AWS_SECRET_PREFIX": "test", "AWS_REGION": "us-west-2",
                        "SECRET_STORE_TYPE": "SECRET_STORE_TYPE_AWS"}
    w = Workflow(env, secret_store_cfg, None)

    # credentialsJson will be inserted by the jupyter extension on connector selection from the drop down.
    credentialsJson = """{"credential_type": "CONNECTOR_TYPE_AZURE", "credential_id":"test", "credential_name": "test" }"""

    t = Task(Workflow())
    t.configure(credentialsJson=credentialsJson)
    (err, hdl, args) = t.validate(InputSchema, vars())
    if err is None:
        t.output = t.execute(azure_get_handle, hdl, args)

    print(t.output)
    assert t.workflow.global_vars['unskript_task_error'] is None
    assert t.output != None
