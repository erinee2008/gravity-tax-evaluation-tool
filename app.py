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
    "front and back heart structure", "buoyancy", "counterbalance", 
    "momentum slow", "momentum normal"
]

st.set_page_config(page_title="Gravity Tax Tool", layout="wide")

st.title("🧬 Gravity Tax Evaluation Tool")
st.write("Clinical analysis tool for **The Fractal Series** in association with **Movement Lesson**.")

# --- SIDEBAR: OVERALL TOTALS ---
st.sidebar.header("Step 1: Overarching Totals")
name = st.sidebar.text_input("Child's Name", "Subject A")
rot_total = st.sidebar.number_input("Total Rotation (0-360)", 0.0, 360.0, value=129.1)
struc_total = st.sidebar.number_input("Total Structural (0-360)", 0.0, 360.0, value=134.05)
trans_total = st.sidebar.number_input("Total Weight Transfer (0-360)", 0.0, 360.0, value=170.6)

# --- DATA ENTRY METHOD ---
st.header("Step 2: Clinical Data Entry")
entry_mode = st.radio("Choose Entry Method:", ["Bulk Paste (Digital)", "Manual Sliders"], horizontal=True)

def parse_paste(raw_text, expected_len):
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    values = []
    for x in lines:
        try:
            clean_val = x.replace('%','').replace('pts','').strip()
            values.append(float(clean_val))
        except ValueError:
            pass
    return (values + [0.0]*expected_len)[:expected_len]

if entry_mode == "Bulk Paste (Digital)":
    st.info("Paste your columns of numbers below. Ensure the order matches your digital evaluation sheets.")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Rotation Data")
        rot_raw = st.text_area("Paste Rotation Column (Body + Milestones)", height=200)
        r_vals = parse_paste(rot_raw, len(BODY_PARTS) + len(MILESTONES))
        rot_b = dict(zip(BODY_PARTS, r_vals[:len(BODY_PARTS)]))
        rot_m = dict(zip(MILESTONES, r_vals[len(BODY_PARTS):]))

    with col2:
        st.subheader("Structural Data")
        struc_raw = st.text_area("Paste Structural Column (Body + Factors)", height=200)
        s_vals = parse_paste(struc_raw, len(BODY_PARTS) + len(STRUCTURAL_FACTORS))
        struc_b = dict(zip(BODY_PARTS, s_vals[:len(BODY_PARTS)]))
        struc_f = dict(zip(STRUCTURAL_FACTORS, s_vals[len(BODY_PARTS):]))

    with col3:
        st.subheader("Weight Transfer Data")
        trans_raw = st.text_area("Paste Weight Transfer Column (Body + Milestones)", height=200)
        w_vals = parse_paste(trans_raw, len(BODY_PARTS) + len(MILESTONES))
        trans_b = dict(zip(BODY_PARTS, w_vals[:len(BODY_PARTS)]))
        trans_m = dict(zip(MILESTONES, w_vals[len(BODY_PARTS):]))
else:
    tab1, tab2, tab3 = st.tabs(["Rotation", "Structural", "Weight Transfer"])
    with tab1:
        c1, c2 = st.columns(2)
        rot_b = {p: c1.slider(f"R-{p}", 0, 100, 0) for p in BODY_PARTS}
        rot_m = {m: c2.slider(f"R-{m}", 0, 100, 0) for m in MILESTONES}
    with tab2:
        c1, c2 = st.columns(2)
        struc_b = {p: c1.slider(f"S-{p}", 0, 100, 0) for p in BODY_PARTS}
        struc_f = {f: c2.slider(f"S-{f}", 0, 100, 0) for f in STRUCTURAL_FACTORS}
    with tab3:
        c1, c2 = st.columns(2)
        trans_b = {p: c1.slider(f"W-{p}", 0, 100, 0) for p in BODY_PARTS}
        trans_m = {m: c2.slider(f"W-{m}", 0, 100, 0) for m in MILESTONES}

if st.button("Calculate Full Clinical Report"):
    tax = gravity_logic.calculate_gravity_tax(rot_total, struc_total, trans_total)
    
    cum_body = {p: rot_b[p] + struc_b[p] + trans_b[p] for p in BODY_PARTS}
    cum_miles = {m: rot_m[m] + trans_m.get(m, 0) for m in MILESTONES}
    
    ranked_body = sorted(cum_body.items(), key=lambda x: x[1], reverse=True)
    ranked_miles = sorted(cum_miles.items(), key=lambda x: x[1], reverse=True)
    ranked_struc = sorted(struc_f.items(), key=lambda x: x[1], reverse=True)

    st.divider()
    st.header(f"Comprehensive Analysis: {name}")
    st.metric("Gravity Tax Score", f"{tax:.4f}")

    # FULL LISTS - Removed the [:5] limits
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("All Body Stressors")
        st.dataframe(pd.DataFrame(ranked_body, columns=["Body Part", "Points"]), height=500)
    with c2:
        st.subheader("All Milestone Resistance")
        st.dataframe(pd.DataFrame(ranked_miles, columns=["Milestone", "Points"]), height=500)
    with c3:
        st.subheader("All Structural Factors")
        st.dataframe(pd.DataFrame(ranked_struc, columns=["Factor", "% Deficit"]), height=500)

    st.success(f"**Action Plan:** Focus on {ranked_body[0][0].upper()}, {ranked_miles[0][0].upper()}, and {ranked_struc[0][0].upper()}.")

    # CSV DOWNLOAD
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 1. Header and Overarching Stats
    writer.writerow(["GRAVITY TAX CLINICAL REPORT", name.upper()])
    writer.writerow(["Date", datetime.now().strftime("%Y-%m-%d")])
    writer.writerow(["Gravity Tax Score", f"{tax:.4f}"])
    writer.writerow(["Action Plan", f"Focus on {ranked_body[0][0].upper()}, {ranked_miles[0][0].upper()}, and {ranked_struc[0][0].upper()}"])
    writer.writerow([]) # Blank row for spacing

    # 2. Complete Body Stressor Ranking
    writer.writerow(["ALL BODY STRESSOR COMPONENTS (RANKED)"])
    writer.writerow(["Component", "Cumulative Stress Points"])
    for item, score in ranked_body:
        writer.writerow([item, round(score, 2)])
    writer.writerow([])

    # 3. Complete Milestone Resistance
    writer.writerow(["ALL MILESTONE RESISTANCE (RANKED)"])
    writer.writerow(["Milestone", "Resistance Points"])
    for item, score in ranked_miles:
        writer.writerow([item, round(score, 2)])
    writer.writerow([])

    # 4. Complete Structural Factors
    writer.writerow(["ALL STRUCTURAL BOTTLENECKS (RANKED)"])
    writer.writerow(["Structural Factor", "Percentage Deficit"])
    for item, score in ranked_struc:
        writer.writerow([item, f"{round(score, 2)}%"])
    
    st.download_button(
        label="📥 Download Full Comprehensive Report",
        data=output.getvalue(),
        file_name=f"{name.replace(' ', '_')}_Full_Clinical_Analysis.csv",
        mime="text/csv"
    )
