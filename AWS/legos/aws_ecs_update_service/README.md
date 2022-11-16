[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Update AWS ECS Service </h1>

## Description
This Lego Updates AWS ECS Service.


## Lego Details

    aws_ecs_update_service(handle, region: str, service: str, taskDefinition: str, cluster: str = None)

        handle: Object of type unSkript AWS Connector
        region: AWS Region of the ECS service..
        service: The name of the service to update.
        taskDefinition: The family and revision (family:revision ) or full ARN of the task definition to run in service.
        cluster: Cluster name that your service runs on.

## Lego Input
This Lego takes five inputs handle, region, service, taskDefinition and cluster. 

## Lego Output
Here is a sample output.
```
{'ResponseMetadata': 
    {'HTTPHeaders': {'content-length': '2510',
                    'content-type': 'application/x-amz-json-1.1',
                    'date': 'Thu, 13 Oct 2022 20:49:08 GMT',
                    'x-amzn-requestid': '9e820eae-1d35-4812-bfca-37c4e1ecd8d0'},
                      'HTTPStatusCode': 200,
                      'RequestId': '9e820eae-1d35-4812-bfca-37c4e1ecd8d0',
                      'RetryAttempts': 0},
 'service': {'clusterArn': 'arn:aws:ecs:us-west-2:100498623390:cluster/TestECSCluster',
             'createdAt': datetime.datetime(2022, 10, 14, 2, 19, 5, 841000, tzinfo=tzlocal()),
             'createdBy': 'arn:aws:iam::100498623390:role/DevProxyRoleToBeAssumed',
             'deploymentConfiguration': {'deploymentCircuitBreaker': {'enable': False,
                                                                      'rollback': False},
                                         'maximumPercent': 200,
                                         'minimumHealthyPercent': 100},
             'deploymentController': {'type': 'ECS'},
             'deployments': [{'createdAt': datetime.datetime(2022, 10, 14, 2, 19, 8, 706000, tzinfo=tzlocal()),
                              'desiredCount': 0,
                              'failedTasks': 0,
                              'id': 'ecs-svc/8526124291437356365',
                              'launchType': 'FARGATE',
                              'networkConfiguration': {'awsvpcConfiguration': {'assignPublicIp': 'ENABLED',
                                                                               'securityGroups': ['sg-0b7a1a8fdf5417f28'],
                                                                               'subnets': ['subnet-c643f49b']}},
                              'pendingCount': 0,
                              'platformVersion': '1.4.0',
                              'rolloutState': 'IN_PROGRESS',
                              'rolloutStateReason': 'ECS deployment '
                                                    'ecs-svc/8526124291437356365 '
                                                    'in progress.',
                              'runningCount': 0,
                              'status': 'PRIMARY',
                              'taskDefinition': 'arn:aws:ecs:us-west-2:100498623390:task-definition/AWSTestAppTwo:17',
                              'updatedAt': datetime.datetime(2022, 10, 14, 2, 19, 8, 706000, tzinfo=tzlocal())},
                             {'createdAt': datetime.datetime(2022, 10, 14, 2, 19, 5, 841000, tzinfo=tzlocal()),
                              'desiredCount': 2,
                              'failedTasks': 0,
                              'id': 'ecs-svc/6903532899083802063',
                              'launchType': 'FARGATE',
                              'networkConfiguration': {'awsvpcConfiguration': {'assignPublicIp': 'ENABLED',
                                                                               'securityGroups': ['sg-0b7a1a8fdf5417f28'],
                                                                               'subnets': ['subnet-c643f49b']}},
            'pendingCount': 0,
            'platformVersion': '1.4.0',
            'rolloutState': 'IN_PROGRESS',
            'rolloutStateReason': 'ECS deployment '
                                'ecs-svc/6903532899083802063 '
                                'in progress.',
            'runningCount': 0,
            'status': 'ACTIVE',
            'taskDefinition': 'arn:aws:ecs:us-west-2:100498623390:task-definition/AWSTestApp:84',
            'updatedAt': datetime.datetime(2022, 10, 14, 2, 19, 5, 841000, tzinfo=tzlocal())}],
             'desiredCount': 2,
             'enableECSManagedTags': False,
             'enableExecuteCommand': False,
             'events': [],
             'launchType': 'FARGATE',
             'loadBalancers': [],
             'networkConfiguration': {'awsvpcConfiguration': {'assignPublicIp': 'ENABLED',
            'securityGroups': ['sg-0b7a1a8fdf5417f28'],
            'subnets': ['subnet-c643f49b']}},
             'pendingCount': 0,
             'placementConstraints': [],
             'placementStrategy': [],
             'platformVersion': 'LATEST',
             'propagateTags': 'NONE',
             'roleArn': 'arn:aws:iam::100498623390:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS',
             'runningCount': 0,
             'schedulingStrategy': 'REPLICA',
             'serviceArn': 'arn:aws:ecs:us-west-2:100498623390:service/TestECSCluster/TestECSService',
             'serviceName': 'TestECSService',
             'serviceRegistries': [],
             'status': 'ACTIVE',
             'taskDefinition': 'arn:aws:ecs:us-west-2:100498623390:task-definition/AWSTestAppTwo:17'}
             }
            
```

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)