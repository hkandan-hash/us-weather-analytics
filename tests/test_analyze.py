import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import analyze  # noqa: E402


def make_df():
    dates = pd.date_range("2025-01-01", "2025-12-31")
    n = len(dates)
    return pd.DataFrame({
        "city": ["A"] * n,
        "date": dates.strftime("%Y-%m-%d"),
        "temperature_2m_mean": [10.0] * n,
        "temperature_2m_max": [31.0 if i == 5 else 15.0 for i in range(n)],
        "temperature_2m_min": [-5.0 if i == 9 else 2.0 for i in range(n)],
        "precipitation_sum": [2.0 if i % 10 == 0 else 0.0 for i in range(n)],
        "wind_speed_10m_max": [20.0] * n,
    })


def test_clean_drops_duplicates_and_null_temps():
    df = make_df()
    df = pd.concat([df, df.iloc[:3]])
    df.loc[df.index[10], "temperature_2m_mean"] = None
    cleaned = analyze.clean(df)
    assert len(cleaned) == 364


def test_summary_counts():
    g = analyze.clean(make_df())
    s = analyze.city_summary(g)
    assert s["hot_days"] == 1
    assert s["hottest_c"] == 31.0
    assert s["coldest_c"] == -5.0
    assert s["rainy_days"] == 37


def test_build_shapes():
    data = analyze.build(analyze.clean(make_df()))
    assert data["cities"] == ["A"]
    assert len(data["monthly_temp"]["A"]) == 12
    assert len(data["monthly_precip"]["A"]) == 12
    assert len(data["daily"]["A"]["dates"]) == len(data["daily"]["A"]["temp7"]) == 365
