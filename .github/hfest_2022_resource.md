[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 



<h1>Hacktoberfest 2022 Resource</h1>

## Google cloud resource available for testing

### Storage Buckets (Object store) 
Your computer's filesystem uses directories to organize data which are then stored in files. Similarly, data that is kept on the Cloud are in the form of objects, which are then gathered in buckets(a bucket is basically a container used to store objects).
  
  ###### Examples
  1. gs://hacktoberfest_bucket_1/
  2. gs://hacktoberfest_bucket_2/
  3. gs://hacktoberfest_public_bucket/


### Compute instances (Compute Engine Instances) 
Compute Engine instances can run public images for Linux and Windows Servers, as well as private custom images created or imported from existing systems. Additionally, Docker containers, which are launched automatically on instances running the Container-Optimized OS public image, can be deployed.

```NAME                    ZONE        MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP  STATUS
hacktoberfest-tagged    us-west1-b  e2-micro                   10.138.0.4                RUNNING
hacktoberfest-untagged  us-west1-b  e2-micro                   10.138.0.3                RUNNING
```

### Identity Access Management (IAM) user
IAM (Identity and Access Management) allows administrators to authorize who can take actions on specific resources, giving you complete control and visibility over Google Cloud resources.

```
DISPLAY NAME                            EMAIL                                                               DISABLED

hacktober-test-user                     hacktober-test-user@hacktoberfest-2022.iam.gserviceaccount.com      False

```

### Filestore
Applications that need a file system interface and a shared file system for data can use Filestore, a managed file storage service. The user gets a native experience for setting up managed network detached storage with their virtual machine in the compute engine and Google Kubernetes Engine. For many applications, it is the ideal choice since it provides low latency for file operations.

```
INSTANCE_NAME            LOCATION    TIER       CAPACITY_GB  FILE_SHARE_NAME  IP_ADDRESS      STATE     CREATE_TIME
hacktoberfest-filestore  us-west1-b  BASIC_HDD  1024         hacktoberfest    10.101.128.210  CREATING  2022-10-11T23:12:25
```


### GKE (Google Kubernetes Engine) Cluster
Google Kubernetes Engine (GKE) is a managed, production-ready environment for running containerized applications.

```
NAME                   LOCATION    MASTER_VERSION    MASTER_IP      MACHINE_TYPE  NODE_VERSION      NUM_NODES  STATUS
hacktoberfest-cluster  us-west1-b  1.22.12-gke.2300  XX.XXX.XXX.XX  e2-medium     1.22.12-gke.2300  3          RUNNING

```
