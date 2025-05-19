"""Student 1: Perfect submission with all requirements met"""

def add(a, b):
    """
    Return the sum of two numbers.
    
    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b

def subtract(a, b):
    """
    Return the difference between two numbers.
    
    >>> subtract(5, 2)
    3
    >>> subtract(2, 5)
    -3
    """
    return a - b

def multiply(a, b):
    """
    Return the product of two numbers.
    
    >>> multiply(3, 4)
    12
    >>> multiply(-2, 3)
    -6
    """
    return a * b

def divide(a, b):
    """
    Return a divided by b. Raises ZeroDivisionError if b is 0.
    
    >>> divide(10, 2)
    5.0
    >>> divide(7, 2)
    3.5
    >>> divide(5, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: Cannot divide by zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def factorial(n):
    """
    Return the factorial of n (n!).
    
    >>> factorial(0)
    1
    >>> factorial(5)
    120
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: Factorial is not defined for negative numbers
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result