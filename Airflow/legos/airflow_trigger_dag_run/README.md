[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>Airflow trigger DAG run</h2>

<br>

## Description
This Lego used to trigger Airflow DAG run.


## Lego Details
    airflow_trigger_dag_run(handle: object, dag_id: str, conf: dict,
                            dag_run_id: str, logical_date: str)

        handle: Object of type unSkript AirFlow Connector
        dag_id: The DAG ID.
        conf: JSON object describing additional configuration parameters.
        dag_run_id: The value of this field can be set only when creating the object.
        logical_date: The logical date (previously called execution date).

## Lego Input
This Lego take five inputs handle, conf, dag_run_id, logical_date and dag_id.

## Lego Output
Here is a sample output.


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)