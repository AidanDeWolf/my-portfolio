
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
I'm a Data Science student at Metropolitan State University of Denver with an interest in machine learning,
statistical analysis, and data visualization. Through my coursework and projects, I've gained experience 
using Python, R, and SQL to clean and analyze datasets, develop predictive models, and explore relationships 
between variables. I enjoy approaching real-world questions from a data-driven perspective, using statistical 
methods and visualizations to identify patterns and communicate meaningful findings. My academic projects have
allowed me to work with a variety of techniques, including regression, classification, clustering, and machine
learning algorithms. I'm continuing to develop my technical skills and looking for opportunities to apply data 
science to practical problems.
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

st.write("Email: [aidancdewolf@gmail.com]")
