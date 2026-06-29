SELECT
    location_id,
    weather_date,
    COUNT(*) AS row_count
FROM {{ ref('fact_daily_weather') }}
GROUP BY
    location_id,
    weather_date
HAVING COUNT(*) > 1
