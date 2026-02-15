import gravity_logic
import csv
from datetime import datetime

# --- EXACT DATA CATEGORIES FROM CLINICAL CHARTS ---
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

def show_instructions():
    print("\n" + "="*65)
    print(" FRACTAL DEVELOPMENT: CLINICAL DIAGNOSTIC TOOL ")
    print("="*65)
    print("This tool processes high-level totals and granular chart data.")
    print("Includes a verification step to ensure data integrity.")
    print("-" * 65)

def get_interpretation(tax_score):
    if tax_score <= 0.25: return ("Low Risk", "Optimal developmental progression likely.")
    elif tax_score <= 0.50: return ("Slight Risk", "Progression likely optimal; minor resistance.")
    elif tax_score <= 0.75: return ("Moderate Risk", "Progression may be delayed by rotational resistance.")
    else: return ("High Risk", "Progression likely significantly delayed or stopped.")

def get_valid_input(prompt, max_val=360):
    while True:
        try:
            val = float(input(prompt))
            if 0 <= val <= max_val: return val
            print(f"Invalid: Must be between 0 and {max_val}.")
        except ValueError: print("Invalid: Please enter a numeric value.")

def get_chart_data(category_list, section_name):
    """Gathers data and allows the user to restart if they make a mistake."""
    while True:
        print(f"\n--- {section_name.upper()} DATA ENTRY (%) ---")
        data = {}
        for item in category_list:
            data[item] = get_valid_input(f"  {item}: ", 100)
        
        # Verification Step
        print(f"\n>>> REVIEWING {section_name.upper()} DATA:")
        for item, score in data.items():
            print(f"  {item}: {score}%")
            
        confirm = input(f"\nIs this data correct? (y/n): ").lower()
        if confirm == 'y':
            return data
        print(f"\n[RESTARTING {section_name.upper()} ENTRY...]")

def get_full_ranking(data_dict):
    return sorted(data_dict.items(), key=lambda x: x[1], reverse=True)

def main():
    show_instructions()
    name = input("Enter Child's Name: ")

    # PART 1: OVERALL EVALUATION
    while True:
        print("\n[PART 1: OVERARCHING EVALUATION TOTALS]")
        rot_total = get_valid_input("  Total Rotation Score (0-360): ")
        struc_total = get_valid_input("  Total Structural Score (0-360): ")
        trans_total = get_valid_input("  Total Weight Transfer Score (0-360): ")
        
        print(f"\nReviewing Totals: Rot: {rot_total}, Struc: {struc_total}, Trans: {trans_total}")
        confirm = input("Are these totals correct? (y/n): ").lower()
        if confirm == 'y': break

    total_deficit = rot_total + struc_total + trans_total
    tax_score = gravity_logic.calculate_gravity_tax(rot_total, struc_total, trans_total)
    risk_level, risk_msg = get_interpretation(tax_score)

    # PART 2: FINITE CHART DATA
    rot_body = get_chart_data(BODY_PARTS, "Rotation Body Parts")
    rot_miles = get_chart_data(MILESTONES, "Rotation Milestones")

    struc_body = get_chart_data(BODY_PARTS, "Structural Body Parts")
    struc_facts = get_chart_data(STRUCTURAL_FACTORS, "Structural Factors")

    trans_body = get_chart_data(BODY_PARTS, "Weight Transfer Body Parts")
    trans_miles = get_chart_data(MILESTONES, "Weight Transfer Milestones")

    # --- AGGREGATION ---
    cum_body = {p: rot_body[p] + struc_body[p] + trans_body[p] for p in BODY_PARTS}
    cum_miles = {m: rot_miles[m] + trans_miles.get(m, 0) for m in MILESTONES}

    ranked_body = get_full_ranking(cum_body)
    ranked_miles = get_full_ranking(cum_miles)
    ranked_struc = get_full_ranking(struc_facts)

    # --- REPORTING ---
    report_header = f"\n{'='*65}\n FULL CLINICAL ANALYSIS: {name.upper()}\n{'='*65}"
    summary = (f"\nGENERAL OVERVIEW:\n  Total Deficit: {total_deficit:.2f} / 1080\n"
               f"  Calculated Gravity Tax: {tax_score:.4f} ({risk_level})")
    
    body_report = "\n\n[RANKED BODY PART STRESSORS]\n" + "\n".join([f"  {i+1:2}. {x[0]:18} : {x[1]:6.1f} pts" for i, x in enumerate(ranked_body)])
    mile_report = "\n\n[RANKED MILESTONE RESISTANCE]\n" + "\n".join([f"  {i+1:2}. {x[0]:25} : {x[1]:6.1f} pts" for i, x in enumerate(ranked_miles)])
    struc_report = "\n\n[RANKED STRUCTURAL BOTTLENECKS]\n" + "\n".join([f"  {i+1:2}. {x[0]:28} : {x[1]:6.1f}%" for i, x in enumerate(ranked_struc)])

    action_plan = (f"\n\n{'='*65}\nTHERAPIST ACTION PLAN:\n"
                   f"Focus intervention on {ranked_body[0][0].upper()} to reduce structural\n"
                   f"resistance in {ranked_miles[0][0].upper()} via {ranked_struc[0][0].upper()}.\n"
                   f"{'='*65}")
    
    full_report = report_header + summary + body_report + mile_report + struc_report + action_plan
    print(full_report)

    # --- LOGGING ---
    filename = f"{name.replace(' ', '_')}_full_report.txt"
    with open(filename, "wt") as f: f.write(full_report)
    
    with open("development_tracker.csv", "at", newline="") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Date", "Name", "Gravity Tax", "Primary Stressor", "Primary Milestone"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), name, tax_score, ranked_body[0][0], ranked_miles[0][0]])

    print(f"\nSuccess: Full report saved to {filename}")

if __name__ == "__main__":
    main()