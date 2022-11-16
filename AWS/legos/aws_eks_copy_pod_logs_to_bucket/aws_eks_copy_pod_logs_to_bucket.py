##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
from typing import  Dict
import pprint


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    namespaceName: str = Field(
        title='namespace Name',
        description='Name of namespace')
    podName: str = Field(
        title='Pod Name',
        description='Name of Pod')
    bucketName: str = Field(
        title='S3 Bucket Name',
        description='Name of S3 Bucket')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_copy_pod_logs_to_bucket_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def aws_eks_copy_pod_logs_to_bucket(handle, clusterName: str, namespaceName: str, podName: str, bucketName: str,
                                    region: str) -> Dict:
    """aws_eks_copy_pod_logs_to_bucket returns Dict.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type podName: string
        :param podName: Pod name.

        :type bucketName: string
        :param bucketName: Name of S3 Bucket.

        :type namespaceName: string
        :param namespaceName: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: Dict of name of pod and bucket with succcess message.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)

    coreApiClient = client.CoreV1Api(api_client=k8shandle)
    try:
        api_response = coreApiClient.read_namespaced_pod_log(name=podName,
                                                             namespace=namespaceName)
    except ApiException as e:
        print("An Exception occured while reading pod log: ".format(str(e)))
        raise e

    s3Client = handle.client('s3', region_name=region)
    try:
        s3Client.put_object(Bucket=bucketName, Key="tests/%s_pod_logs" % podName,
                            Body=api_response)
    except Exception as e:
        print("Error: ".format(str(e)))
        raise e
    return {"success": "Successfully copied %s pod logs to %s bucket." % (podName, bucketName)}
