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
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
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
st.header("Sales Overview")

monthly = filtered.groupby(
    "month", as_index=False
)["sales"].sum()

last = monthly["sales"].iloc[-1]
prev = monthly["sales"].iloc[-2] if len(monthly) > 1 else last

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total sales", f"{filtered['sales'].sum():,}")
k2.metric("Latest month", f"{last:,}", delta=f"{last - prev:,}")
k3.metric(
    "Top product",
    filtered.groupby("product")["sales"].sum().idxmax()
)
k4.metric("Average Monthly Sales", f"{filtered['sales'].mean():,}")

# 5. MAIN ROW
left, right = st.columns((3, 1), gap="medium")

with left:
    st.subheader("Monthly trend by region")

    trend = filtered.groupby(
        ["month", "region"], as_index=False
    )["sales"].sum()

    line = (
        alt.Chart(trend)
        .mark_line(point=True)
        .encode(
            x=alt.X("month:T", title="Month"),
            y=alt.Y("sales:Q", title="Sales"),
            color=alt.Color(
                "region:N",
                scale=alt.Scale(scheme=theme)
            ),
            tooltip=["month:T", "region:N", "sales:Q"]
        )
    )

    st.altair_chart(line, width="stretch")

with right:
    st.subheader("Top products")

    top = (
        filtered.groupby("product", as_index=False)["sales"].sum()
        .sort_values("sales", ascending=False)
    )

    st.dataframe(
        top,
        hide_index=True,
        width="stretch",
        column_config={
            "product": st.column_config.TextColumn("Product"),
            "sales": st.column_config.ProgressColumn(
                "Sales",
                format="%d",
                min_value=0,
                max_value=int(top["sales"].max())
            ),
        },
    )

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
