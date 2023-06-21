from __future__ import annotations

##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from slack_sdk import WebClient
## note: Your Slack App will need the users:read.email scope
# Otherwise you cannot access user's emails!



class InputSchema(BaseModel):
    email: str = Field(..., description='Email Address of user', title='email')



pp = pprint.PrettyPrinter(indent=2)



def slack_lookup_user_by_email_printer(output):
    if output is not None:
        pprint.pprint(output)
    else:
        return


def slack_lookup_user_by_email(
        handle: WebClient,
        email: str) -> Dict:


    try:
        response = handle.users_lookupByEmail(email=email)
        #print(response)
        return response['user']

    except Exception as e:
        print("\n\n")
        pp.pprint(
            f"Failed to find user, Error: {str(e)}")
        return f"Unable to send find user with email {email}"


