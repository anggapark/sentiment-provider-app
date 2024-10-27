from __future__ import annotations

import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

# from kedro.framework.session import KedroSession
# from kedro.framework.project import configure_project


# class KedroOperator(BaseOperator):
#     @apply_defaults
#     def __init__(
#         self,
#         package_name: str,
#         pipeline_name: str,
#         node_name: str | list[str],
#         project_path: str | Path,
#         env: str,
#         conf_source: str,
#         *args,
#         **kwargs,
#     ) -> None:
#         super().__init__(*args, **kwargs)
#         self.package_name = package_name
#         self.pipeline_name = pipeline_name
#         self.node_name = node_name
#         self.project_path = project_path
#         self.env = env
#         self.conf_source = conf_source

#     def execute(self, context):
#         configure_project(self.package_name)
#         with KedroSession.create(
#             self.project_path, env=self.env, conf_source=self.conf_source
#         ) as session:
#             if isinstance(self.node_name, str):
#                 self.node_name = [self.node_name]
#             session.run(self.pipeline_name, node_names=self.node_name)


# Kedro settings required to run your pipeline
env = "airflow"
pipeline_name = "__default__"
project_path = Path.cwd()
package_name = "provider_sentiment"
conf_source = "" or Path.cwd() / "conf"


def run_elt_script():
    script_path = "/opt/airflow/extract/to_lake.py"
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    dag_id="provider-sentiment",
    start_date=datetime(2024, 10, 26),
    max_active_runs=3,
    # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    schedule_interval="@once",
    catchup=False,
    # Default settings applied to all tasks
    default_args=dict(
        owner="airflow",
        depends_on_past=False,
        email_on_failure=False,
        email_on_retry=False,
        retries=1,
        retry_delay=timedelta(minutes=5),
    ),
) as dag:
    extraction_task = PythonOperator(
        task_id="extract_to_postgres",
        python_callable=run_elt_script,
    )

    transform_load_task = DockerOperator(
        task_id="trainsform_load",
        image="kedro-pipeline:latest",  # Use the image name for Kedro pipeline
        api_version="auto",
        auto_remove=True,
        command="kedro run --pipeline=data_preprocessing",  # Adjust to your Kedro pipeline command
        docker_url="unix://var/run/docker.sock",
        network_mode="pulsaproj-net",
        # volumes=[".:/app"],
        environment={
            "AIRFLOW_CONN_SOURCE_POSTGRES": "postgresql://postgres:secret@source_postgres:5433/source_db",
            "AIRFLOW_CONN_DESTINATION_POSTGRES": "postgresql://postgres:secret@destination_postgres:5434/destination_db",
        },
    )
    ml_task = DockerOperator(
        task_id="machine_learning",
        image="kedro-pipeline:latest",  # Use the image name for Kedro pipeline
        api_version="auto",
        auto_remove=True,
        command="kedro run --pipeline=machine_learning",  # Adjust to your Kedro pipeline command
        docker_url="unix://var/run/docker.sock",
        network_mode="pulsaproj-net",
        # volumes=[".:/app"],
        environment={
            "AIRFLOW_CONN_SOURCE_POSTGRES": "postgresql://postgres:secret@source_postgres:5433/source_db",
            "AIRFLOW_CONN_DESTINATION_POSTGRES": "postgresql://postgres:secret@destination_postgres:5434/destination_db",
        },
    )

    # Define the task sequence
    extraction_task >> transform_load_task >> ml_task
    # tasks = {
    #     "extract-to-postgres": PythonOperator(
    #         task_id="extract-to-postgres",
    #         python_callable=run_elt_script,
    #     ),
    #     "combine-dataset": KedroOperator(
    #         task_id="combine-dataset",
    #         package_name=package_name,
    #         pipeline_name=pipeline_name,
    #         node_name="combine_dataset",
    #         project_path=project_path,
    #         env=env,
    #         conf_source=conf_source,
    #     ),
    #     "preprocess-texts": KedroOperator(
    #         task_id="preprocess-texts",
    #         package_name=package_name,
    #         pipeline_name=pipeline_name,
    #         node_name="preprocess_texts",
    #         project_path=project_path,
    #         env=env,
    #         conf_source=conf_source,
    #     ),
    #     "split-data-node": KedroOperator(
    #         task_id="split-data-node",
    #         package_name=package_name,
    #         pipeline_name=pipeline_name,
    #         node_name="split_data_node",
    #         project_path=project_path,
    #         env=env,
    #         conf_source=conf_source,
    #     ),
    #     "train-model-node": KedroOperator(
    #         task_id="train-model-node",
    #         package_name=package_name,
    #         pipeline_name=pipeline_name,
    #         node_name="train_model_node",
    #         project_path=project_path,
    #         env=env,
    #         conf_source=conf_source,
    #     ),
    #     "prediction": KedroOperator(
    #         task_id="prediction",
    #         package_name=package_name,
    #         pipeline_name=pipeline_name,
    #         node_name="prediction",
    #         project_path=project_path,
    #         env=env,
    #         conf_source=conf_source,
    #     ),
    #     "evaluate-model-node": KedroOperator(
    #         task_id="evaluate-model-node",
    #         package_name=package_name,
    #         pipeline_name=pipeline_name,
    #         node_name="evaluate_model_node",
    #         project_path=project_path,
    #         env=env,
    #         conf_source=conf_source,
    #     ),
    # }

    # tasks["extract-to-postgres"] >> tasks["combine-dataset"]
    # tasks["combine-dataset"] >> tasks["preprocess-texts"]
    # tasks["preprocess-texts"] >> tasks["split-data-node"]
    # tasks["split-data-node"] >> tasks["prediction"]
    # tasks["split-data-node"] >> tasks["evaluate-model-node"]
    # tasks["split-data-node"] >> tasks["train-model-node"]
    # tasks["train-model-node"] >> tasks["prediction"]
    # tasks["prediction"] >> tasks["evaluate-model-node"]
