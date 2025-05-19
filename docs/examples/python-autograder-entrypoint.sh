#!/bin/bash
# entrypoint.sh - Container entrypoint script for Python Autograder

set -e  # Exit immediately if a command exits with a non-zero status

# Print Python version for logs
echo "Python Autograder Container"
echo "Python $(python --version)"
echo "------------------------------"

# Ensure results directory exists and is writable
if [ ! -d "/results" ]; then
    echo "Error: /results directory not mounted"
    exit 1
fi

# Check if code directory is mounted and has files
if [ ! -d "/code" ] || [ -z "$(ls -A /code)" ]; then
    echo "Error: /code directory not mounted or empty"
    exit 1
fi

# Set ulimits to prevent fork bombs and other resource exhaustion
# These are backup measures - the Docker container should also have limits
ulimit -u 50  # Max 50 processes
ulimit -f 10240  # Max 10MB file size

# Run the command
echo "Running: $@"
echo "------------------------------"

# Execute the command passed to the entrypoint
exec "$@"
