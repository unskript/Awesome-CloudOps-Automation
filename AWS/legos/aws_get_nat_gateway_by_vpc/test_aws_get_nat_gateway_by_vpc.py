#!/usr/bin/env python
##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
"""Tests for `unskript` package."""

from unskript.legos.aws.aws_get_nat_gateway_by_vpc.aws_get_nat_gateway_by_vpc import aws_get_natgateway_by_vpc, InputSchema, aws_get_natgateway_by_vpc_printer
from unskript.fwk.workflow import Task, Workflow
from unskript.secrets import ENV_MODE, ENV_MODE_AWS
import os


def test_aws_get_natgateway_by_vpc():
    env = {ENV_MODE: ENV_MODE_AWS, "AWS_REGION": "us-west-2"}
    secret_store_cfg = {"AWS_SECRET_PREFIX": "test", "AWS_REGION": "us-west-2", "SECRET_STORE_TYPE": "SECRET_STORE_TYPE_AWS"}
    w = Workflow(env, secret_store_cfg, None)
    # credentialsJson will be inserted by the jupyter extension on connector selection from the drop down.
    if os.environ.get('GITHUB_CICD'):
        credentialsJson = """{"credential_type": "CONNECTOR_TYPE_AWS", "credential_id":"github", "credential_name": "github" }"""
    else:
        credentialsJson = """{"credential_type": "CONNECTOR_TYPE_AWS", "credential_id":"test", "credential_name": "test" }"""
    inputParamsJson = '''
                    {
                        "vpc_id": "\\"vpc-0a9ef7ec0830615a1\\"",
                        "region": "\\"us-west-2\\""
                    }
                    '''
    t = Task(Workflow())
    t.configure(inputParamsJson, credentialsJson)
    (err, hdl, args) = t.validate(InputSchema, vars())
    if err is None:
        t.output = t.execute(aws_get_natgateway_by_vpc, hdl, args, aws_get_natgateway_by_vpc_printer)
    assert t.workflow.global_vars['unskript_task_error'] == None
    assert t.output[0] != None
    assert isinstance(t.output[0], dict)
    assert "error" not in t.output[0]
