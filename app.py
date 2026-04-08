
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NFI Air Freight KPI", layout="wide")

# Clean look
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🚛 NFI Air Freight Warehouse Dashboard")

if st.button("🔄 Refresh Data from Excel"):
    st.rerun()

# ===================== LIVE DATA FROM EXCEL =====================
usable_sqft = 78000
pallet_positions = 4980
forklifts = 4
inbound = 400
total_moves = 780
total_weight_kg = 30000
num_employees = 8
job_completion = 6.0
pallet_weight_kg = 150
number_of_pallets = 467
dock_doors = 20

try:
    data = pd.read_excel("data.xlsx", sheet_name=None)
    st.success("✅ Excel loaded successfully!")

    def safe_int(val, default=0):
        try:
            if pd.isna(val) or val == "" or val is None:
                return default
            return int(round(float(val)))
        except:
            return default

    def safe_float(val, default=6.0):
        try:
            if pd.isna(val) or val == "" or val is None:
                return default
            return round(float(val), 1)
        except:
            return default

    # Virtual Warehouse
    if "Virtual Warehouse" in data:
        vw = data["Virtual Warehouse"]
        usable_sqft = safe_int(vw.iloc[0, 3])
        pallet_positions = safe_int(vw.iloc[9, 1])

    # CFS CES
    if "CFS CES" in data:
        cfs = data["CFS CES"]
        total_weight_kg = safe_int(cfs.iloc[0, 1])
        num_employees   = safe_int(cfs.iloc[2, 1])
        job_completion  = safe_float(cfs.iloc[11, 2])
        pallet_weight_kg = safe_int(cfs.iloc[16, 1])
        number_of_pallets = safe_int(cfs.iloc[17, 1])

    # KPI Dashboard
    if "KPI Dashboard" in data:
        kd = data["KPI Dashboard"]
        forklifts = safe_int(kd.iloc[7, 1])
        inbound = safe_int(kd.iloc[5, 1])
        total_moves = safe_int(kd.iloc[7, 1])

    # Outbond loading - Dock Doors
    if "Outbond loading" in data:
        outbound = data["Outbond loading"]
        dock_doors = safe_int(outbound.iloc[6, 1])

except Exception as e:
    st.error(f"Could not load Excel: {e}")

# ===================== EXECUTIVE SUMMARY =====================
st.subheader("Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Available Pallet Positions", f"{pallet_positions:,}", "65% utilized")

with col2:
    st.metric("Usable Sq Ft", f"{usable_sqft:,}", "65% utilized")

with col3:
    st.metric("Forklifts Needed (8-hr shift)", forklifts, "Current available: 6 → Covered")

with col4:
    st.metric("Total Daily Pallet Moves", total_moves)

st.metric("Target Daily Inbound Pallets", inbound)
st.metric("Dock Doors Available", dock_doors)

st.success("**Overall Ops Status:** CRUSHING - Scale up time 🔥")

# ===================== AIR IMPORT PRODUCTION BATCH =====================
st.subheader("Air Import Production Batch")

colA, colB = st.columns(2)

with colA:
    st.metric("Total Weight KG", f"{total_weight_kg:,}")
    st.metric("Number of Employees", num_employees)
    st.metric("Job Completion (hours)", job_completion)
    st.metric("Pallet Weight (KG)", f"{pallet_weight_kg:,}")

with colB:
    st.metric("Max KG Safe Capacity", "122,435")
    st.metric("Forklifts Needed for this Batch", "2")
    st.metric("Number of Pallets", f"{number_of_pallets:,}")   # Moved to right side

st.caption(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
st.caption("Data from NFI Air Freight Model v1.0")

