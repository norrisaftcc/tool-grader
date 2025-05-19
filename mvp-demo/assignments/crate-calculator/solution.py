"""
Crate Calculator Solution

This program calculates costs and profit for wooden crates.
"""

# Constants
COST_PER_CUBIC_FOOT = 0.23
CHARGE_PER_CUBIC_FOOT = 0.50

def calculate_volume(length, width, height):
    """
    Calculate the volume of a crate.
    
    >>> calculate_volume(4, 3, 2)
    24.0
    >>> calculate_volume(10, 10, 10)
    1000.0
    >>> calculate_volume(1.5, 2.5, 3.5)
    13.125
    >>> calculate_volume(0, 5, 5)
    0.0
    """
    return length * width * height

def calculate_cost(volume, cost_per_cubic_foot=COST_PER_CUBIC_FOOT):
    """
    Calculate the production cost based on volume.
    
    >>> calculate_cost(24.0)
    5.52
    >>> calculate_cost(1000.0)
    230.0
    >>> calculate_cost(13.125)
    3.02
    """
    return round(volume * cost_per_cubic_foot, 2)

def calculate_charge(volume, charge_per_cubic_foot=CHARGE_PER_CUBIC_FOOT):
    """
    Calculate the selling price based on volume.
    
    >>> calculate_charge(24.0)
    12.0
    >>> calculate_charge(1000.0)
    500.0
    >>> calculate_charge(13.125)
    6.56
    """
    return round(volume * charge_per_cubic_foot, 2)

def calculate_profit(charge, cost):
    """
    Calculate the profit (selling price - production cost).
    
    >>> calculate_profit(12.0, 5.52)
    6.48
    >>> calculate_profit(500.0, 230.0)
    270.0
    >>> calculate_profit(6.56, 3.02)
    3.54
    """
    return round(charge - cost, 2)

def format_results(dimensions, volume, cost, charge, profit):
    """
    Generate a formatted results string.
    
    >>> dimensions = (4.0, 3.0, 2.0)
    >>> print(format_results(dimensions, 24.0, 5.52, 12.0, 6.48))
    Results:
    -----------------------
    Crate dimensions: 4.0 × 3.0 × 2.0 feet
    Volume: 24.0 cubic feet
    Production cost: $5.52
    Selling price: $12.00
    Profit: $6.48
    -----------------------
    
    >>> dimensions = (10.0, 10.0, 10.0)
    >>> print(format_results(dimensions, 1000.0, 230.0, 500.0, 270.0))
    Results:
    -----------------------
    Crate dimensions: 10.0 × 10.0 × 10.0 feet
    Volume: 1000.0 cubic feet
    Production cost: $230.00
    Selling price: $500.00
    Profit: $270.00
    -----------------------
    """
    length, width, height = dimensions
    return f"""Results:
-----------------------
Crate dimensions: {length} × {width} × {height} feet
Volume: {volume} cubic feet
Production cost: ${cost:.2f}
Selling price: ${charge:.2f}
Profit: ${profit:.2f}
-----------------------"""

def get_float_input(prompt):
    """
    Get a valid float input from the user, rejecting non-numeric and negative values.
    
    This function prompts the user repeatedly until a valid input is received.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Error: Dimensions cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def main():
    """Main function to run the crate calculator program."""
    print("Crate Cost Calculator")
    print("---------------------")
    
    print("\nEnter crate dimensions in feet:")
    length = get_float_input("Length: ")
    width = get_float_input("Width: ")
    height = get_float_input("Height: ")
    
    # Calculate results
    dimensions = (length, width, height)
    volume = calculate_volume(length, width, height)
    cost = calculate_cost(volume)
    charge = calculate_charge(volume)
    profit = calculate_profit(charge, cost)
    
    # Display results
    print("\n" + format_results(dimensions, volume, cost, charge, profit))

if __name__ == "__main__":
    main()