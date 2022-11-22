{
  "name": "k8s: Pod Stuck in Terminating State",
  "description": "This runbook checks any Pods are in terminating state in a given k8s namespace. If it finds, it tries to recover it by resetting finalizers of the pod.",  
  "uuid": "7108717393788c2d76687490938faffe5e6e2a46f05405f180e089a166761173",
  "icon": "CONNECTOR_TYPE_K8S",
  "categories": [ "CATEGORY_TYPE_CLOUDOPS", "CATEGORY_TYPE_DEVOPS", "CATEGORY_TYPE_SRE" ],
  "connector_types": [ "CONNECTOR_TYPE_K8S" ],
  "version": "1.0.0"
}