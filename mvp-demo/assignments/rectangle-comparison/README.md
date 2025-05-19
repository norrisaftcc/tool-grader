# Rectangle Comparison Assignment

Create a file named `rectangles.py` that compares the areas of two rectangles.

## Requirements

1. Your program must:
   - Ask the user to input the length and width for two rectangles
   - Calculate the area of each rectangle
   - Compare the areas and determine which rectangle is larger (or if they're equal)
   - Display the results clearly to the user

2. The program must include the following functions:
   - `calculate_area(length, width)`: Returns the area of a rectangle
   - `compare_areas(area1, area2)`: Returns a string indicating which area is larger or if they're equal
   - `get_rectangle_dimensions(rectangle_num)`: Prompts the user and returns length and width for a rectangle

3. The program must handle:
   - Numeric input validation
   - Negative dimensions (should be rejected)
   - Proper rounding of display values when needed

## Example Interaction

```
Rectangle Comparison Program
---------------------------

Enter dimensions for Rectangle 1:
Length: 4.5
Width: 2.0

Enter dimensions for Rectangle 2:
Length: 3.0
Width: 3.0

Results:
Rectangle 1 has an area of 9.0 square units.
Rectangle 2 has an area of 9.0 square units.
The rectangles have equal areas.
```

## Test Cases

Your code should handle the following test cases:

1. Rectangle 1 larger than Rectangle 2
2. Rectangle 2 larger than Rectangle 1
3. Rectangles with equal areas
4. Rectangles with decimal dimensions
5. Input validation for non-numeric or negative values

## Grading

Your submission will be automatically graded based on:
- Correctness of area calculations (30%)
- Comparison logic (20%)
- Input validation (20%)
- Function implementation (20%)
- Code organization and documentation (10%)