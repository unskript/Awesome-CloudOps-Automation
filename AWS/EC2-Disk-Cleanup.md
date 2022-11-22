{
  "name": "AWS EC2 Disk Cleanup",
  "description": "This runbook locates large files in an EC2 instance and backs them up into a given S3 bucket. Afterwards, it deletes the files backed up and send a message on a specificed Slack channel. It uses SSH and linux commands to perform the functions it needs.", 
  "uuid": "f16e204e8b4c9a59e52e8d71feda07cfa066fa57d7c427772d715b4221c8f634",
  "icon": "CONNECTOR_TYPE_AWS",
  "categories": [ "CATEGORY_TYPE_CLOUDOPS", "CATEGORY_TYPE_DEVOPS", "CATEGORY_TYPE_SRE" ],
  "connector_types": [ "CONNECTOR_TYPE_AWS" ],
  "version": "1.0.0"
}

