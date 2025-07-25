import os
from collections.abc import Generator
import json
from typing import Any
import uuid
from fastapi import FastAPI
from resonate import Context, Yieldable, Resonate
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi

app = FastAPI()
resonate = Resonate().remote(group="default")
resonate.start()


# handlers
@app.get("/run")
async def get(id: str, url: str):
    h = databricks_integration.begin_run(id, url)
    if h.done():
        return "I'm done"
    return "working on it"


@app.post("/resolve")
async def resolve(id: str, value: str):
    resonate.promises.resolve(id, ikey=id, data=json.dumps(value))


# workflows
@resonate.register
def databricks_integration(ctx: Context, url: str) -> Generator[Yieldable, Any, None]:
    p = yield ctx.promise()
    yield ctx.run(run_workflow, job=615997738957459, promise_id=p.id, url=url)
    v = yield p
    print(f"databricks execution has finished with value {v}")
    # continue any business logic
    return


# functions
def run_workflow(ctx: Context, job: int, promise_id: str, url: str) -> None:
    client = ApiClient(
        host="https://dbc-711faa31-5f0c.cloud.databricks.com",
        token=os.environ["TOKEN"],
    )
    jobs = JobsApi(client)
    jobs.run_now(
        job_id=job,
        notebook_params={"promise_id": promise_id, "url": url},
        jar_params=None,
        python_params=None,
        spark_submit_params=None,
    )
