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

# PRESSURES
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
    bins=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 1],
    labels=["0–5%", "5–10%", "10–15%", "15–20%", "20-25%", "25%+"]
)

pressure_summary = df.groupby("Pressure Rate Group").agg(
    Win_Percentage=("Win", "mean"),
    n=("Win", "size")
).reset_index()

pressure_summary["Win_Percentage"] *= 100

fig = px.bar(
    pressure_summary,
    x="Pressure Rate Group",
    y="Win_Percentage",
    title="Win Percentage by Defensive Pressure Rate",
    labels={
        "Pressure Rate Group": "Pressures per Opponent Play",
        "Win": "Win Percentage (%)"
    },
     text_auto=".1f"
)


# SACKS VS TAKEAWAYS
st.header("2. Sacks vs. Takeaways")

# Create categories
df["Sack Group"] = pd.cut(
    df["Sacks"],
    bins=[-1, 0, 1, 2, 3, float("inf")],
    labels=["0", "1", "2", "3", "4+"]
)

df["Takeaway Group"] = pd.cut(
    df["Takeaways"],
    bins=[-1, 0, 1, 2, 3, float("inf")],
    labels=["0", "1", "2", "3", "4+"]
)

# Calculate win percentage and sample size
sack_takeaway_summary = df.groupby(
    ["Sack Group", "Takeaway Group"], observed=False
).agg(
    Win_Percentage=("Win", "mean"),
    n=("Win", "size")
).reset_index()

sack_takeaway_summary["Win_Percentage"] *= 100

# Create grouped bar chart
fig = px.bar(
    sack_takeaway_summary,
    x="Sack Group",
    y="Win_Percentage",
    color="Takeaway Group",
    barmode="group",
    title="Win Percentage by Sacks and Takeaways",
    labels={
        "Sack Group": "Sacks",
        "Takeaway Group": "Takeaways",
        "Win_Percentage": "Win Percentage (%)"
    },
    hover_data=["n"],
    text_auto=".1f"
)


st.plotly_chart(fig, use_container_width=True)
