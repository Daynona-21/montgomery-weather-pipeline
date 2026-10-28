import sqlite3
from urllib.error import URLError

import streamlit as st
from weather import FOLDER, get_data, clean_data, save_and_report

st.set_page_config(page_title="Montgomery Weather", page_icon="🌤️")

st.title("🌤️ Montgomery Weather")
st.write("Daily weather forecasts for Montgomery, Alabama")

if st.button("Fetch latest forecast"):
    try:
        with st.spinner("Getting the forecast..."):
            data = get_data(demo=False)
            rows = clean_data(data)
            save_and_report(rows, FOLDER / "weather.db")

        st.success("Forecast saved to the database!")

        warmest = max(rows, key=lambda row: row[1])
        st.metric("Warmest forecast day", f"{warmest[1]:.1f} °C")
        st.write(f"Date: {warmest[0]}")

        st.dataframe(
            [{"Date": day, "High (°C)": temp} for day, temp in rows],
            hide_index=True,
        )

    except (URLError, OSError, ValueError, KeyError, TypeError, sqlite3.Error):
        st.error("Could not load the forecast. Check your connection and try again.")

st.caption("Forecast data from Open-Meteo | Python + SQLite")