[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>AWS ECS Describe Task Definition</h1>

## Description
This Lego describes AWS ECS Task Definition..


## Lego Details

    aws_ecs_describe_task_definition(handle, region: str, taskDefinition: str)

        handle: Object of type unSkript AWS Connector
        region: AWS Region of the ECS service..
        taskDefinition: The family and revision (family:revision ) or full ARN of the task definition to run in service.

## Lego Input
This Lego takes three inputs handle, region and taskDefinition. 

## Lego Output
```
{
    'ResponseMetadata': {
        'HTTPHeaders': {
            'content-length': '1145',
                'content-type': 'application/x-amz-json-1.1',
                    'date': 'Thu, 13 Oct 2022 21:01:39 GMT',
                        'x-amzn-requestid': 'e21bb321-9051-4a5e-859c-3ca17d8b8193'
        },
        'HTTPStatusCode': 200,
            'RequestId': 'e21bb321-9051-4a5e-859c-3ca17d8b8193',
                'RetryAttempts': 0
    },
    'taskDefinition': {
        'compatibilities': ['EC2', 'FARGATE'],
            'containerDefinitions': [{
                'cpu': 0,
                'environment': [],
                'essential': True,
                'image': 'amazon/amazon-ecs-sample',
                'logConfiguration': {
                    'logDriver': 'awslogs',
                    'options': {
                        'awslogs-group': '/ecs/AWSSampleApp',
                        'awslogs-region': 'us-west-2',
                        'awslogs-stream-prefix': 'ecs'
                    }
                },
                'mountPoints': [],
                'name': 'AmazonSampleImage',
                'portMappings': [],
                'volumesFrom': []
            }],
                'cpu': '256',
                    'executionRoleArn': 'arn:aws:iam::100498623390:role/DevProxyRoleToBeAssumed',
                        'family': 'AWSTestApp',
                            'memory': '512',
                                'networkMode': 'awsvpc',
                                    'placementConstraints': [],
                                        'registeredAt': datetime.datetime(2022, 10, 14, 2, 31, 37, 50000, tzinfo = tzlocal()),
                                            'registeredBy': 'arn:aws:sts::100498623390:assumed-role/DevProxyRoleToBeAssumed/test',
                                                'requiresAttributes': [{ 'name': 'com.amazonaws.ecs.capability.logging-driver.awslogs' },
                                                { 'name': 'ecs.capability.execution-role-awslogs' },
                                                { 'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.19' },
                                                { 'name': 'com.amazonaws.ecs.capability.docker-remote-api.1.18' },
                                                { 'name': 'ecs.capability.task-eni' }],
                                                    'requiresCompatibilities': ['FARGATE'],
                                                        'revision': 85,
                                                            'status': 'ACTIVE',
                                                                'taskDefinitionArn': 'arn:aws:ecs:us-west-2:100498623390:task-definition/AWSTestApp:85',
                                                                    'volumes': []
    }
}
```


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)