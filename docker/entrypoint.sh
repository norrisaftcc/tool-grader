#!/bin/bash
# Entrypoint script for the autograder container

set -e

# Default command is to run Python doctest
if [ $# -eq 0 ]; then
    # Check if a specific file is provided in environment
    if [ -n "$SUBMISSION_FILE" ]; then
        echo "Running doctest on $SUBMISSION_FILE"
        python -m doctest -v "$SUBMISSION_FILE"
    else
        # Check for Python files in the code directory
        PYTHON_FILES=$(find /code -name "*.py" | sort)
        if [ -n "$PYTHON_FILES" ]; then
            echo "Running doctest on all Python files in /code"
            python -m doctest -v $PYTHON_FILES
        else
            echo "No Python files found in /code"
            exit 1
        fi
    fi
else
    # Execute the provided command
    exec "$@"
fi