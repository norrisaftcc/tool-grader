"""
Receipt Calculator Solution

This program calculates and displays a formatted receipt with tax.
"""

def calculate_tax(subtotal, tax_rate):
    """
    Calculate the tax amount based on the subtotal and tax rate.
    
    >>> calculate_tax(5.99, 0.08)
    0.48
    >>> calculate_tax(12.50, 0.08)
    1.0
    >>> calculate_tax(0, 0.08)
    0.0
    >>> calculate_tax(999.99, 0.08)
    80.0
    """
    tax = subtotal * tax_rate
    # Round to 2 decimal places
    return round(tax, 2)

def calculate_total(subtotal, tax):
    """
    Calculate the total price by adding subtotal and tax.
    
    >>> calculate_total(5.99, 0.48)
    6.47
    >>> calculate_total(12.50, 1.0)
    13.5
    >>> calculate_total(0, 0)
    0.0
    >>> calculate_total(999.99, 80.0)
    1079.99
    """
    return subtotal + tax

def format_receipt(store_name, subtotal, tax, total, tax_rate=0.08):
    """
    Generate a formatted receipt string.
    
    >>> print(format_receipt("Norris' Burgers and Fries", 5.99, 0.48, 6.47))
    RECEIPT
    Norris' Burgers and Fries
    Subtotal: $5.99
    Tax (8.0%): $0.48
    Total: $6.47
    Thank you for your purchase!
    
    >>> print(format_receipt("Norris' Burgers and Fries", 12.50, 1.0, 13.50))
    RECEIPT
    Norris' Burgers and Fries
    Subtotal: $12.50
    Tax (8.0%): $1.00
    Total: $13.50
    Thank you for your purchase!
    """
    return f"""RECEIPT
{store_name}
Subtotal: ${subtotal:.2f}
Tax ({tax_rate*100:.1f}%): ${tax:.2f}
Total: ${total:.2f}
Thank you for your purchase!"""

def main():
    """Main function to run the receipt calculator."""
    # Constants
    STORE_NAME = "Norris' Burgers and Fries"
    BURGER_PRICE = 5.99
    TAX_RATE = 0.08
    
    # Calculate receipt
    subtotal = BURGER_PRICE
    tax = calculate_tax(subtotal, TAX_RATE)
    total = calculate_total(subtotal, tax)
    
    # Display receipt
    receipt = format_receipt(STORE_NAME, subtotal, tax, total)
    print(receipt)

if __name__ == "__main__":
    main()