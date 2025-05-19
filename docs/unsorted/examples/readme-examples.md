# setting up components

# Python Autograder

## Repository Structure & README for MVP

Let's create a repository structure and README for the minimum viable product (MVP) of our Python autograding system, designed to be expandable as resources become available.

Now, let's create a sample MVP implementation of one of the core files - the test runner that will execute student code securely in Docker containers:

Let's also create a simple configuration file that would be used to define an assignment in our MVP:

Finally, let's create a simple Dockerfile that would be used to build the secure grading container:

These files provide a solid foundation for the MVP of our Python autograding system. Let me explain how they work together:

1. **Repository Structure & README** - Provides the overall organization of the codebase and documentation for developers and instructors.

2. **test_runner.py** - The core component that:
   - Runs student code securely in isolated Docker containers
   - Executes doctest-based tests (the simplest approach for our MVP)
   - Collects and formats test results
   - Generates feedback for students
   - Calculates scores based on test results

3. **autograder_config.yml** - A sample configuration file that:
   - Defines assignment details (name, points, due date)
   - Specifies GitHub repository information
   - Sets up grading parameters (which files to test, resource limits)
   - Configures feedback options
   - Provides reference implementation for instructors

4. **Dockerfile & entrypoint.sh** - Define the secure container that:
   - Creates a minimal Python environment
   - Runs as a non-root user
   - Sets resource limits to prevent attacks
   - Isolates student code from the host system

This MVP implementation prioritizes:

1. **Core functionality** - Basic autograding with doctest
2. **Security** - Secure isolation of student code
3. **Integration** - Connections to GitHub Classroom and Canvas
4. **Simplicity** - Straightforward setup and operation

It's designed to be expandable as resources become available, with clear extension points for:
- More sophisticated testing (pytest)
- LLM-generated tests
- Student-developed tests
- Improved analytics and feedback
