# Project Status

## Current Version

Version 1: Python + PostgreSQL + SQL ELT pipeline

## Completed

- Extract data from NASA POWER Daily API.
- Save raw API responses as JSON files.
- Load raw API responses into PostgreSQL as JSONB.
- Prevent duplicate raw loads with a unique constraint and `ON CONFLICT DO NOTHING`.
- Transform raw JSONB into daily weather rows.
- Convert NASA fill values such as `-999.0` to `NULL`.
- Build warehouse layers:
  - `raw`
  - `staging`
  - `dim`
  - `fact`
  - `mart`
- Build dashboard-ready marts:
  - `mart_daily_climate_dashboard`
  - `mart_location_climate_summary`
  - `mart_monthly_climate_summary`
- Add staging data quality checks.
- Add mart data quality checks.
- Add full pipeline runner:
  - manual batch mode
  - daily batch mode

## Verified Outputs

After loading the initial 7-day period and one daily run:

- `raw.nasa_power_responses`: 16 rows
- `staging.stg_daily_weather`: 64 rows
- `fact.fact_daily_weather`: 64 rows
- `mart.mart_daily_climate_dashboard`: 64 rows
- `mart.mart_monthly_climate_summary`: 16 rows

## Known Data Notes

Near-real-time NASA POWER responses may return `-999.0` fill values before final values are available.

The staging layer converts these fill values to `NULL`.

Data quality checks report missing metric values separately from invalid metric ranges.

## Next Improvements

- Add dbt models and dbt tests.
- Add Docker setup.
- Add scheduler with cron or Airflow.
- Add dashboard in Metabase, Grafana, or Power BI.
- Add CI checks.