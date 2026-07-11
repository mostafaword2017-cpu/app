import streamlit as st
import numpy as np

st.set_page_config(page_title="Test", layout="centered")

st.title("✅ ElectroCalc M&F - Test")

st.write("If you see this, Streamlit is working!")

if st.button("Click me"):
    st.success("Button works!")
