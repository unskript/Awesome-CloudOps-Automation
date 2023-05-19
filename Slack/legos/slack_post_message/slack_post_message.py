##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from pydantic import BaseModel, Field
from beartype import beartype
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

pp = pprint.PrettyPrinter(indent=2)

class InputSchema(BaseModel):
    channel: str = Field(
        title='Channel',
        description='Name of slack channel.')
    message: str = Field(
        title='Message',
        description='Message for slack channel.')

@beartype
def slack_post_message_printer(output):
    if output is not None:
        pprint.pprint(output)
    else:
        return


@beartype
def slack_post_message(
        handle: WebClient,
        channel: str,
        message: str) -> str:

    try:
        handle.chat_postMessage(
            channel=channel,
            text=message)
        return f"Successfully Sent Message on Channel: #{channel}"
    except SlackApiError as e:
        pp.pprint(
            f"Failed sending message to slack channel {channel}, Error: {e.response['error']}")
        if e.response['error'] == 'channel_not_found':
            raise Exception('Channel Not Found') from e
        if e.response['error'] == 'duplicate_channel_not_found':
            raise Exception('Channel associated with the message_id not valid') from e
        if e.response['error'] == 'not_in_channel':
            raise Exception('Cannot post message to channel user is not in') from e
        if e.response['error'] == 'is_archived':
            raise Exception('Channel has been archived') from e
        if e.response['error'] == 'msg_too_long':
            raise Exception('Message text is too long') from e
        if e.response['error'] == 'no_text':
            raise Exception('Message text was not provided') from e
        if e.response['error'] == 'restricted_action':
            raise Exception('Workspace preference prevents user from posting') from e
        if e.response['error'] == 'restricted_action_read_only_channel':
            raise Exception('Cannot Post message, read-only channel') from e
        if e.response['error'] == 'team_access_not_granted':
            raise Exception('The token used is not granted access to the workspace') from e
        if e.response['error'] == 'not_authed':
            raise Exception('No Authtnecition token provided') from e
        if e.response['error'] == 'invalid_auth':
            raise Exception('Some aspect of Authentication cannot be validated. Request denied') from e
        if e.response['error'] == 'access_denied':
            raise Exception('Access to a resource specified in the request denied') from e
        if e.response['error'] == 'account_inactive':
            raise Exception('Authentication token is for a deleted user') from e
        if e.response['error'] == 'token_revoked':
            raise Exception('Authentication token for a deleted user has been revoked') from e
        if e.response['error'] == 'no_permission':
            raise Exception('The workspace toekn used does not have necessary permission to send message') from e
        if e.response['error'] == 'ratelimited':
            raise Exception('The request has been ratelimited. Retry sending message later') from e
        if e.response['error'] == 'service_unavailable':
            raise Exception('The service is temporarily unavailable') from e
        if e.response['error'] == 'fatal_error':
            raise Exception('The server encountered catostrophic error while sending message') from e
        if e.response['error'] == 'internal_error':
            raise Exception('The server could not complete operation, likely due to transietn issue') from e
        if e.response['error'] == 'request_timeout':
            raise Exception('Sending message error via POST: either message was missing or truncated') from e
        else:
            raise Exception(f'Failed Sending Message to slack channel {channel} Error: {e.response["error"]}') from e

    except Exception as e:
        print("\n\n")
        pp.pprint(
            f"Failed sending message to slack channel {channel}, Error: {str(e)}")
        return f"Unable to send message on {channel}"
    