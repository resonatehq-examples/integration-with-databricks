from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi

DATABRICKS_HOST = ...
DATABRICKS_TOKEN = ... # see how to get a token: https://docs.databricks.com/aws/en/dev-tools/auth/pat
JOB_ID = ...

client = ApiClient(
    host=DATABRICKS_HOST,
    token=DATABRICKS_TOKEN,
)
jobs = JobsApi(client)
jobs.run_now(
    job_id=JOB_ID,
    notebook_params=None,
    jar_params=None,
    python_params=None,
    spark_submit_params=None,
)
