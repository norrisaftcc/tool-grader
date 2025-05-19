"""Student 2: Partial submission - missing error handling and some doctests"""

def add(a, b):
    """
    Return the sum of two numbers.
    
    >>> add(2, 3)
    5
    """
    return a + b

def subtract(a, b):
    """Return the difference between two numbers."""
    return a - b

def multiply(a, b):
    """
    Return the product of two numbers.
    
    >>> multiply(3, 4)
    12
    """
    return a * b

def divide(a, b):
    """Return a divided by b."""
    # Missing error handling for division by zero
    return a / b

def factorial(n):
    """
    Return the factorial of n.
    
    >>> factorial(5)
    120
    """
    # Missing error handling for negative numbers
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result