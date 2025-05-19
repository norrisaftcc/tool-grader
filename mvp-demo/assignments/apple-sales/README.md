# Python Apple Sales Assignment

Create a file named `apple_sales.py` that implements a simple program for a virtual apple farm.

## Requirements

1. Create a program that:
   - Asks for the user's name and greets them
   - Displays the farm name as "Norris' Apple Orchard"
   - Shows the initial inventory (100 apples)
   - Displays apple price ($0.25 each)
   - Asks how many apples the user wants to buy
   - Calculates and displays the total cost
   - Thanks the user for their purchase

2. The program must include:
   - A function `calculate_cost(quantity, price)` that returns the total cost
   - A function `greet_customer(name)` that returns a greeting message
   - A function `display_receipt(name, quantity, cost)` that returns a formatted receipt string
   - Proper validation to ensure the quantity is a valid number and doesn't exceed inventory

## Example

Sample interaction (user input shown after prompts with >):

```
Welcome to the Apple Sales Program!
Please enter your name: > John
Hello, John! Welcome to Norris' Apple Orchard.
We have 100 apples available.
Each apple costs $0.25.
How many apples would you like to purchase? > 10
----- RECEIPT -----
Customer: John
Quantity: 10 apples
Total Cost: $2.50
Thank you for shopping at Norris' Apple Orchard!
```

## Grading

Your submission will be automatically graded based on:
- Correctness of calculation (30%)
- Function implementation (40%)
- Input validation (20%)
- Code organization and style (10%)