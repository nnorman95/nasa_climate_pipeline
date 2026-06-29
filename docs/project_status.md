# Project Status

# Project Status

## Current Implementation

The pipeline currently uses Python for API extraction and raw loading, PostgreSQL for raw JSONB storage, and dbt for warehouse transformations and data tests.

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
```

## Completed

* Extract data from the NASA POWER Daily API.
* Save raw API responses as JSON files.
* Save processed CSV files locally for inspection.
* Load raw API responses into PostgreSQL as JSONB.
* Prevent duplicate raw loads with a unique constraint and `ON CONFLICT DO NOTHING`.
* Convert nested NASA JSONB into daily weather rows.
* Convert NASA fill values such as `-999.0` to `NULL`.
* Created dbt project structure.
* Add local dbt profile support through `profiles/profiles.yml`.
* Add a dbt macro for direct schema naming.
* Build warehouse layers with dbt:

  * `staging`
  * `dim`
  * `fact`
  * `mart`
* Build dbt models:

  * `stg_nasa_power_responses`
  * `stg_daily_weather`
  * `dim_location`
  * `fact_daily_weather`
  * `mart_daily_climate_dashboard`
  * `mart_monthly_climate_summary`
* Created dbt tests for staging, dimension, fact, and mart models.
* Add relationship test from `fact_daily_weather.location_id` to `dim_location.location_id`.
* Add custom dbt tests for:

  * fact table grain;
  * daily mart grain;
  * monthly mart grain;
  * metric ranges.
* Update the pipeline runner to execute:

  * API extraction;
  * raw JSON loading;
  * `dbt run`;
  * `dbt test`.

## Verified Outputs

After loading the initial 7-day period and one daily run:

* `raw.nasa_power_responses`: 16 rows
* `staging.stg_nasa_power_responses`: 16 rows
* `staging.stg_daily_weather`: 64 rows
* `dim.dim_location`: 8 rows
* `fact.fact_daily_weather`: 64 rows
* `mart.mart_daily_climate_dashboard`: 64 rows
* `mart.mart_monthly_climate_summary`: 16 rows

Full dbt validation:

```text
dbt run  -> PASS=6
dbt test -> PASS=28
```

The full pipeline runner also completed successfully:

```text
python scripts/run_pipeline.py --start 20240101 --end 20240107
```

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

The tracked repository contains the code, SQL setup files, dbt models, dbt tests, documentation, and configuration needed to recreate the pipeline.
