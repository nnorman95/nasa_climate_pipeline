# Metabase Dashboard

## Dashboard Name

NASA Climate Dashboard

## Purpose

The dashboard shows the final BI layer of the NASA climate ELT pipeline. It uses dbt mart tables from PostgreSQL and answers the main climate monitoring questions from the business requirements.

Main data source:

```text
mart.mart_daily_climate_dashboard
mart.mart_location_climate_summary
```

## Dashboard Blocks

### Daily Average Temperature by City

Business question:

```text
How did average temperature change by day for each location?
```

Visualization:

```text
Line chart
X-axis: weather_date
Y-axis: temperature_avg_c
Series: city
```

SQL:

```sql
SELECT
    weather_date,
    city,
    country,
    temperature_avg_c
FROM mart.mart_daily_climate_dashboard
WHERE temperature_avg_c IS NOT NULL
ORDER BY weather_date, city;
```

### Rainy Days by City

Business question:

```text
Which locations had more rainy days during the loaded period?
```

Visualization:

```text
Bar chart
X-axis: city
Y-axis: rainy_days
```

SQL:

```sql
SELECT
    city,
    country,
    COUNT(*) FILTER (WHERE is_rainy_day IS TRUE) AS rainy_days,
    COUNT(*) AS total_days
FROM mart.mart_daily_climate_dashboard
GROUP BY city, country
ORDER BY rainy_days DESC;
```

### High Humidity Days by City

Business question:

```text
Which locations had more high humidity days during the loaded period?
```

Visualization:

```text
Bar chart
X-axis: city
Y-axis: high_humidity_days
```

SQL:

```sql
SELECT
    city,
    country,
    COUNT(*) FILTER (WHERE is_high_humidity_day IS TRUE) AS high_humidity_days,
    COUNT(*) AS total_days
FROM mart.mart_daily_climate_dashboard
GROUP BY city, country
ORDER BY high_humidity_days DESC;
```

### Total Solar Radiation by City

Business question:

```text
How much solar radiation did each location receive?
```

Visualization:

```text
Bar chart
X-axis: city
Y-axis: total_solar_radiation_kwh_m2
```

SQL:

```sql
SELECT
    city,
    country,
    ROUND(SUM(solar_radiation_kwh_m2_day)::numeric, 2) AS total_solar_radiation_kwh_m2,
    ROUND(AVG(solar_radiation_kwh_m2_day)::numeric, 2) AS avg_daily_solar_radiation_kwh_m2,
    COUNT(solar_radiation_kwh_m2_day) AS days_with_solar_data
FROM mart.mart_daily_climate_dashboard
WHERE solar_radiation_kwh_m2_day IS NOT NULL
GROUP BY city, country
ORDER BY total_solar_radiation_kwh_m2 DESC;
```

### Average Daily Temperature Range by City

Business question:

```text
What was the daily temperature range by location?
```

Visualization:

```text
Bar chart
X-axis: city
Y-axis: avg_temperature_range_c
```

SQL:

```sql
SELECT
    city,
    country,
    ROUND(AVG(temperature_range_c)::numeric, 2) AS avg_temperature_range_c,
    ROUND(MIN(temperature_range_c)::numeric, 2) AS min_temperature_range_c,
    ROUND(MAX(temperature_range_c)::numeric, 2) AS max_temperature_range_c,
    COUNT(temperature_range_c) AS days_with_temperature_range_data
FROM mart.mart_daily_climate_dashboard
WHERE temperature_range_c IS NOT NULL
GROUP BY city, country
ORDER BY avg_temperature_range_c DESC;
```

### Location Climate Summary

Business question:

```text
What is the short period summary for each location?
```

Visualization:

```text
Table
```

SQL:

```sql
SELECT
    city,
    country,
    period_start,
    period_end,
    day_count,
    avg_temperature_c,
    min_temperature_c,
    max_temperature_c,
    avg_temperature_range_c,
    avg_relative_humidity_pct,
    high_humidity_day_count,
    avg_wind_speed_m_s,
    total_precipitation_mm,
    rainy_day_count,
    avg_solar_radiation_kwh_m2_day
FROM mart.mart_location_climate_summary
ORDER BY city;
```

## Visualization Notes

The dashboard uses line charts only for time-based trends.

Bar charts are used for comparing cities because `city` is a categorical variable and the measured values are numeric.

The dashboard avoids pie charts, dual axes, and unnecessary colors to keep the visuals readable.
