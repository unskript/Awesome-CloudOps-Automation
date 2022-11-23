{
  "name": "Detect ECS failed deployment",
  "description": "This runbook check if there is a failed deployment in progress for a service in an ECS cluster. If it finds one, it sends the list of stopped task associated with this deployment and their stopped reason to slack.",
  "uuid": "d5a5b8447076f47e99d7603527a6e82fed42e6ae22bffe8eabf446220765e0bc",
  "icon": "CONNECTOR_TYPE_AWS",
  "categories": [ "CATEGORY_TYPE_CLOUDOPS", "CATEGORY_TYPE_DEVOPS", "CATEGORY_TYPE_SRE" ],
  "connector_types": [ "CONNECTOR_TYPE_AWS" ],
  "version": "1.0.0"
}

