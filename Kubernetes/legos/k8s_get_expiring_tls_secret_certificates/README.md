[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Get the expiring TLS secret certificates for a K8s cluster. </h1>

## Description
This action gets the expiring certificates for a K8s cluster.


## Lego Details

    k8s_get_expiring_tls_secret_certificates(handle, namespace:str='', expiring_threshold:int=7)

        handle: Object of type unSkript K8S Connector
        namespace (str) : Optional - k8s namespace.
        expiration_threshold (int): The threshold (in days) for considering a certificate as expiring soon.

## Lego Input

This Lego take three inputs handle, namespace and expiration_threshold.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)