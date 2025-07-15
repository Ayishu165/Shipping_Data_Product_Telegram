# ✅ dbt Testing Overview

This directory contains the data tests used in our dbt project for the Telegram Medical Insights Pipeline.

## 🔍 Built-in Tests (Defined in YAML)

These are automatic validations provided by dbt, applied inside the model YAML files (`fct_messages.yml`, `stg_telegram_messages.yml`, etc.)

| Model            | Column        | Test Type         | Purpose                                       |
|------------------|---------------|-------------------|-----------------------------------------------|
| fct_messages     | message_id    | unique, not_null  | Ensures each message is uniquely identified   |
| fct_messages     | has_media     | accepted_values   | Should only be true or false                  |
| fct_messages     | channel_id    | not_null          | Every message should have an associated channel |
| dim_dates        | date          | unique, not_null  | Ensures time dimension is complete & indexed  |

## 🧪 Custom Tests

### `custom_tests.sql`

SQL-based tests that validate business rules beyond built-in constraints.

| Test Name                     | Description |
|-------------------------------|-------------|
| `media_has_message`           | Ensures media posts are not empty |
| `future_dates` (optional)     | Prevents invalid future post dates |

## 🧪 How to Run All Tests

Use this command to run all schema and custom tests:

```bash
dbt test
