# Crate Calculator Assignment

Create a file named `crate_calculator.py` that calculates costs and profit for wooden crates.

## Requirements

1. Your program must:
   - Ask the user to input dimensions for a crate (length, width, and height in feet)
   - Calculate the volume of the crate in cubic feet
   - Calculate the production cost ($0.23 per cubic foot)
   - Calculate the selling price ($0.50 per cubic foot)
   - Calculate the profit (selling price - production cost)
   - Display all information in a formatted output

2. The program must include the following functions:
   - `calculate_volume(length, width, height)`: Returns the volume of the crate
   - `calculate_cost(volume, cost_per_cubic_foot)`: Returns the production cost
   - `calculate_charge(volume, charge_per_cubic_foot)`: Returns the selling price
   - `calculate_profit(charge, cost)`: Returns the profit
   - `format_results(dimensions, volume, cost, charge, profit)`: Returns a formatted string with results

3. All monetary values must be displayed with 2 decimal places.

## Example Output

```
Crate Cost Calculator
---------------------

Enter crate dimensions in feet:
Length: 4
Width: 3
Height: 2

Results:
-----------------------
Crate dimensions: 4.0 × 3.0 × 2.0 feet
Volume: 24.0 cubic feet
Production cost: $5.52
Selling price: $12.00
Profit: $6.48
-----------------------
```

## Constants

Use these constants in your program:
- `COST_PER_CUBIC_FOOT = 0.23`
- `CHARGE_PER_CUBIC_FOOT = 0.50`

## Test Cases

Your code should handle the following test cases:

1. A crate with dimensions 4 × 3 × 2 feet
2. A crate with dimensions 10 × 10 × 10 feet
3. A crate with dimensions 1.5 × 2.5 × 3.5 feet
4. Input validation for non-numeric or negative values

## Grading

Your submission will be automatically graded based on:
- Correctness of calculations (40%)
- Function implementation (30%)
- Formatting of monetary values (15%)
- Input validation (10%)
- Code organization and documentation (5%)