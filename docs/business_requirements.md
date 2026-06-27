# Business Requirements

## Why This Project Exists

The analytics team wants a small climate monitoring pipeline based on NASA POWER daily data.

The goal is not just to store weather data, but to make it useful for simple reporting:
which days were rainy, which locations had high humidity, how temperature changed by day,
and where solar radiation was stronger during the loaded period.

This project uses a small set of selected locations as a training version of a real ELT workflow.

## Main Questions

The dashboard should help answer these questions:

1. What were the daily weather conditions for each location?
2. Which days had rain?
3. Which days had high humidity?
4. What was the daily temperature range?
5. How much solar radiation did each location receive?
6. What is the short period summary for each location?

## Metrics Needed

- Average temperature
- Minimum temperature
- Maximum temperature
- Temperature range
- Relative humidity
- Wind speed
- Precipitation
- Solar radiation
- Rainy day flag
- High humidity flag

## Data Marts

### mart_daily_climate_dashboard

Grain: one row per location per day.

This table is used for daily dashboard charts and filters.

### mart_location_climate_summary

Grain: one row per location per loaded period.

This table is used for quick summary reporting by location.
