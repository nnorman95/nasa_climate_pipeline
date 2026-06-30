# Scheduling

This project can be scheduled with `cron` for a simple daily batch run.

The scheduled job runs the same pipeline as a manual daily run:

```text
NASA POWER API
-> raw JSON files
-> PostgreSQL raw JSONB table
-> dbt models
-> dbt tests
```

## Daily Pipeline Script

The daily runner is:

```bash
scripts/run_daily_pipeline.sh
```

It runs:

```bash
python scripts/run_pipeline.py
```

When no `--start` and `--end` arguments are provided, the pipeline automatically uses yesterday's date.

## Manual Test

Before adding a cron schedule, test the script manually from the project root:

```bash
scripts/run_daily_pipeline.sh
```

A successful run ends with:

```text
dbt run  -> PASS=6
dbt test -> PASS=28
Pipeline finished successfully
```

## Cron Example

Open the cron editor:

```bash
crontab -e
```

Add this line to run the pipeline every day at 03:00:

```cron
0 3 * * * /Users/norman/Documents/S/Data\ Engineering/nasa_climate_pipeline/scripts/run_daily_pipeline.sh >> /Users/norman/Documents/S/Data\ Engineering/nasa_climate_pipeline/logs/pipeline.log 2>&1
```

## Cron Syntax

```text
0 3 * * *
```

means:

```text
minute: 0
hour: 3
day of month: every day
month: every month
day of week: every day
```

So the job runs every day at `03:00`.

## Log Output

The cron command appends output to:

```text
logs/pipeline.log
```

`logs/` is ignored by Git, so local run logs are not committed.

## Notes

The cron command uses escaped spaces in the project path:

```text
Data\ Engineering
```

This is needed because the project folder path contains a space.

For local development, the cron schedule is documented but does not need to be enabled unless daily automatic runs are required.
