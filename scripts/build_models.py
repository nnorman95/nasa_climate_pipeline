from __future__ import annotations

from pathlib import Path

import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"
DB_NAME = "nasa_climate_project"

SQL_FILES = [
    "03_create_staging_daily_weather.sql",
    "04_staging_data_quality_checks.sql",
    "05_create_dim_location.sql",
    "06_create_fact_daily_weather.sql",
    "07_create_mart_daily_climate_dashboard.sql",
    "08_create_mart_location_climate_summary.sql",
    "09_create_mart_monthly_climate_summary.sql",
    "10_mart_data_quality_checks.sql",
]

def read_sql(file_name: str) -> str:
    file_path = SQL_DIR / file_name
    return file_path.read_text(encoding="utf-8")

def get_connection() -> psycopg.Connection:
    return psycopg.connect(f"dbname={DB_NAME}")


def main() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            for sql_file in SQL_FILES:
                sql = read_sql(sql_file)
                cur.execute(sql)
                print(f"Built from {sql_file}")


if __name__ == "__main__":
    main()
