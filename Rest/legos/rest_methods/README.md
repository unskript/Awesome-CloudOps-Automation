[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Call REST Methods</h2>

<br>

## Description
This Lego call REST Methods.


## Lego Details

    rest_methods(handle: object, relative_url_path: str, method: Method, params: dict,
                headers: dict, body: dict)

        handle: Object of type unSkript Rest Connector
        relative_url_path: Relative URL path for the request. eg /users.
        method: Rest Method Supported methods : GET, POST, PUT, PATCH and DELETE
        params: Dictionary or bytes to be sent in the query eg {'foo': 'bar'}.
        headers: Dictionary of HTTP Headers to send with the requests.
        body: Json to send in the body of the request eg {'foo': 'bar'}.

## Lego Input
This Lego take six input handle, relative_url_path, method, params, headers and body.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)