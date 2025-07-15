from dagster import Definitions
from dagster_pipeline.jobs import full_pipeline_job

defs = Definitions(
    jobs=[full_pipeline_job]
)
