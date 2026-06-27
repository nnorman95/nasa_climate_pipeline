# NASA Climate Data Pipeline

Mini data engineering project that extracts daily climate data from the NASA POWER API.

The project is planned as a second portfolio project after the Online Retail pipeline.
Its goal is to show modern data engineering tools around an API-based data source:

```text
NASA POWER API -> raw JSON -> tabular data -> PostgreSQL -> dbt -> tests -> dashboard
```

## Data Source

NASA POWER provides solar and meteorological data from satellite observations and models.
This project uses the Daily API for point locations.

Initial parameters:

- `T2M`: temperature at 2 meters
- `T2M_MAX`: maximum temperature at 2 meters
- `T2M_MIN`: minimum temperature at 2 meters
- `RH2M`: relative humidity at 2 meters
- `WS2M`: wind speed at 2 meters
- `PRECTOTCORR`: corrected precipitation
- `ALLSKY_SFC_SW_DWN`: solar radiation

## Initial Locations

- Baku
- Istanbul
- London
- New York
- Tokyo
- Paris
- Rome
- Cairo, Egypt

## Current Project Structure

```text
.
├── README.md
├── requirements.txt
├── config/
│   └── locations.json
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   └── fetch_power.py
├── src/
│   └── nasa_climate_pipeline/
│       ├── __init__.py
│       ├── nasa_power.py
│       └── transform.py
└── sql/
```

## First Run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Fetch a small test range:

```bash
python scripts/fetch_power.py --start 20240101 --end 20240107
```

Expected result:

```text
data/raw/nasa_power_<location>_20240101_20240107.json
data/processed/daily_weather_20240101_20240107.csv
```

## Next Steps

- Load processed data into PostgreSQL.
- Add raw metadata table.
- Add dbt staging, fact, dimension, and mart models.
- Add dbt tests for uniqueness, not-null fields, accepted ranges, and row counts.
- Add Docker.
- Add Airflow or cron scheduling.
- Add dashboard.
