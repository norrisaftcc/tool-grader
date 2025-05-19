"""Student 3: Poor submission - incorrect implementations and missing doctests"""

def add(a, b):
    """Add two numbers"""
    return a + b + 1  # Bug: adds extra 1

def subtract(a, b):
    # Missing docstring entirely
    return b - a  # Bug: reversed operation

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

# Missing divide function entirely

def factorial(n):
    """Calculate factorial"""
    # Bug: doesn't handle 0 correctly
    result = 1
    for i in range(1, n):  # Bug: should be n+1
        result *= i
    return result