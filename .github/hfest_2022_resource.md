[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 

<h1>Hacktoberfest 2022 Resource</h1>

## Google cloud resource available for testing

### Storage Buckets (Object store) 
  1. gs://hacktoberfest_bucket_1/
  2. gs://hacktoberfest_bucket_2/
  3. gs://hacktoberfest_public_bucket/


### Compute instances (Compute Engine Instances) 
```NAME                    ZONE        MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP  STATUS
hacktoberfest-tagged    us-west1-b  e2-micro                   10.138.0.4                RUNNING
hacktoberfest-untagged  us-west1-b  e2-micro                   10.138.0.3                RUNNING
```

### IAM user
```
DISPLAY NAME                            EMAIL                                                               DISABLED

hacktober-test-user                     hacktober-test-user@hacktoberfest-2022.iam.gserviceaccount.com      False

```

### Filestore
```
INSTANCE_NAME            LOCATION    TIER       CAPACITY_GB  FILE_SHARE_NAME  IP_ADDRESS      STATE     CREATE_TIME
hacktoberfest-filestore  us-west1-b  BASIC_HDD  1024         hacktoberfest    10.101.128.210  CREATING  2022-10-11T23:12:25
```


### GKE (Google Kubernetes Engine) Cluster
```
NAME                   LOCATION    MASTER_VERSION    MASTER_IP      MACHINE_TYPE  NODE_VERSION      NUM_NODES  STATUS
hacktoberfest-cluster  us-west1-b  1.22.12-gke.2300  XX.XXX.XXX.XX  e2-medium     1.22.12-gke.2300  3          RUNNING

```
