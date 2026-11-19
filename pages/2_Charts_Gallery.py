import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="EDA Gallery",
    page_icon="📊",
    layout="wide"
)

st.title("NFL Defensive Analytics")
st.caption("Exploratory Data Analysis | 2024–2026")
st.write("""
This gallery explores NFL defensive performance across regular-season
games, examining how pressures, sacks, takeaways, and defensive efficiency
relate to game outcomes.
""")

# Load dataset
df = pd.read_csv("data/2024-2026wk10.csv")

# CHART 1
st.header("1. Pressures vs. Points Allowed")

fig = px.scatter(
    df,
    x="Pressures",
    y="opp Points",
    color="Win",
    color_discrete_map={
        1: "#0072B2",
        0: "#D55E00"
        0.5: #000000
    },
    hover_data=["Team", "Date", "Sacks", "Takeaways"],
    trendline="ols",
    title="Defensive Pressures vs. Points Allowed",
    labels={
        "Pressures": "Pressures",
        "oPts": "Points Allowed",
        "Win": "Won Game"
    }
)

st.plotly_chart(fig, use_container_width=True)
