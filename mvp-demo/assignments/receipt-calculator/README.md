# Receipt Calculator Assignment

Create a file named `receipt.py` that calculates and displays a formatted receipt for a purchase.

## Requirements

1. Your program must:
   - Calculate a receipt for a burger priced at $5.99
   - Apply an 8% sales tax
   - Display a formatted receipt showing:
     - Store name: "Norris' Burgers and Fries"
     - Subtotal (before tax)
     - Tax amount
     - Total price (after tax)

2. The program must include the following functions:
   - `calculate_tax(subtotal, tax_rate)`: Returns the tax amount
   - `calculate_total(subtotal, tax)`: Returns the total price
   - `format_receipt(store_name, subtotal, tax, total)`: Returns a formatted receipt string

3. All monetary values must be displayed with 2 decimal places.

## Example Output

```
RECEIPT
Norris' Burgers and Fries
Subtotal: $5.99
Tax (8.0%): $0.48
Total: $6.47
Thank you for your purchase!
```

## Test Cases

Your code should handle the following test cases:

1. A burger at $5.99 with 8% tax
2. A meal at $12.50 with 8% tax
3. Zero amount (free item) with 8% tax
4. Edge case: Large amount ($999.99) with 8% tax

## Grading

Your submission will be automatically graded based on:
- Correctness of calculations (40%)
- Function implementation (30%)
- Formatting of monetary values (20%)
- Code organization and documentation (10%)