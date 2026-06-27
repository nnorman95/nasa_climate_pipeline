SELECT
    id,
    location_id,
    city,
    country,
    latitude,
    longitude,
    start_date,
    end_date,
    source_file,
    loaded_at
FROM raw.nasa_power_responses
