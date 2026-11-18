
import streamlit as st

st.set_page_config(
    page_title="About Me",
    page_icon="📄",
    layout="wide"
)

st.title("About Me")
st.caption("Data Science | Machine Learning | Data Analytics")

st.divider()

# Professional Summary
st.header("Professional Summary")

st.write("""
I'm a Data Science student at Metropolitan State University of Denver
with an interest in machine learning, statistical analysis, and data
visualization. I enjoy using data to investigate questions, identify
patterns, and communicate meaningful insights.
""")

# Highlights
st.header("Highlights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - Python, R, and SQL
    - Statistical analysis
    - Machine learning
    """)

with col2:
    st.markdown("""
    - Data visualization
    - Predictive modeling
    - Streamlit development
    """)

# Visualization Philosophy
st.header("Visualization Philosophy")

st.write("""
I believe effective data visualization should prioritize clarity,
accuracy, and accessibility. My goal is to make complex information
easier to understand without distorting the underlying data.
""")

# Contact
st.header("Contact")

st.write("Email: aidancdewolf@gmail.com")
