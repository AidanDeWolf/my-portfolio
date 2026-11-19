
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

st.markdown("""
**Question:** How are defensive pressures related to points allowed and winning games?

**How to read this chart:**
- Each point represents one team-game observation.
- The X-axis shows pressures generated.
- The Y-axis shows points allowed.
- Colors distinguish wins, losses, and ties; the trendline shows the overall relationship.

**Observations:**
- Pressures show a strong relationship with winning.
- Pressures also show a strong relationship with limiting points allowed.
""")

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

st.markdown("""
**Question:** How does the rate of defensive pressures relate to winning games?

**How to read this chart:**
- The X-axis shows pressure rate categories.
- The Y-axis shows the percentage of games won.
- Higher bars indicate higher win percentages.

**Observations:**
- Compare win percentages across pressure-rate categories.
- Look for whether win percentage generally increases as pressure rate increases.
- Consider the sample size in each category when comparing results.
""")

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

st.markdown("""
**Question:** How do sacks and takeaways compare in their relationship with winning games?

**How to read this chart:**
- The X-axis shows the number of sacks or takeaways.
- The Y-axis shows the percentage of games won.
- Separate lines represent sacks and takeaways.
- Hover over points to see the number of observations.

**Observations:**
- At two sacks, the win percentage is 68%, compared with 48% for two takeaways.
- At three sacks, the win percentage is 82%, compared with 58% for three takeaways.
- Sacks show a higher win percentage than takeaways at these two levels.
""")

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

st.markdown("""
**Question:** Which defensive statistics have the strongest linear relationships with winning?

**How to read this chart:**
- Each cell represents the correlation between two variables.
- Values range from -1 to +1.
- Positive values indicate variables tend to increase together.
- Negative values indicate one variable tends to decrease as the other increases.

**Observations:**
- Takeaways have the strongest correlation with winning (r = 0.36).
- Defensive yards allowed per play have the second-strongest relationship with winning.
- Pressures (r = 0.30) and sacks (r = 0.29) have relatively similar correlations.
- Overall, the correlations are weaker than expected, suggesting no single defensive statistic has a particularly strong linear relationship with winning.
""")

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

st.markdown("""
**Question:** How does defensive efficiency change as the number of opponent offensive plays increases?

**How to read this chart:**
- Each point represents one team-game observation.
- The X-axis shows opponent offensive plays faced.
- The Y-axis shows yards allowed per play; lower values indicate better efficiency.
- The regression line shows the overall trend.

**Observations:**
- There is virtually no linear relationship between opponent plays faced and defensive efficiency.
- The regression model has an R² of 0.0037.
- Opponent plays faced explains approximately 0.37% of the variation in yards allowed per play.
""")
