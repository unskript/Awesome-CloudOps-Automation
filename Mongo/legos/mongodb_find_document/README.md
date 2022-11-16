[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>MongoDB Find Document</h1>

## Description
This Lego Finds the document in collection.


## Lego Details

    mongodb_find_document(handle, database_name: str, collection_name: str, filter: dict, command: FindCommands, document: dict = {}, projection: dict = {}, sort: List = [])

        handle: Object of type unSkript Mongodb Connector.
        database_name: Name of the MongoDB database.
        collection_name: Name of the MongoDB collection.
        filter: A query that matches the document to find.
        command: Db command.
        document:The modifications to apply in dictionary format.
        projection: A list of field names that should be returned/excluded in the result.
        sort: A list of {key:direction} pairs.

## Lego Input
This Lego take eight inputs handle, database_name, collection_name, filter,command, document, projection  and sort. 

## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)