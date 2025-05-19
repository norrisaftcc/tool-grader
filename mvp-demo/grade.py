#!/usr/bin/env python3
"""
Simple grader for the Python Functions Assignment MVP.

This script runs doctests on student submissions and generates 
result files showing passed/failed tests and calculated scores.
"""

import os
import sys
import doctest
import importlib.util
import json
from pathlib import Path
import shutil

# Configuration
ASSIGNMENTS_DIR = Path("mvp-demo/assignments")
SUBMISSIONS_DIR = Path("mvp-demo/submissions")
RESULTS_DIR = Path("mvp-demo/results")

# Ensure results directory exists and is empty
if RESULTS_DIR.exists():
    shutil.rmtree(RESULTS_DIR)
RESULTS_DIR.mkdir(exist_ok=True)

def load_module_from_file(file_path):
    """Dynamically load a Python module from a file path."""
    module_name = Path(file_path).stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def run_doctest(module):
    """Run doctest on a module and return results."""
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
                from io import StringIO
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
    """Check if a function is implemented in the module."""
    try:
        return hasattr(module, function_name)
    except:
        return False

def check_error_handling(module):
    """Check if the module properly handles errors in divide and factorial."""
    error_handling_score = 0
    
    # Check divide function error handling
    try:
        if hasattr(module, 'divide'):
            try:
                module.divide(1, 0)
                # Should have raised an exception
            except ZeroDivisionError:
                error_handling_score += 5
            except:
                # Raised some exception, partial credit
                error_handling_score += 2
    except:
        pass
    
    # Check factorial function error handling
    try:
        if hasattr(module, 'factorial'):
            try:
                module.factorial(-1)
                # Should have raised an exception
            except ValueError:
                error_handling_score += 5
            except:
                # Raised some exception, partial credit
                error_handling_score += 2
    except:
        pass
    
    return error_handling_score

def grade_submission(student_dir, assignment_dir):
    """Grade a student submission and return results."""
    student_file = student_dir / "functions.py"
    
    # Check if the student file exists
    if not student_file.exists():
        return {
            "error": f"Student file {student_file} does not exist",
            "score": 0,
            "max_score": 100
        }
    
    # Load the module
    try:
        module = load_module_from_file(student_file)
    except Exception as e:
        return {
            "error": f"Failed to load module: {str(e)}",
            "score": 0,
            "max_score": 100
        }
    
    # Check if required functions are implemented
    required_functions = ['add', 'subtract', 'multiply', 'divide', 'factorial']
    implemented_functions = []
    
    for func in required_functions:
        if check_function_implementation(module, func):
            implemented_functions.append(func)
    
    # Run doctests
    doctest_results = run_doctest(module)
    
    # Calculate scores
    implementation_score = len(implemented_functions) / len(required_functions) * 70
    
    # Count functions with doctests
    functions_with_doctests = set()
    for result in doctest_results:
        # Extract function name from doctest name (e.g., 'module.function')
        parts = result["name"].split('.')
        if len(parts) > 1:
            functions_with_doctests.add(parts[1])
    
    doctest_score = len(functions_with_doctests) / len(required_functions) * 20
    
    # Check error handling
    error_handling_score = check_error_handling(module)
    
    total_score = implementation_score + doctest_score + error_handling_score
    
    # Generate results
    passed_tests = sum(1 for r in doctest_results if r["success"])
    total_tests = len(doctest_results)
    
    return {
        "student": student_dir.name,
        "implemented_functions": implemented_functions,
        "missing_functions": [f for f in required_functions if f not in implemented_functions],
        "functions_with_doctests": list(functions_with_doctests),
        "doctest_results": doctest_results,
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
    """Format grading results as markdown."""
    md = f"# Grading Results for {results['student']}\n\n"
    
    # Summary
    md += "## Summary\n\n"
    if "error" in results:
        md += f"**Error:** {results['error']}\n\n"
        md += f"**Score:** {results['score']} / {results['max_score']}\n\n"
        return md
    
    score = results['scores']['total']
    max_score = results['max_score']
    md += f"**Score:** {score:.1f} / {max_score} ({score/max_score*100:.1f}%)\n\n"
    
    # Function Implementation
    md += "## Function Implementation\n\n"
    md += f"**Implemented:** {', '.join(results['implemented_functions'])}\n\n"
    if results['missing_functions']:
        md += f"**Missing:** {', '.join(results['missing_functions'])}\n\n"
    else:
        md += "**Missing:** None\n\n"
    
    # Doctest Results
    md += "## Doctest Results\n\n"
    md += f"**Functions with doctests:** {', '.join(results['functions_with_doctests'])}\n\n"
    md += f"**Passed tests:** {results['passed_tests']} / {results['total_tests']}\n\n"
    
    # Detailed Results
    md += "## Detailed Test Results\n\n"
    for test_result in results['doctest_results']:
        md += f"### {test_result['name']}\n\n"
        md += f"**Status:** {'Passed' if test_result['success'] else 'Failed'}\n\n"
        md += f"**Examples tested:** {test_result['examples']}\n\n"
        md += f"**Failures:** {test_result['failures']}\n\n"
        
        if test_result['output']:
            md += "**Output:**\n\n```\n"
            md += test_result['output']
            md += "```\n\n"
    
    # Score Breakdown
    md += "## Score Breakdown\n\n"
    md += f"* Implementation: {results['scores']['implementation']:.1f} / 70\n"
    md += f"* Doctests: {results['scores']['doctests']:.1f} / 20\n"
    md += f"* Error Handling: {results['scores']['error_handling']:.1f} / 10\n"
    md += f"* **Total:** {results['scores']['total']:.1f} / 100\n"
    
    return md

def main():
    """Main function to run the grader."""
    print("🔍 Running Python Functions Assignment Grader")
    print("-------------------------------------------")
    
    assignment_dir = ASSIGNMENTS_DIR / "functions-assignment"
    
    # Iterate over student submissions
    student_dirs = [d for d in SUBMISSIONS_DIR.iterdir() if d.is_dir()]
    
    for student_dir in student_dirs:
        print(f"\nGrading submission for {student_dir.name}...")
        
        # Grade the submission
        results = grade_submission(student_dir, assignment_dir)
        
        # Save raw results as JSON
        results_file = RESULTS_DIR / f"{student_dir.name}_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save formatted results as markdown
        markdown_file = RESULTS_DIR / f"{student_dir.name}_results.md"
        with open(markdown_file, 'w') as f:
            f.write(format_results_markdown(results))
        
        # Print summary
        if "error" in results:
            print(f"❌ Error: {results['error']}")
            print(f"Score: 0 / 100")
        else:
            score = results['scores']['total']
            print(f"✅ Completed: Score {score:.1f} / 100")
    
    print("\n✨ All submissions graded!")
    print(f"📊 Results saved to {RESULTS_DIR}")

if __name__ == "__main__":
    main()