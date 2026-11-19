
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="NFL Defense Dashboard",
    page_icon="🏈",
    layout="wide"
)

st.title("NFL Defensive Performance Dashboard")
st.caption("Explore how defensive performance relates to game outcomes | 2024–2026")

# LOAD DATA
df = pd.read_csv("data/2024-2026wk10.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Pressure Rate"] = (
    df["Pressures"] / df["Defensive Plays"].replace(0, pd.NA)
)

# SIDEBAR FILTERS
st.sidebar.header("Dashboard Filters")

# Team selector: all teams selected initially
teams = sorted(df["Team"].dropna().unique())

selected_teams = st.sidebar.multiselect(
    "Select Teams",
    options=teams,
    default=teams
)

# Date range
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Game Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Helper function for numeric sliders
def numeric_filter(label, column, step=1, format=None):
    minimum = float(df[column].min())
    maximum = float(df[column].max())

    if minimum == maximum:
        return minimum, maximum

    return st.sidebar.slider(
        label,
        min_value=minimum,
        max_value=maximum,
        value=(minimum, maximum),
        step=float(step),
        format=format
    )

# Defensive statistic sliders
st.sidebar.subheader("Defensive Statistics")

pressures = numeric_filter("Pressures", "Pressures")
pressure_rate = numeric_filter(
    "Pressure Rate (%)",
    "Pressure Rate",
    step=0.01,
    format="%.2f"
)
interceptions = numeric_filter("Interceptions", "Interceptions")
fumbles = numeric_filter("Fumble Recoveries", "Fumbles Recovered")
takeaways = numeric_filter("Takeaways", "Takeaways")
sacks = numeric_filter("Sacks", "Sacks")
yards_per_play = numeric_filter(
    "Yards Allowed per Play",
    "Def. Yards/Play",
    step=0.1,
    format="%.1f"
)
plays = numeric_filter("Defensive Plays", "Defensive Plays")

# FILTER DATA
filtered_df = df[
    (df["Team"].isin(selected_teams)) &
    (df["Date"].dt.date >= date_range[0]) &
    (df["Date"].dt.date <= date_range[1]) &
    (df["Pressures"].between(*pressures)) &
    (df["Pressure Rate"].between(*pressure_rate)) &
    (df["Interceptions"].between(*interceptions)) &
    (df["Fumbles Recovered"].between(*fumbles)) &
    (df["Takeaways"].between(*takeaways)) &
    (df["Sacks"].between(*sacks)) &
    (df["Def. Yards/Play"].between(*yards_per_play)) &
    (df["Defensive Plays"].between(*plays))
].copy()

st.divider()

# RESULTS
st.subheader("Filtered Game Results")

if filtered_df.empty:
    st.warning("No games match your selected filters. Try widening your ranges.")

else:
    # KPIs
    total_games = len(filtered_df)
    win_percentage = filtered_df["Win"].mean() * 100
    avg_points_allowed = filtered_df["opp Points"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Matching Team-Games", f"{total_games:,}")
    col2.metric("Win Percentage", f"{win_percentage:.1f}%")
    col3.metric("Average Points Allowed", f"{avg_points_allowed:.1f}")

    # OUTCOME PERCENTAGES
    wins = (filtered_df["Win"] == 1).mean() * 100
    ties = (filtered_df["Win"] == 0.5).mean() * 100
    losses = (filtered_df["Win"] == 0).mean() * 100

    outcomes = pd.DataFrame({
        "Outcome": ["Wins", "Ties", "Losses"],
        "Percentage": [wins, ties, losses],
        "Games": [
            (filtered_df["Win"] == 1).sum(),
            (filtered_df["Win"] == 0.5).sum(),
            (filtered_df["Win"] == 0).sum()
        ]
    })

    fig = px.bar(
        outcomes,
        x="Percentage",
        y=["Selected Games"] * 3,
        color="Outcome",
        orientation="h",
        color_discrete_map={
            "Wins": "#269B70",
            "Losses": "#D55E00",
            "Ties": "#777777"
        },
        text=outcomes.apply(
            lambda row: f"{row['Outcome']}: {row['Percentage']:.1f}%",
            axis=1
        ),
        hover_data=["Games"],
        title="Win / Loss / Tie Distribution",
        labels={
            "Percentage": "Percentage of Team-Games",
            "y": ""
        }
    )

    fig.update_layout(
        barmode="stack",
        xaxis=dict(range=[0, 100]),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Win percentage counts ties as half a win. "
        "The stacked bar displays wins, losses, and ties separately."
    )

    # WIN PERCENTAGE BY TEAM
    st.subheader("Win Percentage by Team")

    team_summary = filtered_df.groupby("Team").agg(
        Win_Percentage=("Win", "mean"),
        Games=("Win", "size")
    ).reset_index()

    team_summary["Win_Percentage"] *= 100

    team_summary = team_summary.sort_values(
        "Win_Percentage",
        ascending=True
    )

    fig = px.bar(
        team_summary,
        x="Win_Percentage",
        y="Team",
        orientation="h",
        text=team_summary["Win_Percentage"].apply(
            lambda x: f"{x:.1f}%"
        ),
        hover_data=["Games"],
        title="Historical Win Percentage by Team",
        labels={
            "Win_Percentage": "Win Percentage (%)",
            "Team": "NFL Team"
        }
    )

    fig.update_layout(
        xaxis=dict(range=[0, 100])
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)


    # Games by team and result
    team_results = (
        filtered_df.groupby(["Team", "Result"])
        .size()
        .reset_index(name="Games")
    )
    
    fig = px.bar(
        team_results,
        x="Games",
        y="Team",
        color="Result",
        orientation="h",
        color_discrete_map={
            "Win": "#269B70",
            "Loss": "#D55E00",
            "Tie": "#777777"
        },
        title="Games by Team and Result",
        labels={"Games": "Number of Games", "Team": "Team"}
    )
    
    fig.update_layout(
        barmode="stack",
        yaxis={"categoryorder": "total ascending"}
    )
    
    st.plotly_chart(fig, width="stretch")

    # NARRATIVE
    st.subheader("Insights")

    best_team = team_summary.iloc[-1]
    worst_team = team_summary.iloc[0]

    st.markdown(f"""
    - **Sample size:** {total_games:,} team-games match the selected filters.
    - **Win rate:** The filtered games have a {win_percentage:.1f}% win rate, counting ties as half a win.
    - **Points allowed:** Teams allowed an average of {avg_points_allowed:.1f} points per game.
    - **Highest win percentage:** {best_team['Team']} leads the filtered teams at {best_team['Win_Percentage']:.1f}% ({int(best_team['Games'])} games).
    - **Lowest win percentage:** {worst_team['Team']} has the lowest filtered win percentage at {worst_team['Win_Percentage']:.1f}% ({int(worst_team['Games'])} games).
    """)


# DATA SOURCE AND REFRESH
st.divider()

st.markdown(
    "[Data Source: Stathead Team Game Stats Finder](https://www.sports-reference.com/stathead/football/team-game-finder.cgi)"
)

st.caption(
    f"Dashboard generated: {date.today().strftime('%B %d, %Y')} | "
    "Dataset: 2024–2026 Week 10"
)
