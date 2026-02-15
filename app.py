import streamlit as st
import gravity_logic
import pandas as pd
from datetime import datetime
import io
import csv

# --- CLINICAL DATA CATEGORIES ---
BODY_PARTS = [
    "Wrist", "Elbow", "Shoulder", "Ankle", "Knee", "Hip", 
    "Pelvis", "Gut", "Chest", "Heart", "Spine", "Head", 
    "Eyes - Object", "Eye - Object", "Eyes - no object", "Eye - no object"
]

MILESTONES = [
    "Sleeping and Lying Down", "Tummy Time", "Looking At You", "Rolling Over", 
    "Grabbing the Feet", "Independent Sitting", "Coming to Sitting", 
    "Going into All Fours", "Crawling", "Crawling Reach", "Reaching Up", 
    "In and out of Standing", "Standing With Support 1", 
    "Standing With Support 2", "Standing With Support 3"
]

STRUCTURAL_FACTORS = [
    "Midline", "Peripheral Midline", "small stem + vortex", "large stem + vortex", 
    "small butterfly", "large butterfly", "breathing", "balance", 
    "horizon heart structure", "driving heart structure", 
    "front and back heart structure", "bouyancy", "counterbalance", 
    "momentum slow", "momentum normal"
]

st.set_page_config(page_title="Fractal Code Diagnostic", layout="wide")

st.title("Gravity Tax Evaluation Tool")
st.write("Calculate **Gravity Tax** and identify structural bottlenecks for milestone enhancement.")

# --- SIDEBAR: OVERALL TOTALS ---
st.sidebar.header("Step 1: Overarching Totals")
name = st.sidebar.text_input("Child's Name", "Subject A")
rot_total = st.sidebar.number_input("Total Rotation (0-360)", 0.0, 360.0, value=129.1)
struc_total = st.sidebar.number_input("Total Structural (0-360)", 0.0, 360.0, value=134.05)
trans_total = st.sidebar.number_input("Total Weight Transfer (0-360)", 0.0, 360.0, value=170.6)

# --- MAIN INTERFACE: FINITE DATA ---
st.header("Step 2: Finite Data Entry (%)")
tab1, tab2, tab3 = st.tabs(["Rotation", "Structural", "Weight Transfer"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Body Parts")
        rot_b = {p: st.slider(f"R-{p}", 0, 100, 50) for p in BODY_PARTS}
    with col2:
        st.subheader("Milestones")
        rot_m = {m: st.slider(f"R-{m}", 0, 100, 50) for m in MILESTONES}

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Body Parts")
        struc_b = {p: st.slider(f"S-{p}", 0, 100, 50) for p in BODY_PARTS}
    with col2:
        st.subheader("Structural Factors")
        struc_f = {f: st.slider(f"S-{f}", 0, 100, 50) for f in STRUCTURAL_FACTORS}

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Body Parts")
        trans_b = {p: st.slider(f"W-{p}", 0, 100, 50) for p in BODY_PARTS}
    with col2:
        st.subheader("Milestones")
        trans_m = {m: st.slider(f"W-{m}", 0, 100, 50) for m in MILESTONES}

# --- GENERATE ANALYSIS ---
if st.button("Generate Full Clinical Analysis"):
    tax = gravity_logic.calculate_gravity_tax(rot_total, struc_total, trans_total)
    
    # Aggregation Logic
    cum_body = {p: rot_b[p] + struc_b[p] + trans_b[p] for p in BODY_PARTS}
    cum_miles = {m: rot_m[m] + trans_m[m] for m in MILESTONES}
    
    ranked_body = sorted(cum_body.items(), key=lambda x: x[1], reverse=True)
    ranked_miles = sorted(cum_miles.items(), key=lambda x: x[1], reverse=True)
    ranked_struc = sorted(struc_f.items(), key=lambda x: x[1], reverse=True)

    st.divider()
    st.header(f"Analysis for {name}")
    st.metric("Calculated Gravity Tax", f"{tax:.4f}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("**Top Body Stressors**")
        st.write(pd.DataFrame(ranked_body[:5], columns=["Part", "Pts"]))
    with c2:
        st.write("**Top Milestone Resistance**")
        st.write(pd.DataFrame(ranked_miles[:5], columns=["Milestone", "Pts"]))
    with c3:
        st.write("**Top Structural Factors**")
        st.write(pd.DataFrame(ranked_struc[:5], columns=["Factor", "%"]))

    # CSV DOWNLOAD
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["The Fractal Code Clinical Report", name])
    writer.writerow(["Gravity Tax", tax])
    writer.writerow(["Top Body Part", ranked_body[0][0]])
    writer.writerow(["Top Milestone", ranked_miles[0][0]])
    
    st.download_button(
        label="Download Full CSV Report",
        data=output.getvalue(),
        file_name=f"{name}_report.csv",
        mime="text/csv"
    )
