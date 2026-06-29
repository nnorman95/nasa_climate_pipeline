SELECT
    location_id,
    month_start,
    COUNT(*) AS row_count
FROM {{ ref('mart_monthly_climate_summary') }}
GROUP BY
    location_id,
    month_start
HAVING COUNT(*) > 1
