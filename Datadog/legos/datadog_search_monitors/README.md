[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Datadog search monitors</h2>

<br>

## Description
This Lego searches monitors in datadog based on filters.


## Lego Details
    datadog_search_monitors(handle: object)

    handle: Object of type unSkript datadog Connector
    query: After entering a search query in your `Manage Monitor page <https://app.datadoghq.com/monitors/manage>`_ use the query parameter value in the
            URL of the page as value for this parameter. Consult the dedicated `manage monitor documentation </monitors/manage/#find-the-monitors>`_
            page to learn more. The query can contain any number of space-separated monitor attributes, for instance ``query="type:metric status:alert"``.
    name: A string to filter monitors by name.

## Lego Input
This Lego takes 3 inputs. handle, query, name

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)