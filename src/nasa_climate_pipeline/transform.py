from __future__ import annotations

from datetime import datetime
from typing import Any


OUTPUT_COLUMNS = [
    "location_id",
    "city",
    "country",
    "latitude",
    "longitude",
    "weather_date",
    "temperature_avg_c",
    "temperature_max_c",
    "temperature_min_c",
    "relative_humidity_pct",
    "wind_speed_m_s",
    "precipitation_mm",
    "solar_radiation_kwh_m2_day",
]

PARAMETER_TO_COLUMN = {
    "T2M": "temperature_avg_c",
    "T2M_MAX": "temperature_max_c",
    "T2M_MIN": "temperature_min_c",
    "RH2M": "relative_humidity_pct",
    "WS2M": "wind_speed_m_s",
    "PRECTOTCORR": "precipitation_mm",
    "ALLSKY_SFC_SW_DWN": "solar_radiation_kwh_m2_day",
}


def parse_nasa_date(value: str) -> str:
    return datetime.strptime(value, "%Y%m%d").date().isoformat()


def clean_value(value: Any, fill_value: Any) -> Any:
    if value == fill_value:
        return None
    return value


def power_json_to_rows(
    payload: dict[str, Any],
    location: dict[str, Any],
) -> list[dict[str, Any]]:
    parameters = payload["properties"]["parameter"]
    fill_value = payload.get("header", {}).get("fill_value")

    first_parameter = next(iter(parameters.values()))
    date_keys = sorted(first_parameter.keys())

    rows = []
    for date_key in date_keys:
        row = {
            "location_id": location["location_id"],
            "city": location["city"],
            "country": location["country"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "weather_date": parse_nasa_date(date_key),
        }

        for parameter_name, column_name in PARAMETER_TO_COLUMN.items():
            row[column_name] = clean_value(
                parameters[parameter_name].get(date_key),
                fill_value,
            )

        rows.append(row)

    return rows

