# NASA Climate ELT Pipeline

A batch ELT pipeline that collects daily climate data from the NASA POWER API and builds PostgreSQL warehouse tables for climate monitoring and reporting.

The pipeline starts from real API extraction, keeps the raw NASA response as JSONB, and then uses dbt to build cleaned staging tables, warehouse models, and dashboard-ready marts.

## Project Goal

The goal is to turn daily NASA POWER climate data into structured tables that can answer practical monitoring questions:

1. what daily weather conditions were recorded for each location;
2. how temperature, precipitation, humidity, wind, and solar radiation changed over time;
3. which days were rainy or highly humid;
4. how each location looks at a monthly summary level;
5. whether the pipeline can be rerun safely without duplicating raw API responses.

## Pipeline Flow

```text
NASA POWER API
-> raw JSON files
-> PostgreSQL raw JSONB table
-> dbt staging models
-> dbt dimension and fact models
-> dbt marts
-> dbt data tests
```

## Data Source

The project uses the NASA POWER Daily API for point locations.

Climate parameters used in the pipeline:

* `T2M`: temperature at 2 meters
* `T2M_MAX`: maximum temperature at 2 meters
* `T2M_MIN`: minimum temperature at 2 meters
* `RH2M`: relative humidity at 2 meters
* `WS2M`: wind speed at 2 meters
* `PRECTOTCORR`: corrected precipitation
* `ALLSKY_SFC_SW_DWN`: solar radiation

NASA can return fill values such as `-999.0` when a metric is not available yet. The staging layer converts those values to `NULL` so they are not treated as real measurements.

## Locations

* Baku, Azerbaijan
* Istanbul, Turkey
* London, United Kingdom
* New York, United States
* Tokyo, Japan
* Paris, France
* Rome, Italy
* Cairo, Egypt

## Stack

* Python
* PostgreSQL
* dbt
* SQL
* NASA POWER API
* JSON / JSONB
* Git

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── dbt_project.yml
├── config/
│   └── locations.json
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── docs/
│   ├── business_requirements.md
│   └── project_status.md
├── macros/
│   └── generate_schema_name.sql
├── models/
│   ├── staging/
│   │   ├── schema.yml
│   │   ├── stg_daily_weather.sql
│   │   └── stg_nasa_power_responses.sql
│   ├── dim/
│   │   ├── schema.yml
│   │   └── dim_location.sql
│   ├── fact/
│   │   ├── schema.yml
│   │   └── fact_daily_weather.sql
│   └── marts/
│       ├── schema.yml
│       ├── mart_daily_climate_dashboard.sql
│       └── mart_monthly_climate_summary.sql
├── profiles/
│   └── profiles.yml
├── scripts/
│   ├── fetch_power.py
│   ├── load_raw.py
│   ├── build_models.py
│   └── run_pipeline.py
├── src/
│   └── nasa_climate_pipeline/
│       ├── __init__.py
│       ├── nasa_power.py
│       └── transform.py
└── sql/
    ├── 01_create_raw_tables.sql
    ├── 02_add_raw_constraints.sql
    ├── 03_create_staging_daily_weather.sql
    ├── 04_staging_data_quality_checks.sql
    ├── 05_create_dim_location.sql
    ├── 06_create_fact_daily_weather.sql
    ├── 07_create_mart_daily_climate_dashboard.sql
    ├── 08_create_mart_location_climate_summary.sql
    ├── 09_create_mart_monthly_climate_summary.sql
    └── 10_mart_data_quality_checks.sql
```

`profiles/profiles.yml`, `logs/`, and `target/` are local dbt files and are ignored by Git. The `sql/` folder keeps the raw table setup and earlier SQL build scripts; dbt is now the main warehouse transformation layer.

## Warehouse Layers

### Raw

`raw.nasa_power_responses`

Stores one row per location and API request period. The full NASA response is stored as PostgreSQL `JSONB`.

This layer keeps the original API response available for reprocessing and debugging.

### Staging

`staging.stg_nasa_power_responses`

Stores metadata about raw NASA API responses without the full JSON payload.

`staging.stg_daily_weather`

Converts nested NASA JSON into one row per location per day. NASA fill values such as `-999.0` are converted to `NULL`.

### Dimension

`dim.dim_location`

Stores location attributes such as city, country, latitude, and longitude.

### Fact

`fact.fact_daily_weather`

Stores daily weather measurements by location and date.

The grain is:

```text
one row per location per weather_date
```

### Marts

`mart.mart_daily_climate_dashboard`

Daily reporting table with location fields, weather metrics, and derived flags:

* `temperature_range_c`
* `is_rainy_day`
* `is_high_humidity_day`

`mart.mart_monthly_climate_summary`

Monthly climate summary by location. This table is better for trend analysis than comparing long uneven date ranges directly.

## Data Quality

The project uses dbt tests for key warehouse checks:

* non-null primary fields;
* unique location identifiers in the location dimension;
* non-null dates;
* non-null location keys;
* basic mart-level key checks.

Current dbt validation result:

```text
dbt run  -> PASS=6
dbt test -> PASS=28
```

Some metric fields are allowed to be `NULL`. This is intentional because NASA may return missing values for near-real-time data. The pipeline keeps those values as unknown instead of replacing them with fake zeroes.

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the PostgreSQL database:

```bash
createdb nasa_climate_project
```

Create raw tables and constraints:

```bash
psql -d nasa_climate_project -f sql/01_create_raw_tables.sql
psql -d nasa_climate_project -f sql/02_add_raw_constraints.sql
```

Copy the example dbt profile:

```bash
cp profiles/profiles.example.yml profiles/profiles.yml
```

Then edit `profiles/profiles.yml` and set your local PostgreSQL user:

```yaml
user: your_postgres_user
```

If your local PostgreSQL requires a password, also update:

```yaml
password: ""
```

Check the dbt connection:

```bash
dbt debug --profiles-dir profiles
```

Run the full pipeline for a specific period:

```bash
python scripts/run_pipeline.py --start 20240101 --end 20240107
```

Run the daily pipeline for yesterday:

```bash
python scripts/run_pipeline.py
```

The pipeline runs these steps:

```text
Step 1: Extract NASA POWER data
Step 2: Load raw JSON files into PostgreSQL
Step 3: Build dbt warehouse models
Step 4: Run dbt data tests
```

## Example Output

After loading 8 locations for 7 days:

```text
8 locations x 7 days = 56 daily weather rows
```

After adding one daily run:

```text
raw.nasa_power_responses: 16 rows
staging.stg_daily_weather: 64 rows
fact.fact_daily_weather: 64 rows
mart.mart_daily_climate_dashboard: 64 rows
mart.mart_monthly_climate_summary: 16 rows
```

A successful full run ends with:

```text
dbt run  -> PASS=6
dbt test -> PASS=28
Pipeline finished successfully
```

## Notes

Generated raw JSON and processed CSV files are not committed to Git. They can be recreated by running the pipeline.

The raw table is designed to be rerunnable. A unique constraint on `location_id`, `start_date`, and `end_date` prevents duplicate raw API loads for the same location and request period.
