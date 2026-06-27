ALTER TABLE raw.nasa_power_responses
ADD CONSTRAINT uq_nasa_power_location_period
UNIQUE (location_id, start_date, end_date);
