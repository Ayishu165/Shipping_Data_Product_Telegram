from dagster import ScheduleDefinition
from .jobs import full_pipeline_job

daily_schedule = ScheduleDefinition(
    job=full_pipeline_job,
    cron_schedule="0 2 * * *",  # Every day at 2AM
)
