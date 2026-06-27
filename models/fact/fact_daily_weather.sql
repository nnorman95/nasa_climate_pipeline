SELECT
    location_id,
    weather_date,
    temperature_avg_c,
    temperature_max_c,
    temperature_min_c,
    relative_humidity_pct,
    wind_speed_m_s,
    precipitation_mm,
    solar_radiation_kwh_m2_day,
    loaded_at
FROM {{ ref('stg_daily_weather') }}
