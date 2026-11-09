import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Colorado Air Quality Dashborad",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("data/colorado_air_quality.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# 3. SIDEBAR
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


# 4. KPI ROW
st.header("Colorado Air Quality Dashboard")

k1, k2, k3 = st.columns(3)

k1.metric("Average AQI", f"{filtered['aqi'].mean():.1f}")
k2.metric("Maximum AQI", int(filtered['aqi'].max())
k3.metric("Average Ozone", f"{filtered['ozone_ppb'].mean():.1f} ppb")


# 5. MAIN CHARTS
st.subheader("AQI Trend Over Time")
aqi_trend = (filtered.groupby("date")["aqi"].mean().reset_index())

line_chart = alt.Chart(aqi_trend.mark_line().encode(
    x="date:T",
    y="aqi:Q",
    tooltip=["date:T", "aqi:Q"]
).properties(height=350)

st.altair_chart(line_chart, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Ozone vs. Temperature")

    ozone_chart = alt.Chart(filtered).mark_circle().encode(
        x="temp_f:Q",
        y="ozone_ppb:Q",
        tooltip=["city", "temp_f", "ozone_ppb"]
    )
    st.altair_chart(ozone_chart, use_container_width=True)

with right:
    st.subheader("Wildfire Smoke Impact")

    smoke_data = (
        filtered.groupby("wildfire_smoke")["aqi"]
        .mean()
        .reset_index()
    )

    smoke_chart = alt.Chart(smoke_data).mark_bar().encode(
        x="wildfire_smoke:N",
        y="aqi:Q",
        tooltip=["wildfire_smoke", "aqi"]
    )

    st.altair_chart(smoke_chart, use_container_width=True)

# 6. TABS
tab_heat, tab_data = st.tabs(["🔥 Heatmap", "📄 Raw data"])

with tab_heat:
    heat_df = filtered.groupby(
        ["region", "product"], as_index=False
    )["sales"].sum()

    heat = (
        alt.Chart(heat_df)
        .mark_rect()
        .encode(
            x=alt.X("product:N", title="Product"),
            y=alt.Y("region:N", title="Region"),
            color=alt.Color(
                "sales:Q",
                scale=alt.Scale(scheme=theme)
            ),
            tooltip=["region", "product", "sales"]
        )
        .properties(height=250)
    )

    st.altair_chart(heat, width="stretch")

with tab_data:
    st.dataframe(filtered, hide_index=True, width="stretch")

# 7. EXPANDER
with st.expander("About this dashboard"):
    st.write(
        "Synthetic data for teaching. Change the sidebar filters "
        "and watch every chart rerun automatically."
    )
