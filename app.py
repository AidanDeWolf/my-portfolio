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
    "pages/1_Sales_Dashboard.py",
    label="Coffee Shop Sales Dashboard"
)
