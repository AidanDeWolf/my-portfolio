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

st.plotly_chart(fig, width='stretch')




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
st.plotly_chart(fig, width='stretch')


# SACKS VS TAKEAWAYS
st.header("2. Sacks vs. Takeaways")

# Group sacks
sack_summary = df.groupby("Sacks").agg(
    Win_Percentage=("Win", "mean"),
    n=("Win", "size")
).reset_index()

sack_summary["Statistic"] = "Sacks"
sack_summary["Value"] = sack_summary["Sacks"]

# Group takeaways
takeaway_summary = df.groupby("Takeaways").agg(
    Win_Percentage=("Win", "mean"),
    n=("Win", "size")
).reset_index()

takeaway_summary["Statistic"] = "Takeaways"
takeaway_summary["Value"] = takeaway_summary["Takeaways"]

# Combine data
comparison = pd.concat([
    sack_summary[["Statistic", "Value", "Win_Percentage", "n"]],
    takeaway_summary[["Statistic", "Value", "Win_Percentage", "n"]]
])

comparison["Win_Percentage"] *= 100

# Create chart
fig = px.line(
    comparison,
    x="Value",
    y="Win_Percentage",
    color="Statistic",
    markers=True,
    hover_data=["n"],
    title="Win Percentage by Sacks vs. Takeaways",
    labels={
        "Value": "Number of Sacks / Takeaways",
        "Win_Percentage": "Win Percentage (%)",
        "Statistic": "Defensive Statistic"
    }
)

st.plotly_chart(fig, width='stretch')

# CORRELATION MATRIX
st.header("3. Defensive Statistics and Winning")

# Calculate correlation matrix
correlation_matrix = df[
    ["Win", "Takeaways", "Sacks", "Pressures", "Def. Yards/Play"]
].corr()

# Create heatmap
fig = px.imshow(
    correlation_matrix,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Correlation Between Defensive Statistics and Winning",
    labels={
        "x": "Statistic",
        "y": "Statistic",
        "color": "Correlation (r)"
    }
)

st.plotly_chart(fig, width='stretch')

# DEFENSIVE EFFICIENCY VS PLAYS FACED
# CHART 4
st.header("4. Defensive Efficiency vs. Plays Faced")

fig = px.scatter(
    df,
    x="Defensive Plays",
    y="Def. Yards/Play",
    hover_data=["Team", "Date", "Sacks", "Takeaways"],
    trendline="ols",
    trendline_scope="overall",
    title="Defensive Efficiency by Opponent Plays Faced",
    labels={
        "Defensive Plays": "Opponent Offensive Plays",
        "Def. Yards/Play": "Yards Allowed per Play"
    }
)

st.plotly_chart(fig, width='stretch')
