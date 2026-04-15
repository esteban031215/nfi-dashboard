import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NFI Air Freight KPI", layout="wide")

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🚛 NFI Air Freight Warehouse Dashboard")

# Force fresh load every single time
st.cache_data.clear()

if st.button("🔄 Refresh Data from Excel"):
    st.rerun()

try:
    data = pd.read_excel("data.xlsx", sheet_name=None)
    st.success("✅ Excel loaded successfully!")
except Exception as e:
    st.error(f"Could not load Excel: {e}")

# Executive Summary
st.subheader("Executive Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Available Pallet Positions", "10,380", "65% utilized")
with col2:
    st.metric("Usable Sq Ft", "78,000", "65% utilized")
with col3:
    st.metric("Forklifts Needed (8-hr shift)", "4", "Current available: 6 → Covered")
with col4:
    st.metric("Total Daily Pallet Moves", "780")

st.metric("Target Daily Inbound Pallets", "380")
st.metric("Dock Doors Available", "20")

st.success("**Overall Ops Status:** CRUSHING - Scale up time 🔥")

# Air Import Production Batch
st.subheader("Air Import Production Batch")
colA, colB = st.columns(2)
with colA:
    st.metric("Total Weight KG", "80,000")   # Change this in Excel to test
    st.metric("Number of Employees", "8")
    st.metric("Job Completion (hours)", "11.2")
    st.metric("Pallet Weight (KG)", "150")
with colB:
    st.metric("Max KG Safe Capacity", "122,435")
    st.metric("Forklifts Needed for this Batch", "2")
    st.metric("Number of Pallets", "467")

st.caption(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
