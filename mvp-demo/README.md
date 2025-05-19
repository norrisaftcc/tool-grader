# Python Autograder MVP Demo

This is a simplified demo of the Python Autograder system using local directories instead of GitHub Classroom and Canvas LMS integration.

## Structure

- `assignments/` - Contains assignment specifications and reference solutions
- `submissions/` - Contains student submissions for grading
- `results/` - Contains grading results (generated when you run the grader)

## Running the Demo

To run the autograder:

```bash
# Make sure you're in the tool-grader root directory
python mvp-demo/grade.py
```

This will:
1. Run tests on all student submissions in the `submissions/` directory
2. Generate detailed grading results in the `results/` directory
3. Show a summary of grades in the console

## Demo Assignment

The demo contains a simple "Python Functions Assignment" that tests students' ability to:
- Implement basic functions correctly
- Write proper doctests
- Handle errors appropriately

### Student Submissions

The demo includes three sample student submissions:
- `student1` - Perfect submission with all requirements met
- `student2` - Partial submission with some missing features
- `student3` - Poor submission with several bugs and missing functions

## Grading Criteria

The grader evaluates submissions based on:
- **Implementation (70%)** - Are the required functions implemented correctly?
- **Doctests (20%)** - Are there doctests for each function?
- **Error Handling (10%)** - Are edge cases handled properly?

## How It Works

The grader:
1. Dynamically loads each student's Python module
2. Runs doctests on the module and collects results
3. Checks if required functions are implemented
4. Verifies proper error handling for edge cases
5. Calculates scores based on the criteria
6. Generates detailed feedback in Markdown format
7. Stores raw results in JSON format for further processing

## Next Steps

This MVP demonstrates the core grading functionality. In the full system, this would be:
1. Integrated with GitHub Classroom for submission collection
2. Dockerized for secure execution
3. Connected to Canvas LMS for grade reporting
4. Expanded with more sophisticated test frameworks