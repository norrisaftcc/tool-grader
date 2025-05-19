"""
Test Runner Module for Tool Grader

This module handles executing doctest on student submissions
and collecting results. It's based on the MVP demo implementation.
"""

import sys
import doctest
import importlib.util
import json
from pathlib import Path
from io import StringIO

from .config import get_config


def load_module_from_file(file_path):
    """
    Dynamically load a Python module from a file path.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Loaded module object
    """
    module_name = Path(file_path).stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        # Capture import/execution errors
        return {
            "error": f"Failed to load module: {str(e)}",
            "module_name": module_name
        }


def run_doctest(module):
    """
    Run doctest on a module and return results.
    
    Args:
        module: Python module object
        
    Returns:
        List of test results
    """
    # Handle modules that failed to load
    if isinstance(module, dict) and "error" in module:
        return [{
            "name": module.get("module_name", "unknown"),
            "error": module["error"],
            "examples": 0,
            "failures": 0,
            "success": False,
            "output": None
        }]
    
    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner(verbose=True)
    
    tests = finder.find(module)
    
    test_results = []
    for test in tests:
        if test.examples:  # Skip docstrings without examples
            output = ""
            old_stdout = sys.stdout
            try:
                # Capture doctest output
                fake_stdout = StringIO()
                sys.stdout = fake_stdout
                
                # Run the test
                failures, tests_run = runner.run(test)
                
                # Get the output
                output = fake_stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            test_results.append({
                "name": test.name,
                "examples": len(test.examples),
                "failures": failures,
                "success": failures == 0,
                "output": output
            })
    
    return test_results


def check_function_implementation(module, function_name):
    """
    Check if a function is implemented in the module.
    
    Args:
        module: Python module object
        function_name: Name of function to check
        
    Returns:
        True if function exists, False otherwise
    """
    try:
        return hasattr(module, function_name)
    except:
        return False


def check_error_handling(module, test_functions):
    """
    Check if the module properly handles error cases.
    
    Args:
        module: Python module object
        test_functions: Dictionary mapping function names to test cases
        
    Returns:
        Dictionary with error handling results
    """
    results = {}
    
    for func_name, test_cases in test_functions.items():
        if not check_function_implementation(module, func_name):
            continue
        
        func = getattr(module, func_name)
        results[func_name] = {}
        
        for case_name, case_info in test_cases.items():
            args = case_info.get("args", [])
            expected_exception = case_info.get("exception", None)
            
            try:
                # Call the function with test arguments
                result = func(*args)
                
                # If we expected an exception but didn't get one, mark as failed
                if expected_exception:
                    results[func_name][case_name] = {
                        "success": False,
                        "reason": f"Expected {expected_exception.__name__} but no exception was raised"
                    }
                else:
                    # No exception expected, and none raised - success
                    results[func_name][case_name] = {
                        "success": True
                    }
            except Exception as e:
                # Check if this is the expected exception
                if expected_exception and isinstance(e, expected_exception):
                    results[func_name][case_name] = {
                        "success": True
                    }
                else:
                    # Wrong exception or unexpected exception
                    results[func_name][case_name] = {
                        "success": False,
                        "reason": f"Got {type(e).__name__}, expected {'no exception' if not expected_exception else expected_exception.__name__}"
                    }
    
    return results


def grade_submission(student_code_path, assignment_config=None):
    """
    Grade a student submission.
    
    Args:
        student_code_path: Path to student submission
        assignment_config: Optional assignment-specific configuration
        
    Returns:
        Dictionary with grading results
    """
    # Set defaults from global config if not provided
    config = get_config()
    if not assignment_config:
        assignment_config = {}
    
    # Determine file(s) to grade
    if isinstance(student_code_path, (str, Path)):
        student_code_path = Path(student_code_path)
        
        # If it's a directory, look for Python files
        if student_code_path.is_dir():
            # Look for main file specified in assignment config
            main_file = assignment_config.get("main_file")
            if main_file and (student_code_path / main_file).exists():
                student_file = student_code_path / main_file
            else:
                # Find first Python file
                python_files = list(student_code_path.glob("*.py"))
                if not python_files:
                    return {
                        "error": f"No Python files found in {student_code_path}",
                        "score": 0,
                        "max_score": 100
                    }
                student_file = python_files[0]
        else:
            student_file = student_code_path
    else:
        return {
            "error": "Invalid student_code_path",
            "score": 0,
            "max_score": 100
        }
    
    # Ensure file exists
    if not student_file.exists():
        return {
            "error": f"Student file {student_file} does not exist",
            "score": 0,
            "max_score": 100
        }
    
    # Load the module
    module = load_module_from_file(student_file)
    
    # Check if required functions are implemented
    required_functions = assignment_config.get("required_functions", [])
    implemented_functions = []
    
    for func in required_functions:
        if check_function_implementation(module, func):
            implemented_functions.append(func)
    
    # Run doctests
    doctest_results = run_doctest(module)
    
    # Calculate scores
    implementation_weight = assignment_config.get("implementation_weight", 70)
    doctest_weight = assignment_config.get("doctest_weight", 20)
    error_handling_weight = assignment_config.get("error_handling_weight", 10)
    
    if required_functions:
        implementation_score = len(implemented_functions) / len(required_functions) * implementation_weight
    else:
        implementation_score = implementation_weight
    
    # Count functions with doctests
    functions_with_doctests = set()
    for result in doctest_results:
        # Extract function name from doctest name (e.g., 'module.function')
        parts = result["name"].split('.')
        if len(parts) > 1:
            functions_with_doctests.add(parts[1])
    
    if required_functions:
        doctest_score = len(functions_with_doctests) / len(required_functions) * doctest_weight
    else:
        doctest_score = doctest_weight
    
    # Check error handling if specified in assignment config
    error_handling_score = 0
    error_handling_results = {}
    
    if "error_cases" in assignment_config:
        error_handling_results = check_error_handling(module, assignment_config["error_cases"])
        
        # Calculate error handling score
        if error_handling_results:
            total_cases = 0
            passed_cases = 0
            
            for func_results in error_handling_results.values():
                for case_result in func_results.values():
                    total_cases += 1
                    if case_result["success"]:
                        passed_cases += 1
            
            if total_cases > 0:
                error_handling_score = (passed_cases / total_cases) * error_handling_weight
    
    total_score = implementation_score + doctest_score + error_handling_score
    
    # Generate results
    passed_tests = sum(1 for r in doctest_results if r.get("success", False))
    total_tests = len(doctest_results)
    
    return {
        "student_file": str(student_file),
        "implemented_functions": implemented_functions,
        "missing_functions": [f for f in required_functions if f not in implemented_functions],
        "functions_with_doctests": list(functions_with_doctests),
        "doctest_results": doctest_results,
        "error_handling_results": error_handling_results,
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "scores": {
            "implementation": implementation_score,
            "doctests": doctest_score,
            "error_handling": error_handling_score,
            "total": total_score
        },
        "max_score": 100
    }


