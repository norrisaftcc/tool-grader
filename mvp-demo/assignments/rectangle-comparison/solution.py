"""
Rectangle Comparison Solution

This program compares the areas of two rectangles.
"""

def calculate_area(length, width):
    """
    Calculate the area of a rectangle.
    
    >>> calculate_area(4.5, 2.0)
    9.0
    >>> calculate_area(3.0, 3.0)
    9.0
    >>> calculate_area(5, 10)
    50
    >>> calculate_area(0, 10)
    0
    """
    return length * width

def compare_areas(area1, area2):
    """
    Compare two areas and return a string indicating which is larger or if they're equal.
    
    >>> compare_areas(10, 5)
    'Rectangle 1 has the larger area.'
    >>> compare_areas(5, 10)
    'Rectangle 2 has the larger area.'
    >>> compare_areas(10, 10)
    'The rectangles have equal areas.'
    """
    if area1 > area2:
        return "Rectangle 1 has the larger area."
    elif area2 > area1:
        return "Rectangle 2 has the larger area."
    else:
        return "The rectangles have equal areas."

def get_float_input(prompt):
    """
    Get a valid float input from the user, rejecting non-numeric and negative values.
    
    This function prompts the user repeatedly until a valid input is received.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Error: Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def get_rectangle_dimensions(rectangle_num):
    """
    Prompt the user for length and width of a rectangle and return them as a tuple.
    
    This function includes input validation to ensure positive numeric values.
    """
    print(f"\nEnter dimensions for Rectangle {rectangle_num}:")
    length = get_float_input("Length: ")
    width = get_float_input("Width: ")
    return length, width

def main():
    """Main function to run the rectangle comparison program."""
    print("Rectangle Comparison Program")
    print("---------------------------")
    
    # Get dimensions for both rectangles
    length1, width1 = get_rectangle_dimensions(1)
    length2, width2 = get_rectangle_dimensions(2)
    
    # Calculate areas
    area1 = calculate_area(length1, width1)
    area2 = calculate_area(length2, width2)
    
    # Display results
    print("\nResults:")
    print(f"Rectangle 1 has an area of {area1} square units.")
    print(f"Rectangle 2 has an area of {area2} square units.")
    print(compare_areas(area1, area2))

if __name__ == "__main__":
    main()