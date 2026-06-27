# NASA Climate ELT Pipeline

A small data engineering portfolio project that collects daily climate data from the NASA POWER API and builds a PostgreSQL warehouse model for climate monitoring.

The project is built as a second portfolio project after the Online Retail pipeline. The focus here is API extraction, raw JSON loading, ELT design, data warehouse modeling, and data quality checks.

## Project Goal

Build a batch ELT pipeline that:

1. extracts daily climate data from the NASA POWER API;
2. stores raw API responses as JSONB in PostgreSQL;
3. transforms raw JSON into daily weather rows;
4. builds dimension, fact, and mart tables;
5. runs SQL data quality checks;
6. can be rerun without duplicating raw records.

## Pipeline Flow

```text
NASA POWER API
-> raw JSON files
-> PostgreSQL raw JSONB table
-> staging daily weather table
-> dimension and fact tables
-> dashboard-ready marts
-> data quality checks
```

## Data Source

The project uses the NASA POWER Daily API for point locations.

Climate parameters:

* `T2M`: temperature at 2 meters
* `T2M_MAX`: maximum temperature at 2 meters
* `T2M_MIN`: minimum temperature at 2 meters
* `RH2M`: relative humidity at 2 meters
* `WS2M`: wind speed at 2 meters
* `PRECTOTCORR`: corrected precipitation
* `ALLSKY_SFC_SW_DWN`: solar radiation

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
* SQL
* NASA POWER API
* JSON / JSONB
* Git

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── config/
│   └── locations.json
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── docs/
│   └── business_requirements.md
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

## Warehouse Layers

### Raw

`raw.nasa_power_responses`

Stores one row per location and API request period. The full NASA response is stored as PostgreSQL `JSONB`.

### Staging

`staging.stg_daily_weather`

Converts nested NASA JSON into one row per location per day. NASA fill values such as `-999.0` are converted to `NULL`.

### Dimension

`dim.dim_location`

Stores location attributes such as city, country, latitude, and longitude.

### Fact

`fact.fact_daily_weather`

Stores daily weather measurements by location and date.

### Marts

`mart.mart_daily_climate_dashboard`

Dashboard-ready daily table with derived fields such as:

* `temperature_range_c`
* `is_rainy_day`
* `is_high_humidity_day`

`mart.mart_location_climate_summary`

Period-level summary by location.

`mart.mart_monthly_climate_summary`

Monthly climate summary by location.

## Data Quality Checks

The project includes SQL checks for:

* staging row count;
* duplicate `location_id + weather_date` rows;
* missing key fields;
* invalid metric ranges;
* missing metric values;
* mart row counts;
* invalid summary day counts;
* monthly mart missing average temperature warnings.

During testing, near-real-time NASA responses returned `-999.0` fill values for some metrics. The staging layer converts those values to `NULL`, and the DQ checks report missing metric values separately.

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

Run the full pipeline for a specific period:

```bash
python scripts/run_pipeline.py --start 20240101 --end 20240107
```

Run the daily pipeline for yesterday:

```bash
python scripts/run_pipeline.py
```

## Example Outputs

After loading 8 locations for 7 days:

```text
8 locations x 7 days = 56 daily weather rows
```

After adding one daily run:

```text
raw.nasa_power_responses: 16 rows
staging.stg_daily_weather: 64 rows
mart.mart_daily_climate_dashboard: 64 rows
```

## Notes

Generated raw JSON and processed CSV files are not committed to Git. They can be recreated by running the pipeline.

This version uses Python, PostgreSQL, and SQL files. Future improvements may include dbt, Docker, scheduling, and a dashboard.