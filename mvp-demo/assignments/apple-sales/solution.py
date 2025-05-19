"""
Apple Sales Program Solution

This program implements a simple apple sales system with validation and receipt generation.
"""

def calculate_cost(quantity, price):
    """
    Calculate the total cost of apples.
    
    >>> calculate_cost(10, 0.25)
    2.5
    >>> calculate_cost(0, 0.25)
    0.0
    >>> calculate_cost(100, 0.25)
    25.0
    """
    return quantity * price

def greet_customer(name):
    """
    Generate a personalized greeting for a customer.
    
    >>> greet_customer("John")
    'Hello, John! Welcome to Norris\\' Apple Orchard.'
    >>> greet_customer("")
    'Hello! Welcome to Norris\\' Apple Orchard.'
    """
    if name:
        return f"Hello, {name}! Welcome to Norris' Apple Orchard."
    else:
        return f"Hello! Welcome to Norris' Apple Orchard."

def display_receipt(name, quantity, cost):
    """
    Generate a formatted receipt string.
    
    >>> display_receipt("John", 10, 2.5)
    '----- RECEIPT -----\\nCustomer: John\\nQuantity: 10 apples\\nTotal Cost: $2.50\\nThank you for shopping at Norris\\' Apple Orchard!'
    >>> display_receipt("", 5, 1.25)
    '----- RECEIPT -----\\nCustomer: Guest\\nQuantity: 5 apples\\nTotal Cost: $1.25\\nThank you for shopping at Norris\\' Apple Orchard!'
    """
    customer_name = name if name else "Guest"
    return f"----- RECEIPT -----\nCustomer: {customer_name}\nQuantity: {quantity} apples\nTotal Cost: ${cost:.2f}\nThank you for shopping at Norris' Apple Orchard!"

def validate_quantity(quantity, inventory):
    """
    Validate that the quantity is a valid number and doesn't exceed inventory.
    
    >>> validate_quantity(10, 100)
    True
    >>> validate_quantity(0, 100)
    False
    >>> validate_quantity(101, 100)
    False
    >>> validate_quantity(-5, 100)
    False
    """
    return quantity > 0 and quantity <= inventory

def main():
    """Main function to run the apple sales program."""
    # Constants
    INVENTORY = 100
    PRICE = 0.25
    
    print("Welcome to the Apple Sales Program!")
    
    # Get customer name
    name = input("Please enter your name: ")
    
    # Display greeting and inventory information
    print(greet_customer(name))
    print(f"We have {INVENTORY} apples available.")
    print(f"Each apple costs ${PRICE:.2f}.")
    
    # Get quantity and validate
    try:
        quantity = int(input("How many apples would you like to purchase? "))
        
        if not validate_quantity(quantity, INVENTORY):
            if quantity <= 0:
                print("Sorry, quantity must be greater than zero.")
            else:
                print(f"Sorry, we only have {INVENTORY} apples available.")
            return
            
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Calculate cost
    cost = calculate_cost(quantity, PRICE)
    
    # Display receipt
    print(display_receipt(name, quantity, cost))

if __name__ == "__main__":
    main()