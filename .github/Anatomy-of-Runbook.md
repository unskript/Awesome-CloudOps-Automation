[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Anatomy of a unSkript Runbook</h1>


<div class="warning" style='padding:0.1em; background-color:#EFEFFF; color:#69337A'>
<span>
<p style='margin-top:1em; text-align:center'>
<b>Runbook Definition</b></p>
<p style='margin-left:1em;'>
In a computer sytem or network, a runbook is a compilation of routine procedures and operations that the system administrator or operator carries out. System adminsistrators in IT department and NOCs use runbooks as a reference. 
</p>
<p style='margin-bottom:1em; margin-right:1em; text-align:right; font-family:Georgia'> <b>- Wikipedia</b> <i>(https://en.wikipedia.org/wiki/Runbook)</i>
</p></span>
</div>



## unSkript Runbook

`unSkript Runbooks` is a collection of atomic `Routines` called unSkript `Actions`. Think of it like a build blocks (like Legos) with which you can construct any model you wish. These `Actions` are nothing but modular python `functions` that accomplish a well defined task. Using these `Actions` you can construct a unSkript Runbook to accomplish a given task.  In that sense `unSkript Runbooks` is a collection of such `Actions` and/or Information `Text` that accomplish a pre-defined task. 

<image src="https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/images/anatomy.png">
<br>
<image src="https://github.com/unskript/Awesome-CloudOps-Automation/blob/master/.github/images/ui.png">
<br>


## Action 

`Action` sometimes referred to here as `Lego` are the Atomic part of a unSkript Runbook. Here is a sample `Action` that performs a well defined task. 

```
def aws_get_instance_details(handle, instance_id: str, region: str) -> Dict:
    """aws_get_instance_details Returns instance details.

        :type handle: object
        :param handle: Object returned by the task.validate(...) method.

        :type instance_ids: list
        :param instance_ids: List of instance ids.

        :type region: string
        :param region: Region for instance.

        :rtype: Dict with the instance details.
    """

    ec2client = handle.client('ec2', region_name=region)
    instances = []
    response = ec2client.describe_instances(
        Filters=[{"Name": "instance-id", "Values": [instance_id]}])
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance)

    return instances[0]
```

This Action expects three parameters as inputs. 
  1. `handle` is an Object of type `Connector AWS`. 
  2. `instance-id`  is the `aws ec2` instance identifier.
  3. `region` is the `aws region` where the `aws ec2` can be found


unSkript `Action` are tied to a Connector. What this means is that we need to 
create a `AWS connector` before using this `Action`. You can create any supported
connector by clicking `Credentials` -> Add New Credential. 
