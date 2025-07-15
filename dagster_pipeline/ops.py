from dagster import op

@op
def scrape_telegram_data():
    print("Scraping telegram data...")
    return "done"

@op
def load_raw_to_postgres(dummy):
    print("Loading raw data to Postgres...")
    return "done"

@op
def run_dbt_transformations(dummy):
    print("Running dbt models...")
    import subprocess
    subprocess.run(["dbt", "run"], cwd="dbt_project")
    return "done"

@op
def run_yolo_enrichment(dummy):
    print("Running YOLOv8 enrichment...")
    import subprocess
    subprocess.run(["python", "scripts/yolo_enrichment.py"])
