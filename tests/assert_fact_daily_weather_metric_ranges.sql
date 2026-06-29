SELECT
    location_id,
    weather_date,
    temperature_max_c,
    temperature_min_c,
    relative_humidity_pct,
    wind_speed_m_s,
    precipitation_mm,
    solar_radiation_kwh_m2_day
FROM {{ ref('fact_daily_weather') }}
WHERE
    (
        relative_humidity_pct IS NOT NULL
        AND (relative_humidity_pct < 0 OR relative_humidity_pct > 100)
    )
    OR (
        wind_speed_m_s IS NOT NULL
        AND wind_speed_m_s < 0
    )
    OR (
        precipitation_mm IS NOT NULL
        AND precipitation_mm < 0
    )
    OR (
        solar_radiation_kwh_m2_day IS NOT NULL
        AND solar_radiation_kwh_m2_day < 0
    )
    OR (
        temperature_max_c IS NOT NULL
        AND temperature_min_c IS NOT NULL
        AND temperature_max_c < temperature_min_c
    )
