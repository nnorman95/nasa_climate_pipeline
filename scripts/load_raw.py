from __future__ import annotations

import json
from pathlib import Path

from datetime import datetime

import psycopg
from psycopg.types.json import Jsonb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
LOCATIONS_FILE = PROJECT_ROOT / "config" / "locations.json"
DB_NAME = "nasa_climate_project"

def get_raw_files() -> list[Path]:
    return sorted(RAW_DIR.glob("*.json"))



def read_json_file(file_path: Path) -> dict:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)



def read_locations_by_id() -> dict:
    with LOCATIONS_FILE.open("r", encoding="utf-8") as file:
        locations = json.load(file)

    return {location["location_id"]: location for location in locations}



def parse_raw_filename(file_path: Path) -> dict[str, str]:
    filename = file_path.stem
    prefix = "nasa_power_"

    if not filename.startswith(prefix):
        raise ValueError(f"Unexpected raw file name: {file_path.name}")

    name_without_prefix = filename.removeprefix(prefix)
    parts = name_without_prefix.rsplit("_", 2)

    if len(parts) != 3:
        raise ValueError(f"Could not parse raw file name: {file_path.name}")

    location_id, start_date, end_date = parts

    return {
        "location_id": location_id,
        "start_date": start_date,
        "end_date": end_date,
    }



def parse_date(value: str) -> str:
    return datetime.strptime(value, "%Y%m%d").date().isoformat()



def build_raw_record(file_path: Path, locations_by_id: dict) -> dict:
    parsed = parse_raw_filename(file_path)
    location = locations_by_id[parsed["location_id"]]
    payload = read_json_file(file_path)

    return {
        "location_id": parsed["location_id"],
        "city": location["city"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "start_date": parse_date(parsed["start_date"]),
        "end_date": parse_date(parsed["end_date"]),
        "source_file": file_path.name,
        "response_json": payload,
    }

def get_connection() -> psycopg.Connection:
    return psycopg.connect(f"dbname={DB_NAME}")

def insert_raw_record(conn: psycopg.Connection, record: dict) -> int:
    sql = """
        INSERT INTO raw.nasa_power_responses (
            location_id,
            city,
            country,
            latitude,
            longitude,
            start_date,
            end_date,
            source_file,
            response_json
        )
        VALUES (
            %(location_id)s,
            %(city)s,
            %(country)s,
            %(latitude)s,
            %(longitude)s,
            %(start_date)s,
            %(end_date)s,
            %(source_file)s,
            %(response_json)s
        )
        ON CONFLICT ON CONSTRAINT uq_nasa_power_location_period
        DO NOTHING;
    """

    values = {
        **record,
        "response_json": Jsonb(record["response_json"]),
    }

    with conn.cursor() as cur:
        cur.execute(sql, values)
        return cur.rowcount


def main() -> None:
    raw_files = get_raw_files()
    locations_by_id = read_locations_by_id()

    inserted_total = 0

    print(f"Found {len(raw_files)} raw JSON files")

    with get_connection() as conn:
        for file_path in raw_files:
            record = build_raw_record(file_path, locations_by_id)
            inserted_rows = insert_raw_record(conn, record)
            inserted_total += inserted_rows

            print(f"{file_path.name}: inserted {inserted_rows}")

    print(f"Inserted total rows: {inserted_total}")




if __name__ == "__main__":
    main()