import streamlit as st

st.set_page_config(
    page_title="My Portfolio",
    page_icon="📊",
    layout="wide"
)

st.title("My Data Science Portfolio")
st.write("Welcome to my portfolio!")

st.subheader("My Projects")
st.page_link(
    "pages/1_Bio.py",
    label="Bio"
)


st.subheader("EDA Gallery")
st.page_link(
    "pages/2_Charts_Gallery.py",
    label="EDA"
)

st.subheader("Interactive Dashboard")
st.page_link(
    "pages/3_Dashboard.py",
    label="Dashboard"
)

st.subheader("Future Work")
st.page_link(
    "pages/4_Future.py",
    label="Future"
)

st.page_link(
    "pages/5_CO_Air_Quality_Dashboard.py",
    label="Colorado Air Quality Dashboard"
)
