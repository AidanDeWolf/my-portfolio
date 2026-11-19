import streamlit as st

st.set_page_config(
    page_title="Future Work",
    page_icon="🚀",
    layout="wide"
)

st.title("Future Work")
st.caption("Potential improvements and project reflection")

st.header("Planned Improvements")

st.markdown("""
1. **Add Predictive Modeling:** Build a machine learning model to estimate the probability of winning based on defensive statistics.

2. **Expand the Dataset:** Include additional seasons and offensive statistics to provide more context for defensive performance.

3. **Add Opponent-Adjusted Metrics:** Account for opponent offensive strength when evaluating defensive performance.

4. **Improve Interactivity:** Add filters for season, week, and opponent, along with additional comparisons between teams.

5. **Conduct an Accessibility Audit:** Test color contrast, colorblind-friendly visualizations, chart labels, and navigation.
""")

st.divider()

st.header("Reflection: Paper Prototype vs. Final Build")

st.markdown("""
- I didn't think this was connected to the 4.3 Lab, so no changes were made that weren't already made when I submitted Lab 4.3
""")
