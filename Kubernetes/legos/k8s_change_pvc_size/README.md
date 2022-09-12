[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>K8S Change PVC Size</h2>

<br>

## Description
This Lego uses the `unSkript` internal k8s API to resize the size of a given K8S PVC. 


## Lego Details

    k8s_change_pvc_size(handle: object, 
                        namespace: str,
                        name: str,
                        resize_option: SizingOption,
                        resize_value: float)

        handle: Object of type unSkript K8S Connector
        namespace: String, K8S Namespace
        name: String, Name of the PVC
        resize_option: Enum, SizingOption (Add or Multiply)
        resize_value: Float, Value that is used to resize.

## Lego Input
This Lego takes Four input values. `namespace` (string), `name` (string), `resize_option` (Enum of type SizingOption) and `resize_value` (float).

Like all unSkript Legos this lego relies on the information provided in unSkript K8S Connector. 


## Lego Output
Here is a sample output. 

    Events:
    Type     Reason   Age                     From     Message
    ----     ------   ----                    ----     -------
    Normal   BackOff  33m (x437 over 133m)    kubelet  Back-off pulling image "diebian"
    Warning  Failed   3m16s (x569 over 133m)  kubelet  Error: ImagePullBackOff


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)
