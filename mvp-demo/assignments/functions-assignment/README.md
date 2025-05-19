# Python Functions Assignment

Create a file named `functions.py` that implements the following functions:

## Required Functions

1. `add(a, b)`: Returns the sum of a and b
2. `subtract(a, b)`: Returns a minus b
3. `multiply(a, b)`: Returns the product of a and b
4. `divide(a, b)`: Returns a divided by b (handle division by zero)
5. `factorial(n)`: Returns the factorial of n (n!)

## Requirements

Each function must include:
- A docstring describing what it does
- At least one doctest example
- Proper error handling where appropriate

## Example

```python
def add(a, b):
    """
    Return the sum of two numbers.
    
    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b
```

## Grading

Your submission will be automatically graded based on:
- Correctness of implementation (70%)
- Presence of doctests (20%)
- Proper error handling (10%)