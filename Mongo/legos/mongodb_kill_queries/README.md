[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>MongoDB Kill Query  </h1>

## Description
This Lego uses the `killop` command of MongoDB shell to kill the Job with the given operation ID.  

## Lego Details

    mongodb_kill_queries(handle: object, op_id: int)

        handle: Object: Object of type unSkript MongoDB Connector
        op_id: Int: Operation ID (as an integer)

## Lego Input
This Lego takes Operation ID of the Query to kill. Like other MongoDB, this lego relies
on information provided in unSkript MongoDB Connector. 

## Lego Output
Here is a sample output.

    {'info': 'Successfully Killed OpID 1132332', 'ok': 1}

The Input that was given was `1132332` which is the Operation ID we intended to kill.



## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)