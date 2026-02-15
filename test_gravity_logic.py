import gravity_logic
from pytest import approx

def test_calculate_gravity_tax():
    """
    Verifies that the Gravity Tax calculation correctly returns 
    a float between 0.0 and 1.0.
    """
    # Test Julia's actual data points: 129.1, 134.05, 170.6
    # Total Deficit: 433.75. Expected Tax: 0.4016
    assert gravity_logic.calculate_gravity_tax(129.1, 134.05, 170.6) == approx(0.4016, abs=0.0001)

    # Test perfect scores (No Deficit)
    assert gravity_logic.calculate_gravity_tax(0, 0, 0) == 0.0

    # Test maximum deficit (1080 total)
    assert gravity_logic.calculate_gravity_tax(360, 360, 360) == 1.0

def test_value_types():
    """
    Ensures the function handles float inputs correctly, 
    as clinical scores often include decimals.
    """
    result = gravity_logic.calculate_gravity_tax(10.5, 20.5, 30.0)
    assert isinstance(result, float)

if __name__ == "__main__":
    # This allows you to run the tests directly
    import pytest
    pytest.main(["-v", "test_gravity_logic.py"])