def format_results_markdown(results):
    """
    Format grading results as markdown.
    
    Args:
        results: Grading results dictionary
        
    Returns:
        Markdown string with formatted results
    """
    if "error" in results:
        md = f"# Grading Results\n\n"
        md += f"**Error:** {results['error']}\n\n"
        md += f"**Score:** {results.get('score', 0)} / {results.get('max_score', 100)}\n\n"
        return md
    
    md = f"# Grading Results\n\n"
    
    # Summary
    score = results['scores']['total']
    max_score = results.get('max_score', 100)
    md += f"**Score:** {score:.1f} / {max_score} ({score/max_score*100:.1f}%)\n\n"
    
    # Function Implementation
    md += "## Function Implementation\n\n"
    md += f"**Implemented:** {', '.join(results['implemented_functions']) if results['implemented_functions'] else 'None'}\n\n"
    md += f"**Missing:** {', '.join(results['missing_functions']) if results['missing_functions'] else 'None'}\n\n"
    
    # Doctest Results
    md += "## Doctest Results\n\n"
    md += f"**Functions with doctests:** {', '.join(results['functions_with_doctests']) if results['functions_with_doctests'] else 'None'}\n\n"
    md += f"**Passed tests:** {results['passed_tests']} / {results['total_tests']}\n\n"
    
    # Detailed Results
    md += "## Detailed Test Results\n\n"
    for test_result in results['doctest_results']:
        md += f"### {test_result['name']}\n\n"
        md += f"**Status:** {'Passed' if test_result.get('success', False) else 'Failed'}\n\n"
        md += f"**Examples tested:** {test_result.get('examples', 0)}\n\n"
        md += f"**Failures:** {test_result.get('failures', 0)}\n\n"
        
        if test_result.get('output'):
            md += "**Output:**\n\n```\n"
            md += test_result['output']
            md += "```\n\n"
    
    # Error Handling Results
    if results.get('error_handling_results'):
        md += "## Error Handling Results\n\n"
        
        for func_name, cases in results['error_handling_results'].items():
            md += f"### {func_name}\n\n"
            
            for case_name, result in cases.items():
                status = "✅ Passed" if result["success"] else "❌ Failed"
                md += f"- **{case_name}**: {status}"
                
                if not result["success"] and "reason" in result:
                    md += f" - {result['reason']}"
                
                md += "\n"
            
            md += "\n"
    
    # Score Breakdown
    md += "## Score Breakdown\n\n"
    md += f"* Implementation: {results['scores']['implementation']:.1f} / {100 - results['scores']['doctests'] - results['scores']['error_handling']}\n"
    md += f"* Doctests: {results['scores']['doctests']:.1f} / {results['scores']['doctests'] + results['scores']['implementation'] - results['scores']['implementation']}\n"
    md += f"* Error Handling: {results['scores']['error_handling']:.1f} / {results['scores'].get('error_handling', 0) + results['scores']['doctests'] - results['scores']['doctests']}\n"
    md += f"* **Total:** {results['scores']['total']:.1f} / 100\n"
    
    return md


if __name__ == "__main__":
    """Simple CLI for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run doctest on Python code")
    parser.add_argument("path", type=str, help="Path to student code")
    
    args = parser.parse_args()
    
    # Grade the submission
    results = grade_submission(args.path)
    
    # Print formatted results
    print(format_results_markdown(results))
    print(f"Score: {results['scores']['total']:.1f}%")