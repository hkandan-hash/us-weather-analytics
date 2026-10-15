"""Download one year of daily weather for several US cities from Open-Meteo (no API key)."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

API_URL = "https://archive-api.open-meteo.com/v1/archive"
YEAR = 2025
CITIES = {
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "Los Angeles": (34.0522, -118.2437),
}
DAILY = ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
         "precipitation_sum", "wind_speed_10m_max"]
OUT = Path("data/daily_weather.csv")


def fetch_city(name: str, lat: float, lon: float) -> pd.DataFrame:
    params = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon,
        "start_date": f"{YEAR}-01-01", "end_date": f"{YEAR}-12-31",
        "daily": ",".join(DAILY), "timezone": "auto",
    })
    with urllib.request.urlopen(f"{API_URL}?{params}", timeout=60) as resp:
        payload = json.load(resp)
    df = pd.DataFrame(payload["daily"]).rename(columns={"time": "date"})
    df.insert(0, "city", name)
    return df


def main() -> None:
    frames = [fetch_city(name, lat, lon) for name, (lat, lon) in CITIES.items()]
    df = pd.concat(frames, ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} rows to {OUT}")


if __name__ == "__main__":
    main()
