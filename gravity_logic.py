def calculate_total_deficit(rotation, structural, weight_transfer):
    """Sums the scores from the three evaluation sheets (Max 1080)."""
    return rotation + structural + weight_transfer

def calculate_tax_coefficient(total_deficit):
    """Converts the deficit into a multiplier (1.0 to 2.0)."""
    MAX_POSSIBLE = 1080
    if total_deficit > MAX_POSSIBLE:
        total_deficit = MAX_POSSIBLE
    return 1 + (total_deficit / MAX_POSSIBLE)

def calculate_gravity_tax(rotation, structural, weight_transfer):
    """
    Calculates the Gravity Tax as a value between 0 and 1.
    0 = Perfect Rotation (No Tax)
    1 = No Rotation (Maximum Tax)
    """
    MAX_POSSIBLE = 1080
    total_score = rotation + structural + weight_transfer
    
    # Ensure the tax doesn't exceed 1.0
    if total_score > MAX_POSSIBLE:
        total_score = MAX_POSSIBLE
        
    tax = total_score / MAX_POSSIBLE
    return round(tax, 4)