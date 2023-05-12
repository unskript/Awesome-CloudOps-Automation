# Copyright (c) 2021 unSkript.com
# All rights reserved.
#

import pprint
from typing import Optional, Dict
from enum import Enum
from unskript.enums.rest_enums import Method
import html_to_json
from pydantic import BaseModel, Field
from werkzeug.exceptions import MethodNotAllowed


class Method(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class InputSchema(BaseModel):
    relative_url_path: str = Field(
        title='Path',
        description='Relative URL path for the request. eg /users.'
    )
    method: Method = Field(
        'GET',
        title='Method',
        description='''
                    Rest Method
                    Supported methods : GET, POST, PUT, PATCH and DELETE
                    '''
    )
    params: Optional[dict] = Field(
        default=None,
        title='URL Parameters',
        description="Dictionary or bytes to be sent in the query eg {'foo': 'bar'}"
    )
    headers: Optional[dict] = Field(
        default=None,
        title='Headers',
        description='''
                Dictionary of HTTP Headers to send with the requests.
                Example: {“Accept”: “*/*”}
            '''
    )
    body: Optional[dict] = Field(
        default=None,
        title='Body',
        description="Json to send in the body of the request eg {'foo': 'bar'}"
    )


def rest_methods_printer(output):
    if output is None:
        return None
    print('\n')
    pprint.pprint(output)
    return output


def rest_methods(
    handle,
    relative_url_path: str,
    method: Method,
    params: dict = None,
    headers: dict = None,
    body: dict = None) -> Dict:

    """rest_methods executes the rest method

        :type relative_url_path: string
        :param relative_url_path: Relative URL path for the request. eg /users.

        :type method: Method
        :param method: Rest Method Supported methods : GET, POST, PUT, PATCH and DELETE

        :type params: dict
        :param params: Dictionary or bytes to be sent in the query eg {'foo': 'bar'}.
        
        :type headers: dict
        :param headers: Dictionary of HTTP Headers to send with the requests.

        :type body: dict
        :param body: Json to send in the body of the request eg {'foo': 'bar'}.

        :rtype: Dict
    """
    if method == Method.GET:
        res = handle.get(relative_url_path,
                         params=params or {},
                         headers=headers or {}
                         )
    elif method == Method.POST:
        res = handle.post(relative_url_path, json=body, params=params or {}, headers=headers or {})
    elif method == Method.PUT:
        res = handle.put(relative_url_path, json=body, params=params or {}, headers=headers or {})
    elif method == Method.PATCH:
        res = handle.patch(relative_url_path, json=body, params=params or {}, headers=headers or {})
    elif method == Method.DELETE:
        res = handle.delete(relative_url_path, params=params or {}, headers=headers or {})
        if res.status_code == 200:
            print(f"Status: {res.status_code}")
        else:
            try:
                result = res.json()
            except Exception:
                result = html_to_json.convert(res.content)
            print(f"Status: {res.status_code}, Response:{result}")
        return {}
    else:
        raise MethodNotAllowed(f'Unsupported method {method}')

    handle.close()
    try:
        res.raise_for_status()
        result = res.json()
    except Exception as e:
        return {'Error while executing api': {str(e)}}

    return result
