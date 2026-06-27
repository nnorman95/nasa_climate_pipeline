from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from nasa_climate_pipeline.nasa_power import (  # noqa: E402
    fetch_daily_power_data,
    raw_output_path,
)
from nasa_climate_pipeline.transform import OUTPUT_COLUMNS, power_json_to_rows  # noqa: E402


LOCATIONS_FILE = PROJECT_ROOT / "config" / "locations.json"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def read_locations() -> list[dict]:
    with LOCATIONS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path: Path, payload: dict) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def write_csv(file_path: Path, rows: list[dict]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch daily NASA POWER climate data.")
    parser.add_argument("--start", required=True, help="Start date in YYYYMMDD format.")
    parser.add_argument("--end", required=True, help="End date in YYYYMMDD format.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    locations = read_locations()
    all_rows = []

    for location in locations:
        payload = fetch_daily_power_data(location, args.start, args.end)

        raw_path = raw_output_path(
            RAW_DIR,
            location["location_id"],
            args.start,
            args.end,
        )
        write_json(raw_path, payload)

        rows = power_json_to_rows(payload, location)
        all_rows.extend(rows)
        print(f"Fetched {len(rows)} rows for {location['city']}")

    csv_path = PROCESSED_DIR / f"daily_weather_{args.start}_{args.end}.csv"
    write_csv(csv_path, all_rows)
    print(f"Saved {len(all_rows)} total rows to {csv_path}")


if __name__ == "__main__":
    main()

