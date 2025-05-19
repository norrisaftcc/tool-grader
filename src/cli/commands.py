"""
Command Line Interface for Tool Grader

This module provides command-line tools for using the autograder.
"""

import argparse
import sys
import json
from pathlib import Path

from autograder.config import load_config
from autograder.test_runner import grade_submission, format_results_markdown


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Tool Grader - Python autograding system"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Grade command
    grade_parser = subparsers.add_parser("grade", help="Grade a submission")
    grade_parser.add_argument(
        "path", 
        help="Path to student submission (file or directory)"
    )
    grade_parser.add_argument(
        "--config", 
        help="Path to assignment configuration file"
    )
    grade_parser.add_argument(
        "--format", 
        choices=["json", "markdown"], 
        default="markdown",
        help="Output format (default: markdown)"
    )
    grade_parser.add_argument(
        "--output", 
        help="Path to write results (default: stdout)"
    )
    
    # Config test command
    config_parser = subparsers.add_parser(
        "test-config", 
        help="Test configuration loading"
    )
    config_parser.add_argument(
        "--config", 
        help="Path to configuration file"
    )
    
    # Version command
    subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 1
    
    # Handle version command
    if args.command == "version":
        from autograder import __version__
        print(f"Tool Grader version {__version__}")
        return 0
    
    # Handle config test command
    if args.command == "test-config":
        config = load_config(args.config)
        print(json.dumps(config.config, indent=2))
        return 0
    
    # Handle grade command
    if args.command == "grade":
        # Load assignment configuration if provided
        assignment_config = None
        if args.config:
            try:
                with open(args.config, 'r') as f:
                    assignment_config = json.load(f)
            except Exception as e:
                print(f"Error loading assignment configuration: {e}", file=sys.stderr)
                return 1
        
        # Grade the submission
        results = grade_submission(args.path, assignment_config)
        
        # Format the results
        if args.format == "json":
            output = json.dumps(results, indent=2)
        else:  # markdown
            output = format_results_markdown(results)
        
        # Write the results
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)
        
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())