# Python Autograder Configuration
# Assignment: Intro to Python Functions
# Course: CS101 - Introduction to Programming

# Basic assignment information
assignment:
  name: "Intro to Python Functions"
  canvas_id: 12345
  points_possible: 100
  due_date: "2025-09-30T23:59:59Z"
  
# GitHub repository information  
github:
  organization: "cs101-fall-2025"
  template_repo: "python-functions-template"
  classroom_url: "https://classroom.github.com/a/abcdefgh"
  
# Autograding configuration
grading:
  # Test configuration
  tests:
    - file: "functions.py"
      weight: 1.0  # 100% of grade comes from this file
      
  # Resource limits
  limits:
    memory: "256m"  # 256 MB maximum memory
    cpu: 0.5        # Half a CPU core
    timeout: 30     # 30 seconds maximum execution time
    
  # Feedback configuration  
  feedback:
    show_test_names: true        # Show names of tests to students
    show_test_docstrings: true   # Show test docstrings to students
    show_expected_output: true   # Show expected output for failed tests
    show_full_traceback: false   # Do not show full tracebacks, just summary
    
# Canvas integration
canvas:
  post_grades: true
  post_feedback: true
  update_existing: true  # Update existing submissions
  feedback_format: "markdown"  # Format feedback as markdown

# Sample assignment description (for reference)
description: |
  # Introduction to Python Functions
  
  In this assignment, you will practice creating and using functions in Python.
  
  ## Tasks:
  
  1. Implement the following functions in `functions.py`:
     - `add(a, b)`: Returns the sum of a and b
     - `subtract(a, b)`: Returns a minus b
     - `multiply(a, b)`: Returns the product of a and b
     - `divide(a, b)`: Returns a divided by b
     - `factorial(n)`: Returns the factorial of n
  
  2. Each function should include a docstring with:
     - A description of what the function does
     - Parameters and their types
     - Return value and type
     - At least one example in doctest format
  
  ## Grading:
  
  Your code will be graded based on:
  - Correctness: Does it produce the expected output?
  - Documentation: Are docstrings complete and formatted correctly?
  - Style: Does it follow Python best practices?
  
  All tests will be run using the built-in `doctest` module.
  
# Sample expected implementation (for reference)
expected_implementation: |
  def add(a, b):
      """
      Return the sum of two numbers.
      
      Args:
          a (int or float): First number
          b (int or float): Second number
          
      Returns:
          int or float: The sum of a and b
          
      Example:
          >>> add(2, 3)
          5
          >>> add(-1, 1)
          0
          >>> add(2.5, 3.5)
          6.0
      """
      return a + b
      
  def subtract(a, b):
      """
      Return the difference between two numbers.
      
      Args:
          a (int or float): First number
          b (int or float): Second number
          
      Returns:
          int or float: The result of a - b
          
      Example:
          >>> subtract(5, 2)
          3
          >>> subtract(2, 5)
          -3
          >>> subtract(10.5, 0.5)
          10.0
      """
      return a - b
