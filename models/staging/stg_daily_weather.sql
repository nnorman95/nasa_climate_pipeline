SELECT
    r.location_id,
    r.city,
    r.country,
    r.latitude,
    r.longitude,
    TO_DATE(d.nasa_date, 'YYYYMMDD') AS weather_date,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'T2M', d.nasa_date])::NUMERIC, -999.0) AS temperature_avg_c,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'T2M_MAX', d.nasa_date])::NUMERIC, -999.0) AS temperature_max_c,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'T2M_MIN', d.nasa_date])::NUMERIC, -999.0) AS temperature_min_c,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'RH2M', d.nasa_date])::NUMERIC, -999.0) AS relative_humidity_pct,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'WS2M', d.nasa_date])::NUMERIC, -999.0) AS wind_speed_m_s,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'PRECTOTCORR', d.nasa_date])::NUMERIC, -999.0) AS precipitation_mm,
    NULLIF((r.response_json #>> ARRAY['properties', 'parameter', 'ALLSKY_SFC_SW_DWN', d.nasa_date])::NUMERIC, -999.0) AS solar_radiation_kwh_m2_day,    
    r.loaded_at
FROM raw.nasa_power_responses AS r
CROSS JOIN LATERAL jsonb_object_keys(
    r.response_json #> '{properties,parameter,T2M}'
) AS d(nasa_date)
