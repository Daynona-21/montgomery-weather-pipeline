"""A beginner Python + SQL project: Montgomery daily weather forecasts."""

import argparse
import json
import logging
import math
import sqlite3
from datetime import date
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

FOLDER = Path(__file__).resolve().parent
URL = (
    "https://api.open-meteo.com/v1/forecast?latitude=32.3668"
    "&longitude=-86.3000&daily=temperature_2m_max"
    "&temperature_unit=celsius&timezone=America%2FChicago&forecast_days=7"
)


def get_data(demo):
    """Read practice JSON or request real forecast data."""
    if demo:
        return json.loads((FOLDER / "sample.json").read_text())
    with urlopen(URL, timeout=20) as response:
        return json.load(response)


def clean_data(data):
    """Check the response, then turn valid days into database rows."""
    days = data["daily"]["time"]
    temperatures = data["daily"]["temperature_2m_max"]
    if not isinstance(days, list) or not isinstance(temperatures, list):
        raise ValueError("Expected lists of dates and temperatures.")
    if len(days) != len(temperatures):
        raise ValueError("Dates and temperatures have different lengths.")

    rows = []
    for day, temperature in zip(days, temperatures):
        try:
            date.fromisoformat(day)
            if type(temperature) not in (int, float):
                raise ValueError("Missing or nonnumeric temperature")
            if not math.isfinite(temperature):
                raise ValueError("Temperature must be finite")
        except (TypeError, ValueError):
            logging.warning("Skipped invalid record: %s, %s", day, temperature)
            continue
        rows.append((day, temperature))
    if not rows:
        raise ValueError("No valid weather records were found.")
    return rows


def save_and_report(rows, database):
    """Save forecasts and use SQL to find the warmest stored day."""
    with sqlite3.connect(database) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                day TEXT PRIMARY KEY,
                max_temp_c REAL NOT NULL
            )
        """)
        # The primary key keeps one row per day. Reruns update its forecast.
        # Question marks safely pass Python values into the SQL statement.
        connection.executemany("""
            INSERT INTO weather (day, max_temp_c) VALUES (?, ?)
            ON CONFLICT(day) DO UPDATE SET max_temp_c = excluded.max_temp_c
        """, rows)

        records = connection.execute(
            "SELECT day, max_temp_c FROM weather ORDER BY day"
        ).fetchall()
        warmest = connection.execute("""
            SELECT day, max_temp_c FROM weather
            ORDER BY max_temp_c DESC, day ASC LIMIT 1
        """).fetchone()

    print("\nMontgomery, Alabama — stored daily forecasts")
    for day, temperature in records:
        print(f"{day}: {temperature:.1f} C")
    print(f"\nWarmest stored day: {warmest[0]} ({warmest[1]:.1f} C)")
    print(f"Saved or updated {len(rows)} records. Database: {database.name}")
    logging.info("Saved or updated %s records in %s", len(rows), database.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Use invented practice data")
    args = parser.parse_args()
    logging.basicConfig(
        filename=FOLDER / "pipeline.log", level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    # Separate databases keep practice values out of the real forecasts.
    database = FOLDER / ("demo_weather.db" if args.demo else "weather.db")
    print("DEMO: invented practice data" if args.demo else "Fetching Open-Meteo forecasts...")
    try:
        data = get_data(args.demo)
        rows = clean_data(data)
        save_and_report(rows, database)
    except (URLError, OSError, ValueError, KeyError, TypeError, sqlite3.Error) as error:
        logging.error("Pipeline failed: %s", error)
        print(f"Could not finish: {error}")
        print("See pipeline.log. For offline practice, run: python weather.py --demo")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
