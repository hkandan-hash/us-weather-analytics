# US Weather 2025: Analytics Dashboard

An end-to-end data analytics project: fetch a year of daily weather for four US cities, clean and aggregate it with pandas, and explore it in an interactive dashboard.

**Live dashboard:** https://hkandan-hash.github.io/us-weather-analytics/

## What the dashboard shows

- **Key figures:** hottest day, coldest day, wettest city, and the city with the most hot days
- **Temperature:** 7-day rolling average for each city across 2025
- **Precipitation:** monthly totals by city
- **Hot days:** days with a high of 30 °C or more
- **Interactions:** toggle cities on and off, hover for exact values, switch to a table view, light and dark themes

## Pipeline

```
Open-Meteo archive API
        ↓  src/fetch_data.py
data/daily_weather.csv   (1,460 rows: 4 cities × 365 days)
        ↓  src/analyze.py   (clean, rolling averages, monthly aggregates, summary stats)
docs/data.js
        ↓
docs/index.html          (Chart.js dashboard, served by GitHub Pages)
```

## Run it locally

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/fetch_data.py        # optional: re-download the data
python src/analyze.py           # rebuild docs/data.js
pytest
```

Open `docs/index.html` in a browser.

## Notes and limitations

- The data is ERA5 reanalysis served by Open-Meteo. It is a gridded model estimate, not a station reading, so extremes can differ from official weather station records.
- A "hot day" is a daily maximum at or above 30 °C. A "rainy day" is 1 mm or more of precipitation.
- One year and four cities is a small sample. Conclusions about climate would need many more years.

**Built with:** `Python` · `pandas` · `Chart.js` · `pytest` · `GitHub Actions` · `GitHub Pages`
