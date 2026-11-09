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
st.caption(
    "Line chart showing AQI remaining mostly steady "
    "throughout the year, with noticeable spikes during the "
    "summer months associated with increased wildfire activity."
)

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
    st.caption("Scatterplot showing a generally positive relationship between temperature and ozone concentration. "
               "Higher temperatures tend to correspond with higher ozone levels.")

# WILDFIRE SMOKE BOXPLOT
with middle:
    st.subheader("Wildfire Smoke Impact")
    smoke_chart = alt.Chart(filtered).mark_boxplot().encode(
        x=alt.X("wildfire_smoke:N", title="Wildfire Smoke"),
        y=alt.Y("aqi:Q", title="AQI"),
        color=alt.Color("wildfire_smoke:N", legend=None)
    ).properties(height=300)

    st.altair_chart(smoke_chart, use_container_width=True)
    st.caption("AQI Boxplots for wildfire smoke and non-smoke days are completely separated."
                "The median AQI is 146 on smoke days compared to 39 on non-smoke days, indicating a substantial difference in air quality.")

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
            scale=alt.Scale(scheme="reds"),
            legend=None
        ),
        tooltip=["city", "avg_aqi"]
    ).properties(height=300)

    st.altair_chart(city_chart, use_container_width=True)
    st.caption("Bar Chart showing the average AQI by city within the selected filters."
               "Color coded with darker red indicating higher AQI levels and lighter red indicating lower AQI levels."
               "When viewing the full year, Denver has the highest average "
                "AQI at 52, followed by Grand Junction at 46 and Pueblo at 43. "
                "Fort Collins, Colorado Springs, and Boulder each average 41.")

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

# Monthly AQI
monthly_aqi = filtered.groupby("month")["aqi"].mean()
worst_month = monthly_aqi.idxmax()
worst_month_aqi = monthly_aqi.max()

# Temperature and ozone correlation
correlation = filtered["temp_f"].corr(
    filtered["ozone_ppb"]
)

st.markdown(f"""
- **Highest AQI by city:** {highest_city} has the highest
  average AQI at **{highest_city_aqi:.1f}**.


- **Seasonal pattern:** {worst_month} has the highest
  average AQI at **{worst_month_aqi:.1f}**.

- **Ozone and temperature:** The correlation is
  **{correlation:.2f}**.
""")
