SELECT DISTINCT
    location_id,
    city,
    country,
    latitude,
    longitude
FROM {{ ref('stg_daily_weather') }}
