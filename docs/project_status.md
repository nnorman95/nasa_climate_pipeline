# Project Status

## Current Implementation

The pipeline currently uses Python for API extraction and raw loading, PostgreSQL for raw JSONB storage, dbt for warehouse transformations and data tests, Docker Compose for local services, cron for scheduling, and Metabase for dashboarding.

## Current Pipeline

The pipeline extracts daily climate data from the NASA POWER API, stores raw API responses in PostgreSQL as JSONB, and uses dbt to build warehouse models and run data quality tests.

Current flow:

```text
NASA POWER API
-> raw JSON files
-> PostgreSQL raw JSONB table
-> dbt staging models
-> dbt dimension and fact models
-> dbt marts
-> dbt data tests
-> Metabase dashboard
```

## Completed

* Extract data from the NASA POWER Daily API.
* Save raw API responses as JSON files.
* Save processed CSV files locally for inspection.
* Load raw API responses into PostgreSQL as JSONB.
* Support local PostgreSQL and Docker PostgreSQL through `DATABASE_URL`.
* Prevent duplicate raw loads with a unique constraint and `ON CONFLICT DO NOTHING`.
* Convert nested NASA JSONB into daily weather rows.
* Convert NASA fill values such as `-999.0` to `NULL`.
* Created dbt project structure.
* Added local dbt profile support through `profiles/profiles.yml`.
* Added `profiles/profiles.example.yml` as a safe tracked profile template.
* Added a dbt macro for direct schema naming.
* Built warehouse layers with dbt:

  * `staging`
  * `dim`
  * `fact`
  * `mart`
* Built dbt models:

  * `stg_nasa_power_responses`
  * `stg_daily_weather`
  * `dim_location`
  * `fact_daily_weather`
  * `mart_daily_climate_dashboard`
  * `mart_location_climate_summary`
  * `mart_monthly_climate_summary`
* Created dbt tests for staging, dimension, fact, and mart models.
* Added a relationship test from `fact_daily_weather.location_id` to `dim_location.location_id`.
* Added custom dbt tests for:

  * fact table grain;
  * daily mart grain;
  * monthly mart grain;
  * metric ranges.
* Updated the pipeline runner to execute:

  * API extraction;
  * raw JSON loading;
  * `dbt run`;
  * `dbt test`.
* Added `--dbt-target` support to run against different dbt profile targets.
* Added Docker Compose services for:

  * PostgreSQL
  * Metabase
* Added a daily scheduler script:

  * `scripts/run_daily_pipeline.sh`
* Added scheduling documentation:

  * `docs/scheduling.md`
* Built and documented the Metabase dashboard:

  * `docs/dashboard.md`

## Verified Outputs

Current Docker test database after loading the initial sample period and later daily runs:

* `staging.stg_nasa_power_responses`: 32 rows
* `staging.stg_daily_weather`: 80 rows
* `dim.dim_location`: 8 rows
* `fact.fact_daily_weather`: 80 rows
* `mart.mart_daily_climate_dashboard`: 80 rows
* `mart.mart_location_climate_summary`: 8 rows
* `mart.mart_monthly_climate_summary`: 16 rows

Full dbt validation:

```text
dbt run  -> PASS=7
dbt test -> PASS=35
```

The full Docker pipeline runner also completed successfully:

```text
DATABASE_URL="postgresql://nasa_user:nasa_password@localhost:5433/nasa_climate_project" python scripts/run_pipeline.py --start 20240101 --end 20240107 --dbt-target docker
```

## Dashboard Coverage

The Metabase dashboard is named:

```text
NASA Climate Dashboard
```

Current dashboard blocks:

* Daily Average Temperature by City
* Rainy Days by City
* High Humidity Days by City
* Total Solar Radiation by City
* Average Daily Temperature Range by City
* Location Climate Summary

The dashboard answers the main business questions from `docs/business_requirements.md`.

## Data Notes

Near-real-time NASA POWER responses may return `-999.0` fill values before final metric values are available.

The staging layer converts these fill values to `NULL`.

Metric fields are allowed to be `NULL` when the source data is missing. This keeps missing values as unknown instead of replacing them with fake zeroes.

Boolean fields that depend on missing metrics can also be `NULL`. For example, if precipitation is missing, `is_rainy_day` is unknown rather than false.

## Current Data Quality Coverage

The project currently uses dbt tests for:

* non-null key fields;
* unique raw response identifiers;
* unique location identifiers;
* fact-to-dimension relationship validation;
* fact table grain validation;
* daily mart grain validation;
* monthly mart grain validation;
* location summary uniqueness by location;
* basic metric range validation.

Earlier SQL data quality scripts are still kept in the repository, but dbt is now the main transformation and validation layer.

## Repository Notes

Generated raw JSON files and processed CSV files are not committed to Git.

Local dbt files are also ignored:

```text
profiles/profiles.yml
profiles/.user.yml
logs/
target/
```

Local environment and generated files are ignored:

```text
.venv/
__pycache__/
*.pyc
.DS_Store
data/raw/*.json
data/processed/*.csv
```

The tracked repository contains the code, SQL setup files, dbt models, dbt tests, Docker Compose setup, scheduler script, documentation, and configuration needed to recreate the pipeline.

The current project is complete as an end-to-end local ELT project.
