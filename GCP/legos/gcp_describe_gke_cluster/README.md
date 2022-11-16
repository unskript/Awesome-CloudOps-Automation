[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>GCP Describe a GKE cluster</h1>

## Description
This Lego describe a GKE clusterfor a given Project, cluster and Zone.

## Lego Details

    describe_gke_cluster(handle: object, project_id: str, zone: str, cluster_name: str)

        handle: Object of type unSkript GCP Connector
        project_id: String GCP Project name
        zone: Zone to which the cluster in the project should be fetched.
        cluster_name: Name of the GKE cluster.


## Lego Input
 project:  GCP Project name eg. "acme-dev"
 zone: GCP Zone eg. "us-west1-b"
 cluster_name: cluster Name

## Lego Output
Here is a sample output.

<img src="./1.png">



## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)
