import os
from collections.abc import Generator
import json
from typing import Any
from fastapi import FastAPI
from resonate import Context, Yieldable, Resonate
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.jobs.api import JobsApi
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
resonate = Resonate().remote()
resonate.start()


# handlers
@app.get("/run")
async def get(id: str, url: str):
    h = data_pipeline.begin_run(id, url)
    if h.done():
        return "I am done"
    return "working on it"


@app.post("/resolve")
async def resolve(id: str, value: str):
    resonate.promises.resolve(id, ikey=id, data=json.dumps(value))


@resonate.register
def data_pipeline(ctx: Context, url: str) -> Generator[Yieldable, Any, None]:
    p = yield ctx.promise()
    yield ctx.run(run_job, promise_id=p.id, job=int(os.environ["JOB_ID"]), url=url)
    v = yield p
    # yield ctx.run(send_email)
    print(f"databricks execution has finished with value {v}")
    return


def run_job(ctx: Context, promise_id: str, job: int, url: str) -> None:
    client = ApiClient(
        host=os.environ["DATABRICKS_HOST"],
        token=os.environ["DATABRICKS_TOKEN"],
    )
    jobs = JobsApi(client)
    jobs.run_now(
        job_id=job,
        notebook_params={"promise_id": promise_id, "url": url},
        jar_params=None,
        python_params=None,
        spark_submit_params=None,
    )
