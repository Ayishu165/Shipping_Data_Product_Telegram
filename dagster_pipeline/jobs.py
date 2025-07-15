from dagster import job
from dagster_pipeline.ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment
)

@job
def full_pipeline_job():
    # call scrape first
    scrape_telegram_data()
    
    # then call loading
    load_raw_to_postgres()
    
    # then dbt
    run_dbt_transformations()
    
    # finally YOLO enrichment
    run_yolo_enrichment()
