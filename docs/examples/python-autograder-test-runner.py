"""
test_runner.py - Executes student Python code securely in Docker containers 
and evaluates results using doctest.

This is a core component of the Python Autograder MVP, responsible for:
1. Setting up secure Docker execution environments
2. Running student code with doctest 
3. Collecting and formatting test results
4. Handling execution errors and timeouts
"""

import os
import json
import tempfile
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import docker
from docker.errors import ContainerError, ImageNotFound

logger = logging.getLogger(__name__)

# Default resource constraints
DEFAULT_MEMORY_LIMIT = '256m'  # 256 MB memory limit
DEFAULT_CPU_LIMIT = 0.5        # Half a CPU core
DEFAULT_TIMEOUT = 30           # 30 seconds execution timeout

class DockerTestRunner:
    """Runs Python code tests inside a Docker container for security and isolation."""
    
    def __init__(
        self, 
        docker_image: str = 'python-autograder:latest',
        memory_limit: str = DEFAULT_MEMORY_LIMIT,
        cpu_limit: float = DEFAULT_CPU_LIMIT,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize the Docker test runner.
        
        Args:
            docker_image: Name of the Docker image to use
            memory_limit: Memory limit for the container (e.g., '256m')
            cpu_limit: CPU limit for the container (e.g., 0.5 = half a core)
            timeout: Timeout in seconds for test execution
        """
        self.docker_image = docker_image
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.timeout = timeout
        self.client = docker.from_env()
        
        # Verify the Docker image exists
        try:
            self.client.images.get(docker_image)
        except ImageNotFound:
            logger.error(f"Docker image '{docker_image}' not found. Did you build it?")
            raise
    
    def run_doctest(self, student_code_path: Path, module_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Run doctest on student code inside a Docker container.
        
        Args:
            student_code_path: Path to directory containing student code
            module_name: Optional specific module to test
                         If None, all Python files will be tested
                         
        Returns:
            Dict containing test results including:
            - success: Whether all tests passed
            - total: Total number of tests run
            - passed: Number of tests passed
            - failed: Number of tests failed
            - output: Raw doctest output
            - error: Any error messages (if tests couldn't be run)
        """
        # Create temporary directory for results
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            results_file = temp_path / "results.json"
            
            # Prepare volumes to mount in container
            volumes = {
                str(student_code_path.absolute()): {
                    'bind': '/code',
                    'mode': 'ro'  # read-only
                },
                str(temp_path.absolute()): {
                    'bind': '/results',
                    'mode': 'rw'  # read-write for output
                }
            }
            
            # Prepare command to run inside container
            command = ["python", "-m", "doctest"]
            
            if module_name:
                command.append(f"/code/{module_name}")
            else:
                command.append("/code")
                command.append("-v")  # verbose output
            
            command.extend([
                "-o", "ELLIPSIS",     # More flexible output comparison
                ">>", "/results/output.txt"
            ])
            
            # Create a simple script to capture doctest results
            wrapper_script = """
import sys
import os
import json
import doctest
import importlib.util
from pathlib import Path

def test_module(module_path):
    """Run doctest on a single module and return results."""
    try:
        # Import module dynamically
        module_name = Path(module_path).stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run doctest
        results = doctest.testmod(module, verbose=True)
        return {
            'file': module_path,
            'passed': results.attempted - results.failed,
            'failed': results.failed,
            'total': results.attempted,
            'success': results.failed == 0,
        }
    except Exception as e:
        return {
            'file': module_path,
            'error': str(e),
            'success': False,
        }

def test_directory(dir_path):
    """Test all Python files in a directory."""
    results = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                results.append(test_module(file_path))
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: script.py <file_or_directory>")
        sys.exit(1)
        
    path = sys.argv[1]
    if os.path.isdir(path):
        results = test_directory(path)
        summary = {
            'files_tested': len(results),
            'total_tests': sum(r.get('total', 0) for r in results if 'total' in r),
            'passed_tests': sum(r.get('passed', 0) for r in results if 'passed' in r),
            'failed_tests': sum(r.get('failed', 0) for r in results if 'failed' in r),
            'success': all(r.get('success', False) for r in results),
            'results': results
        }
    else:
        result = test_module(path)
        summary = {
            'files_tested': 1,
            'total_tests': result.get('total', 0),
            'passed_tests': result.get('passed', 0),
            'failed_tests': result.get('failed', 0),
            'success': result.get('success', False),
            'results': [result]
        }
        
    # Write results to JSON file
    with open('/results/results.json', 'w') as f:
        json.dump(summary, f, indent=2)
            """
            
            # Write the wrapper script to the temp directory
            wrapper_script_path = temp_path / "run_doctest.py"
            with open(wrapper_script_path, 'w') as f:
                f.write(wrapper_script)
            
            try:
                # Run container with resource constraints
                container = self.client.containers.run(
                    image=self.docker_image,
                    command=f"python /results/run_doctest.py /code",
                    volumes=volumes,
                    working_dir="/code",
                    mem_limit=self.memory_limit,
                    cpu_quota=int(100000 * self.cpu_limit),  # Docker uses microseconds
                    network_mode="none",  # No network access
                    cap_drop=["ALL"],     # Drop all capabilities
                    security_opt=["no-new-privileges:true"],
                    remove=True,          # Remove container after execution
                    detach=True
                )
                
                try:
                    # Wait for container to finish with timeout
                    exit_code = container.wait(timeout=self.timeout)
                    container_logs = container.logs().decode('utf-8')
                    
                    if exit_code['StatusCode'] != 0:
                        logger.error(f"Container exited with code {exit_code['StatusCode']}")
                        logger.error(f"Container logs: {container_logs}")
                        return {
                            'success': False,
                            'error': f"Execution failed with code {exit_code['StatusCode']}",
                            'output': container_logs
                        }
                        
                except Exception as e:
                    # Try to kill the container if it's still running
                    try:
                        container.kill()
                    except:
                        pass
                    
                    return {
                        'success': False,
                        'error': f"Execution timed out or failed: {str(e)}",
                        'output': None
                    }
                
                # Read results from the JSON file
                if results_file.exists():
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                    return results
                else:
                    return {
                        'success': False,
                        'error': "No results file was generated",
                        'output': container_logs if 'container_logs' in locals() else None
                    }
                    
            except ContainerError as e:
                logger.error(f"Container error: {str(e)}")
                return {
                    'success': False,
                    'error': f"Container error: {str(e)}",
                    'output': e.stderr.decode('utf-8') if e.stderr else None
                }
                
            except Exception as e:
                logger.error(f"Failed to run tests: {str(e)}")
                return {
                    'success': False,
                    'error': f"Failed to run tests: {str(e)}",
                    'output': None
                }
                
    def format_feedback(self, results: Dict[str, Any]) -> str:
        """
        Format test results into human-readable feedback.
        
        Args:
            results: Test results from run_doctest
            
        Returns:
            Formatted string with feedback
        """
        if 'error' in results and results['error']:
            feedback = f"Error running tests: {results['error']}\n\n"
            if results.get('output'):
                feedback += f"Output:\n{results['output']}"
            return feedback
            
        feedback = []
        
        # Add summary
        total_tests = results.get('total_tests', 0)
        passed_tests = results.get('passed_tests', 0)
        failed_tests = results.get('failed_tests', 0)
        
        feedback.append(f"# Test Results Summary")
        feedback.append(f"- Files tested: {results.get('files_tested', 0)}")
        feedback.append(f"- Total tests: {total_tests}")
        feedback.append(f"- Tests passed: {passed_tests}")
        feedback.append(f"- Tests failed: {failed_tests}")
        feedback.append(f"- Overall success: {'Yes' if results.get('success', False) else 'No'}")
        feedback.append("")
        
        # Add details for each file
        feedback.append(f"# Detailed Results")
        
        for file_result in results.get('results', []):
            file_name = file_result.get('file', 'Unknown file')
            # Extract just the filename, not the full path
            file_name = os.path.basename(file_name)
            
            feedback.append(f"## {file_name}")
            
            if 'error' in file_result and file_result['error']:
                feedback.append(f"Error: {file_result['error']}")
            else:
                passed = file_result.get('passed', 0)
                failed = file_result.get('failed', 0)
                total = file_result.get('total', 0)
                
                feedback.append(f"- Tests: {total}")
                feedback.append(f"- Passed: {passed}")
                feedback.append(f"- Failed: {failed}")
                feedback.append(f"- Result: {'Passed' if file_result.get('success', False) else 'Failed'}")
            
            feedback.append("")
            
        return "\n".join(feedback)
        
    def grade_submission(self, student_code_path: Path) -> Dict[str, Any]:
        """
        Grade a student submission directory.
        
        Args:
            student_code_path: Path to directory containing student code
            
        Returns:
            Dict containing:
            - score: Numeric score (percentage of tests passed)
            - feedback: Formatted feedback string
            - results: Raw test results
        """
        # Run tests
        results = self.run_doctest(student_code_path)
        
        # Calculate score (percentage of tests passed)
        total_tests = results.get('total_tests', 0)
        passed_tests = results.get('passed_tests', 0)
        
        if total_tests > 0:
            score = (passed_tests / total_tests) * 100
        else:
            score = 0 if results.get('error') else 100
            
        # Format feedback
        feedback = self.format_feedback(results)
        
        return {
            'score': score,
            'feedback': feedback,
            'results': results
        }


if __name__ == "__main__":
    # Simple CLI for testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Run doctest on Python code in a Docker container")
    parser.add_argument("path", type=str, help="Path to directory containing student code")
    parser.add_argument("--module", type=str, help="Specific module to test", default=None)
    parser.add_argument("--timeout", type=int, help="Timeout in seconds", default=DEFAULT_TIMEOUT)
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create test runner
    runner = DockerTestRunner(timeout=args.timeout)
    
    # Run tests
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path {path} does not exist")
        exit(1)
        
    results = runner.grade_submission(path)
    
    # Print results
    print(results['feedback'])
    print(f"Score: {results['score']:.2f}%")
