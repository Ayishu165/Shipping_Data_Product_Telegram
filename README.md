# 📦 Telegram Medical Insights Pipeline (Tasks 0 - 2)

An end-to-end ELT pipeline for extracting, transforming, and modeling Telegram data related to Ethiopian medical businesses. This part of the project covers:

- ✅ Task 0: Project & Environment Setup
- ✅ Task 1: Data Scraping & Collection
- ✅ Task 2: Data Modeling & Transformation with dbt

---

---

## ✅ Task 0 - Project & Environment Setup

### 🔧 Key Steps

- Initialized a Git repository.
- Created `.env` file for secrets (e.g., Telegram API keys, DB password).
- Added `.env` to `.gitignore`.
- Created `requirements.txt` with required Python packages.
- Configured Docker and Docker Compose for reproducible environment:
  - `app`: Python application
  - `db`: PostgreSQL database

### 📄 Requirements

```txt
telethon
psycopg2-binary
python-dotenv
dbt-postgres
ultralytics
fastapi
uvicorn
dagster
dagster-webserver

Task 1: Data Scraping and Collection (Extract & Load)
This task focuses on populating a raw data lake with data from specified Telegram channels .

Scraping: A Python script using the Telethon library extracts messages and images from channels like Chemed Telegram Channel, lobelia4cosmetics, and tikvahpharma .

Data Lake: The raw, unaltered data is stored as JSON files in a partitioned directory structure (data/raw/telegram_messages/YYYY-MM-DD/channel_name.json) to facilitate incremental processing .



Task 2: Data Modeling and Transformation (Transform)
Raw data is loaded into PostgreSQL and then transformed into a clean, analytics-ready star schema using dbt (Data Build Tool) .

Loading: A script loads the raw JSON files from the data lake into a raw schema in the PostgreSQL data warehouse .

Transformation: A dbt project cleans, restructures, and models the data into layers .

Staging Models: stg_telegram_messages.sql performs initial cleaning, type casting, and column renaming on the raw data .

Data Mart Models: Final analytical tables are built using a star schema :

dim_channels: A dimension table for Telegram channel information .

dim_dates: A time dimension table for trend analysis .

fct_messages: A fact table with foreign keys to the dimension tables and key metrics like has_image and message_length .

Testing: The dbt models include built-in tests (unique, not_null) to validate primary keys and a custom test to enforce business logic, ensuring data quality .