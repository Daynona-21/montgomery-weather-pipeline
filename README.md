# Montgomery Weather App

A small Python project that fetches weather forecasts for Montgomery, Alabama, saves them in a SQLite database, and displays them in a simple Streamlit interface.

I put this project together with AI assistance to practice working with APIs, Python, and SQL.

## What it does

- Gets seven days of forecasts from the Open-Meteo API.
- Checks dates and temperatures before saving them.
- Stores forecasts in SQLite.
- Updates existing dates instead of adding duplicate records.
- Displays the forecast in a table and highlights the warmest day.
- Includes an offline mode with made-up practice data.

Temperatures are in Celsius. The data represents forecasts, not measured observations.

## Tools used

- Python
- SQL and SQLite
- REST API and JSON
- Streamlit

## How to run it

Install Python 3.9 or later and download this repository. Open a terminal inside the project folder.

Install the required package:

```bash
python -m pip install -r requirements.txt
```

Start the web interface:

```bash
python -m streamlit run app.py
```

The app opens in your browser. Click **Fetch latest forecast** to retrieve and save the data. Keep the terminal running while using the app.

To stop the app, press **Ctrl + C** in the terminal.

### Run without the interface

Fetch real forecasts:

```bash
python weather.py
```

Try the offline practice version:

```bash
python weather.py --demo
```

On Windows, use `py` instead of `python` if needed.

## Project files

| File | Purpose |
|---|---|
| `weather.py` | Fetches, checks, stores, and queries weather data |
| `app.py` | Displays the Streamlit interface |
| `sample.json` | Contains invented data for offline practice |
| `requirements.txt` | Lists the extra package needed for the interface |
| `.gitignore` | Excludes generated databases, logs, and Python cache files |

The program creates `weather.db` for real forecasts and `demo_weather.db` for practice data. The pipeline also records messages in `pipeline.log`. These generated files are not included in the repository.

## How the data flows

1. Python requests forecast data from Open-Meteo.
2. The JSON response is checked for valid dates and numeric temperatures.
3. Valid records are saved to SQLite.
4. A date acts as the primary key, so running the program again updates that date's forecast.
5. The terminal version uses SQL to find the warmest stored day. The interface highlights the warmest day in the newly fetched forecast.

Older dates remain in the database. The project does not keep previous versions of a forecast.

## Scope

This is a beginner learning project. It runs locally and does not include API authentication, Snowflake, or automatic scheduling.

## Data source

Weather forecasts are provided by [Open-Meteo](https://open-meteo.com/).

- [API documentation](https://open-meteo.com/en/docs)
- [Data license and attribution](https://open-meteo.com/en/licence)

The values in `sample.json` are invented for practice.
