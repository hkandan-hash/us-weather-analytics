"""Aggregate the daily weather CSV into the JSON the dashboard reads (docs/data.js)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

SRC = Path("data/daily_weather.csv")
OUT = Path("docs/data.js")
HOT_DAY_C = 30.0
RAIN_DAY_MM = 1.0


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates and rows with no temperature; fill missing precipitation with 0."""
    df = df.drop_duplicates(["city", "date"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["temperature_2m_mean"])
    df["precipitation_sum"] = df["precipitation_sum"].fillna(0.0)
    return df.sort_values(["city", "date"])


def city_summary(g: pd.DataFrame) -> dict:
    hottest = g.loc[g["temperature_2m_max"].idxmax()]
    coldest = g.loc[g["temperature_2m_min"].idxmin()]
    windiest = g.loc[g["wind_speed_10m_max"].idxmax()]
    return {
        "avg_temp": round(g["temperature_2m_mean"].mean(), 1),
        "hottest_c": round(hottest["temperature_2m_max"], 1),
        "hottest_date": hottest["date"].strftime("%b %d"),
        "coldest_c": round(coldest["temperature_2m_min"], 1),
        "coldest_date": coldest["date"].strftime("%b %d"),
        "total_precip_mm": round(g["precipitation_sum"].sum(), 1),
        "rainy_days": int((g["precipitation_sum"] >= RAIN_DAY_MM).sum()),
        "hot_days": int((g["temperature_2m_max"] >= HOT_DAY_C).sum()),
        "max_wind_kmh": round(windiest["wind_speed_10m_max"], 1),
        "max_wind_date": windiest["date"].strftime("%b %d"),
    }


def build(df: pd.DataFrame) -> dict:
    cities = list(df["city"].unique())
    months = [pd.Timestamp(2025, m, 1).strftime("%b") for m in range(1, 13)]
    out = {"cities": cities, "months": months, "hot_day_c": HOT_DAY_C,
           "rain_day_mm": RAIN_DAY_MM, "daily": {}, "monthly_temp": {},
           "monthly_precip": {}, "summary": {}}
    for city, g in df.groupby("city", sort=False):
        g = g.set_index("date")
        out["daily"][city] = {
            "dates": [d.strftime("%Y-%m-%d") for d in g.index],
            "temp7": [None if pd.isna(v) else round(v, 1)
                      for v in g["temperature_2m_mean"].rolling(7, min_periods=4).mean()],
        }
        out["monthly_temp"][city] = [round(v, 1) for v in
                                     g["temperature_2m_mean"].resample("MS").mean()]
        out["monthly_precip"][city] = [round(v, 1) for v in
                                       g["precipitation_sum"].resample("MS").sum()]
        out["summary"][city] = city_summary(g.reset_index())
    return out


def main() -> None:
    df = clean(pd.read_csv(SRC))
    data = build(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("window.DATA = " + json.dumps(data) + ";\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(df)} rows, {len(data['cities'])} cities)")


if __name__ == "__main__":
    main()
