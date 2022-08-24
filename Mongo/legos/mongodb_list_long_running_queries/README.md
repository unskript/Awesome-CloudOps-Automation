[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>MongoDB List Long Running Queries </h1>

## Description
This Lego queries the server and retrieves long running queries.
A Long running query is defined that has a running time of more than 5 seconds.


## Lego Details

    mongodb_list_long_running_queries(handle: object, query_secs_running_threshold:int = 5)

        handle: Object of type unSkript MongoDB Connector
        query_secs_running_threshold: Integer value, default time to use to query long_query. Any query
                that is taking more than the query_secs_running_threshold is deamed as long-running-query

## Lego Input
This Lego takes `query_secs_running_threshold` an integer value (default set to 5). 
The Lego will use this threshold value when checking long-running queries.
This Lego relies on unSkript Connector to access the MongoDB server.

## Lego Output
Here is a sample output.

    
    appName        active    op       ns                      secs_running  desc
    -------------  --------  -------  --------------------  --------------  ---------------
    mongosh 1.3.1  True      command  admin.$cmd.aggregate               0  conn388
    None           True      none                                           waitForMajority
    


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://unskript.com)