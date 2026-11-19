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
df["Result"] = df["Win"].map({
    0: "Loss",
    0.5: "Tie",
    1: "Win"
})

# CHART 1
st.header("1. Pressures vs. Points Allowed")

fig = px.scatter(
    df,
    x="Pressures",
    y="opp Points",
    color="Result",
    color_discrete_map={
        "Win": "#0072B2",
        "Loss": "#D55E00",
        "Tie": "#000000"
    },
    hover_data=["Team", "Date", "Sacks", "Takeaways"],
    trendline="ols",
    trendline_scope="overall",
    title="Defensive Pressures vs. Points Allowed",
    labels={
        "Pressures": "Pressures",
        "opp Points": "Points Allowed",
        "Win": "Won Game"
    }
)

st.plotly_chart(fig, use_container_width=True)




df["Pressure Rate"] = df["Pressures"] / df["Defensive Plays"]

df["Pressure Rate Group"] = pd.cut(
    df["Pressure Rate"],
    bins=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 1],
    labels=["0–5%", "5–10%", "10–15%", "15–20%", "20-25%", "25-30%", "30-35%", "35%+"]
)

pressure_summary = df.groupby("Pressure Rate Category").agg(
    Win_Percentage=("Win", "mean"),
    n=("Win", "size")
).reset_index()

win_rates["Win"] *= 100

fig = px.bar(
    pressure_summary,
    x="Pressure Rate Group",
    y="Win_Percentage",
    text = pressure_summary["n"].apply(lambda n: f"n={n}"),
    title="Win Percentage by Defensive Pressure Rate",
    labels={
        "Pressure Rate Group": "Pressures per Opponent Play",
        "Win": "Win Percentage (%)"
    },
    text_auto=".1f"
)

st.plotly_chart(fig, use_container_width=True)
