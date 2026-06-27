from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

DEFAULT_PARAMETERS = [
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "RH2M",
    "WS2M",
    "PRECTOTCORR",
    "ALLSKY_SFC_SW_DWN",
]


def build_power_params(location: dict[str, Any], start: str, end: str) -> dict[str, str]:
    return {
        "parameters": ",".join(DEFAULT_PARAMETERS),
        "community": "RE",
        "longitude": str(location["longitude"]),
        "latitude": str(location["latitude"]),
        "start": start,
        "end": end,
        "format": "JSON",
        "time-standard": "UTC",
    }


def fetch_daily_power_data(location: dict[str, Any], start: str, end: str) -> dict[str, Any]:
    params = build_power_params(location, start, end)
    request_url = f"{BASE_URL}?{urlencode(params)}"
    request = Request(
        request_url,
        headers={"User-Agent": "nasa-climate-pipeline/0.1"},
    )

    try:
        with urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as error:
        raise RuntimeError(
            f"NASA POWER API returned HTTP {error.code} for {location['city']}. "
            f"Request URL: {request_url}"
        ) from error
    except URLError as error:
        raise RuntimeError(
            f"Could not connect to NASA POWER API for {location['city']}. "
            f"Request URL: {request_url}"
        ) from error

    return json.loads(response_body)


def raw_output_path(raw_dir: Path, location_id: str, start: str, end: str) -> Path:
    return raw_dir / f"nasa_power_{location_id}_{start}_{end}.json"
