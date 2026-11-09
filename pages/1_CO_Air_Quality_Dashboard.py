import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Colorado Air Quality Dashborad",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/colorado_air_quality.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ----------------------------------
# SIDEBAR
# ----------------------------------
with st.sidebar:
    st.title("Colorado Air Quality")

    city_choice = st.multiselect(
        "City",
        options=sorted(df["city"].unique()),
        default=sorted(df["city"].unique())
    )

    month_range = st.slider(
        "Month(s)",
        min_value=1,
        max_value=12,
        value=(1, 12)
    )

    smoke_choice = st.selectbox(
        "Wildfire Smoke",
        ["All", "Yes", "No"]
    )

    category_choice = st.multiselect(
        "AQI Category",
        options=sorted(df["aqi_category"].unique()),
        default=sorted(df["aqi_category"].unique())
    )


mask = (df["city"].isin(city_choice)
        & df["date"].dt.month.between(month_range[0], month_range[1]
    )
        & df["aqi_category"].isin(category_choice)
    )

if smoke_choice != "All":
    mask = mask & (df["wildfire_smoke"] == smoke_choice)

filtered = df[mask]

if filtered.empty:
    st.warning("No data matches these filters.")
    st.stop


# ----------------------------------
# KPI ROW
# ----------------------------------
st.header("Colorado Air Quality Dashboard")

k1, k2, k3 = st.columns(3)

k1.metric("Average AQI", f"{filtered['aqi'].mean():.1f}")
k2.metric("Maximum AQI", int(filtered['aqi'].max()))
k3.metric("Average Ozone", f"{filtered['ozone_ppb'].mean():.1f} ppb")


# ----------------------------------
# MAIN CHARTS
# ----------------------------------
st.subheader("AQI Trend Over Time")
aqi_trend = (filtered.groupby("date")["aqi"].mean().reset_index())

line_chart = alt.Chart(aqi_trend).mark_line().encode(
    x="date:T",
    y="aqi:Q",
    tooltip=["date:T", "aqi:Q"]
).properties(height=350)

st.altair_chart(line_chart, use_container_width=True)

left, middle, right = st.columns(3)

# OZONE VS TEMPERATURE
with left:
    st.subheader("Ozone vs. Temperature")

    ozone_data = filtered.dropna(
        subset=["temp_f", "ozone_ppb"]
    )

    points = alt.Chart(ozone_data).mark_circle(
        size=20,
        opacity=0.4
    ).encode(
        x=alt.X("temp_f:Q", title="Temperature (F)"),
        y=alt.Y("ozone_ppb:Q", title="Ozone (ppb)"),
        tooltip=["city", "temp_f", "ozone_ppb"]
    )

    trendline = (
        alt.Chart(ozone_data)
        .transform_regression("temp_f", "ozone_ppb")
        .mark_line(color="red", size=2)
        .encode(
            x="temp_f:Q",
            y="ozone_ppb:Q"
        )
    )

    ozone_chart = points + trendline

    st.altair_chart(ozone_chart, use_container_width=True)

# WILDFIRE SMOKE BOXPLOT

with middle:
    st.subheader("Wildfire Smoke Impact")

    smoke_chart = alt.Chart(filtered).mark_boxplot().encode(
        x=alt.X("wildfire_smoke:N", title="Wildfire Smoke"),
        y=alt.Y("aqi:Q", title="AQI"),
        color=alt.Color("wildfire_smoke:N", legend=None)
    ).properties(height=300)

    st.altair_chart(smoke_chart, use_container_width=True)

# AVERAGE AQI BY CITY
with right:
    st.subheader("Average AQI by City")

    city_avg = (
        filtered.groupby("city")["aqi"]
        .mean()
        .reset_index()
        .rename(columns={"aqi": "avg_aqi"})
    )

    city_chart = alt.Chart(city_avg).mark_bar().encode(
        x=alt.X("city:N", title="City", sort="-y"),
        y=alt.Y("avg_aqi:Q", title="Average AQI"),
        color=alt.Color(
            "avg_aqi:Q",
            scale=alt.Scale(scheme="greens"),
            legend=None
        ),
        tooltip=["city", "avg_aqi"]
    ).properties(height=300)

    st.altair_chart(city_chart, use_container_width=True)

# ----------------------------------
# KEY INSIGHTS
# ----------------------------------
st.divider()
st.subheader("Key Insights")

# Highest average AQI city
city_averages = filtered.groupby("city")["aqi"].mean()
highest_city = city_averages.idxmax()
highest_city_aqi = city_averages.max()

# Wildfire smoke comparison
smoke_avg = filtered.groupby("wildfire_smoke")["aqi"].mean()

smoke_yes = smoke_avg.get("yes", float("nan"))
smoke_no = smoke_avg.get("no", float("nan"))

# Month with highest average AQI
worst_month = (
    filtered.groupby("month")["aqi"]
    .mean()
    .idxmax()
)

# Temperature and ozone correlation
correlation = filtered["temp_f"].corr(
    filtered["ozone_ppb"]
)

st.markdown(f"""
- **Highest AQI by city:** {highest_city} has the highest
  average AQI at **{highest_city_aqi:.1f}**.

- **Wildfire smoke impact:** Average AQI is
  **{smoke_yes:.1f}** on smoke days compared to
  **{smoke_no:.1f}** on non-smoke days.

- **Seasonal pattern:** {worst_month} has the highest
  average AQI.

- **Ozone and temperature:** The correlation is
  **{correlation:.2f}**.
""")
