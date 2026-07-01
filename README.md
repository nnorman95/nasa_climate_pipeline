# NASA Climate ELT Pipeline

A batch ELT pipeline that collects daily climate data from the NASA POWER API and builds PostgreSQL warehouse tables for climate monitoring, reporting, and dashboarding.

The pipeline starts from real API extraction, keeps the raw NASA response as JSONB, uses dbt to build cleaned staging tables, warehouse models, dashboard-ready marts, and data quality tests, and exposes the final mart layer through Metabase.

## Project Goal

The goal is to turn daily NASA POWER climate data into structured tables that can answer practical monitoring questions:

1. what daily weather conditions were recorded for each location;
2. how temperature, precipitation, humidity, wind, and solar radiation changed over time;
3. which locations had more rainy or high-humidity days;
4. what the daily temperature range looked like by location;
5. how much solar radiation each location received;
6. how each location looks at a short-period and monthly summary level;
7. whether the pipeline can be rerun safely without duplicating raw API responses.

## Pipeline Flow

```text
NASA POWER API
--> raw JSON files
--> PostgreSQL raw JSONB table
--> dbt staging models
--> dbt dimension and fact models
--> dbt marts
--> dbt data tests
--> Metabase dashboard
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
* Docker Compose
* Metabase
* SQL
* NASA POWER API
* JSON / JSONB
* cron
* Git

## Project Structure

```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── dbt_project.yml
├── docker-compose.yml
├── config/
│   └── locations.json
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── docs/
│   ├── business_requirements.md
│   ├── dashboard.md
│   ├── project_status.md
│   └── scheduling.md
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
│       ├── mart_location_climate_summary.sql
│       └── mart_monthly_climate_summary.sql
├── profiles/
│   └── profiles.example.yml
├── scripts/
│   ├── fetch_power.py
│   ├── load_raw.py
│   ├── build_models.py
│   ├── run_daily_pipeline.sh
│   └── run_pipeline.py
├── src/
│   └── nasa_climate_pipeline/
│       ├── __init__.py
│       ├── nasa_power.py
│       └── transform.py
├── tests/
│   ├── assert_fact_daily_weather_metric_ranges.sql
│   ├── assert_fact_daily_weather_unique_grain.sql
│   ├── assert_mart_daily_climate_dashboard_unique_grain.sql
│   └── assert_mart_monthly_climate_summary_unique_grain.sql
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

`profiles/profiles.yml`, `profiles/.user.yml`, `logs/`, and `target/` are local dbt files and are ignored by Git. Generated raw JSON and processed CSV files are also ignored because they can be recreated by running the pipeline.

The `sql/` folder keeps the raw table setup and earlier SQL build scripts. dbt is now the main warehouse transformation and validation layer.

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

`mart.mart_location_climate_summary`

Short-period summary by location. This table is used for quick location-level reporting across the loaded data period.

`mart.mart_monthly_climate_summary`

Monthly climate summary by location. This table is better for trend analysis than comparing long uneven date ranges directly.

## Data Quality

The project uses dbt tests for key warehouse checks:

* non-null key fields;
* unique raw response identifiers;
* unique location identifiers in the location dimension;
* relationship validation between fact and dimension models;
* fact table grain validation;
* daily mart grain validation;
* monthly mart grain validation;
* location summary uniqueness by location;
* basic metric range validation.

Current dbt validation result:

```text
dbt run  -> PASS=7
dbt test -> PASS=35
```

Some metric fields are allowed to be `NULL`. This is intentional because NASA may return missing values for near-real-time data. The pipeline keeps those values as unknown instead of replacing them with fake zeroes.

## How to Run Locally

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

## Docker Setup

The project can also run against Docker services:

```text
PostgreSQL -> warehouse database
Metabase   -> dashboard UI
```

Start the services:

```bash
docker compose up -d
```

PostgreSQL is exposed to the host machine on port `5433`:

```text
localhost:5433
```

Metabase is available in the browser:

```text
http://localhost:3000
```

Create raw tables and constraints in the Docker database:

```bash
PGPASSWORD=nasa_password psql -h localhost -p 5433 -U nasa_user -d nasa_climate_project -f sql/01_create_raw_tables.sql
PGPASSWORD=nasa_password psql -h localhost -p 5433 -U nasa_user -d nasa_climate_project -f sql/02_add_raw_constraints.sql
```

Check the Docker database connection:

```bash
PGPASSWORD=nasa_password psql -h localhost -p 5433 -U nasa_user -d nasa_climate_project -c "SELECT version();"
```

Check the dbt Docker target:

```bash
dbt debug --profiles-dir profiles --target docker
```

Run the full pipeline against Docker PostgreSQL:

```bash
DATABASE_URL="postgresql://nasa_user:nasa_password@localhost:5433/nasa_climate_project" python scripts/run_pipeline.py --start 20240101 --end 20240107 --dbt-target docker
```

Stop Docker services:

```bash
docker compose down
```

Stop Docker services and remove volume data:

```bash
docker compose down -v
```

## Metabase Dashboard

The project includes a Metabase dashboard layer.

Metabase connects to PostgreSQL inside the Docker network with:

```text
Host: postgres
Port: 5432
Database: nasa_climate_project
Username: nasa_user
Password: nasa_password
```

The dashboard is named:

```text
NASA Climate Dashboard
```

Dashboard documentation and SQL queries are stored in:

```text
docs/dashboard.md
```

Current dashboard blocks:

* Daily Average Temperature by City
* Rainy Days by City
* High Humidity Days by City
* Total Solar Radiation by City
* Average Daily Temperature Range by City
* Location Climate Summary

## Scheduling

The repository includes a small shell script for daily runs:

```text
scripts/run_daily_pipeline.sh
```

It activates the virtual environment and runs:

```bash
python scripts/run_pipeline.py
```

Cron setup notes are documented in:

```text
docs/scheduling.md
```

## Example Output

After loading 8 locations for 7 days:

```text
8 locations x 7 days = 56 daily weather rows
```

After loading the initial sample period and later daily runs, row counts depend on how many request periods have been loaded. In the current Docker test database, the full dbt build produced:

```text
staging.stg_nasa_power_responses: 32 rows
staging.stg_daily_weather: 80 rows
dim.dim_location: 8 rows
fact.fact_daily_weather: 80 rows
mart.mart_daily_climate_dashboard: 80 rows
mart.mart_location_climate_summary: 8 rows
mart.mart_monthly_climate_summary: 16 rows
```

A successful full dbt validation ends with:

```text
dbt run  -> PASS=7
dbt test -> PASS=35
```

The full pipeline runner ends with:

```text
Pipeline finished successfully
```

## Notes

Generated raw JSON and processed CSV files are not committed to Git. They can be recreated by running the pipeline.

Docker PostgreSQL uses port `5433` to avoid conflicts with a local PostgreSQL server on port `5432`.

The raw table is designed to be rerunnable. A unique constraint on `location_id`, `start_date`, and `end_date` prevents duplicate raw API loads for the same location and request period.

Metabase dashboards and questions are stored inside the Metabase Docker volume. The repository documents the dashboard design and SQL queries in `docs/dashboard.md`.
