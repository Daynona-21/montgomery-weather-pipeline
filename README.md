# Montgomery Weather Pipeline

A small beginner project using Python, a REST API, JSON, and SQLite SQL.
It fetches seven daily maximum-temperature forecasts for Montgomery, Alabama,
checks the records, stores them, and prints the warmest stored day.
These are forecasts, not measured weather observations.

## Run it

You need Python 3.9 or later. No extra packages or API keys are needed.
Unzip the project, open its folder in VS Code, and open Terminal > New Terminal.

Start with invented practice data (no internet needed):

```bash
python weather.py --demo
```

On Windows, use `py` instead of `python` if necessary. On macOS/Linux,
you may need `python3`.

Expected practice results:

```text
2027-06-01: 28.5 C
2027-06-02: 30.0 C
2027-06-03: 29.2 C

Warmest stored day: 2027-06-02 (30.0 C)
```

Fetch actual forecasts with an internet connection:

```bash
python weather.py
```

Practice uses `demo_weather.db`; the API run uses `weather.db`.
Messages and errors are written to `pipeline.log`.
If the network request fails, the script exits with an error and suggests demo
mode; it never silently presents invented data as a real forecast.

## Read the code in this order

1. `get_data`: downloads JSON, or opens the practice file.
2. `clean_data`: pairs dates with temperatures, checks dates and numbers,
   and skips invalid records. Unequal list lengths stop the run.
3. `save_and_report`: creates a table, saves records, and runs SQL queries.
4. `main`: connects those steps and handles errors.

This is a small ETL pipeline: extract data, transform/check it, then load it.
SQLite is a database stored in a local file; SQL is the language used to query it.
The table has two columns: `day` and `max_temp_c` (degrees Celsius).

## Understand the SQL

`CREATE TABLE IF NOT EXISTS` creates the table on the first run.
`PRIMARY KEY` makes each date unique. The `ON CONFLICT` clause updates an
existing date instead of inserting a duplicate. `excluded.max_temp_c` means
the new temperature we tried to insert. `?` placeholders pass values safely.

```sql
SELECT day, max_temp_c
FROM weather
ORDER BY max_temp_c DESC, day ASC
LIMIT 1;
```

This sorts from hottest to coolest, breaks ties by the earliest date, and
returns one row. The query covers all stored dates. Older dates remain in the
database; rerunning updates dates that appear in the new response. The project
does not keep a history of earlier forecast versions.

## Three exercises before adding it to your resume

1. Run demo mode twice. There should still be three rows printed.
2. Change `30.0` to `31.5` in sample.json and rerun. See the saved value update.
3. Change a temperature to `null`. Rerun and inspect pipeline.log for the warning.
   An existing saved record stays in the database if its new input is invalid.

Explain aloud: Where does the data come from? Why use a primary key?
What happens when the API fails? What does the SQL query return?

## Git practice

Once Git is installed, run these from this project folder:

```bash
git init
git add weather.py sample.json README.md .gitignore
git commit -m "Add beginner weather data pipeline"
```

Git may ask you to configure your name and email before the first commit.
The ignore file excludes generated databases and logs. Publishing to GitHub
is a separate step; this download does not create a GitHub repository.

## Scope and source

This version demonstrates Python, JSON, a REST GET request, basic validation,
SQL, duplicate prevention, and logging. It does not implement Snowflake,
API authentication, automatic scheduling, or a web interface.
It was created with AI assistance as a learning starter. Run, understand,
and modify it before describing your contribution in an application.

Weather data: [Open-Meteo](https://open-meteo.com/).
API reference: https://open-meteo.com/en/docs
Data attribution/license: https://open-meteo.com/en/licence
The included sample.json values are invented for practice, not API data.

