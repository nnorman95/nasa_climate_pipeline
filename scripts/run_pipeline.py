from __future__ import annotations

from datetime import date, timedelta
import argparse
import os
import subprocess
import sys
from pathlib import Path

import certifi


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full NASA climate ELT pipeline.")
    parser.add_argument("--start", help="Start date in YYYYMMDD format.")
    parser.add_argument("--end", help="End date in YYYYMMDD format.")
    parser.add_argument(
    "--dbt-target",
    default="dev",
    help="dbt target to use from profiles.yml. Default: dev.",
)
    return parser.parse_args()


def run_command(command: list[str]) -> None:
    env = os.environ.copy()
    env["SSL_CERT_FILE"] = certifi.where()

    subprocess.run(command, cwd=PROJECT_ROOT, check=True, env=env)


def resolve_date_range(args: argparse.Namespace) -> tuple[str, str]:
    if args.start and args.end:
        return args.start, args.end

    if args.start or args.end:
        raise ValueError("Please provide both --start and --end, or neither.")

    yesterday = date.today() - timedelta(days=1)
    yesterday_text = yesterday.strftime("%Y%m%d")
    return yesterday_text, yesterday_text

def main() -> None:
    args = parse_args()
    start, end = resolve_date_range(args)

    print("Step 1/4: Extract NASA POWER data")
    run_command([
        sys.executable,
        "scripts/fetch_power.py",
        "--start",
        start,
        "--end",
        end,
    ])

    print("Step 2/4: Load raw JSON files into PostgreSQL")
    run_command([sys.executable, "scripts/load_raw.py"])

    print("Step 3/4: Build dbt warehouse models")
    run_command([
        "dbt",
        "run",
        "--profiles-dir",
        "profiles",
        "--target",
        args.dbt_target,
    ])

    print("Step 4/4: Run dbt data quality tests")
    run_command([
        "dbt",
        "test",
        "--profiles-dir",
        "profiles",
        "--target",
        args.dbt_target,
    ])

    print("Pipeline finished successfully")


if __name__ == "__main__":
    main()
