[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>AWS Register/Unregister Instances from a Target Group </h1>

## Description
This Lego Register/Unregister AWS Instance from a Target Group.


## Lego Details

    aws_target_group_register_unregister_instances(handle: object, arn: str, instance_ids: List, port: int,
                                                   unregister: bool)

        handle: Object of type unSkript AWS Connector.
        arn: ARN of the Target Group.
        instance_ids: List of instance IDs.
        port: The port on which the instances are listening.
        unregister: Check this if the instances need to be unregistered.

## Lego Input

This Lego take five inputs handle, arn, instance_ids, port and unregister.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)