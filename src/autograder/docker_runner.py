"""
Docker Container Management for Tool Grader

This module handles running code in Docker containers for secure execution.
"""

import os
import tempfile
import json
import logging
from pathlib import Path

import docker
from docker.errors import ContainerError, ImageNotFound

from .config import get_config

# Set up logging
logger = logging.getLogger(__name__)


class DockerRunner:
    """Runs code in Docker containers for security and isolation."""
    
    def __init__(
        self,
        docker_image=None,
        memory_limit=None,
        cpu_limit=None,
        timeout=None
    ):
        """
        Initialize the Docker runner.
        
        Args:
            docker_image: Name of the Docker image to use
            memory_limit: Memory limit for the container
            cpu_limit: CPU limit for the container
            timeout: Timeout in seconds
        """
        config = get_config()
        
        self.docker_image = docker_image or config.get("docker", "image")
        self.memory_limit = memory_limit or config.get("docker", "memory_limit")
        self.cpu_limit = cpu_limit or config.get("docker", "cpu_limit")
        self.timeout = timeout or config.get("docker", "timeout")
        
        self.client = docker.from_env()
        
        # Verify the Docker image exists
        try:
            self.client.images.get(self.docker_image)
        except ImageNotFound:
            logger.error(f"Docker image '{self.docker_image}' not found. Did you build it?")
            raise
    
    def run_doctest(self, code_path, module_name=None):
        """
        Run doctest on code inside a Docker container.
        
        Args:
            code_path: Path to directory containing code
            module_name: Optional specific module to test
            
        Returns:
            Dict containing test results
        """
        code_path = Path(code_path)
        
        # Create temporary directory for results
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            results_file = temp_path / "results.json"
            
            # Prepare volumes to mount in container
            volumes = {
                str(code_path.absolute()): {
                    'bind': '/code',
                    'mode': 'ro'  # read-only
                },
                str(temp_path.absolute()): {
                    'bind': '/results',
                    'mode': 'rw'  # read-write for output
                }
            }
            
            # Prepare environment variables
            environment = {}
            if module_name:
                environment["SUBMISSION_FILE"] = f"/code/{module_name}"
            
            try:
                # Run container with resource constraints
                container = self.client.containers.run(
                    image=self.docker_image,
                    volumes=volumes,
                    working_dir="/code",
                    mem_limit=self.memory_limit,
                    cpu_quota=int(100000 * self.cpu_limit),  # Docker uses microseconds
                    network_mode="none",  # No network access
                    cap_drop=["ALL"],     # Drop all capabilities
                    security_opt=["no-new-privileges:true"],
                    environment=environment,
                    command=f"python -c 'import doctest, json, sys; import importlib.util; module_name = \"{module_name or 'main'}\"; spec = importlib.util.spec_from_file_location(module_name, \"/code/{module_name or '*.py'}\"); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); result = doctest.testmod(module, verbose=True); json.dump({{'attempted': result.attempted, 'failed': result.failed}}, open(\"/results/results.json\", \"w\"))'",
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
                    
                    return {
                        'success': results.get('failed', 0) == 0,
                        'attempted': results.get('attempted', 0),
                        'failed': results.get('failed', 0),
                        'output': container_logs
                    }
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


if __name__ == "__main__":
    """Simple CLI for testing."""
    import argparse
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Run code in Docker container")
    parser.add_argument("path", help="Path to code directory")
    parser.add_argument("--module", help="Specific module to test")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds")
    
    args = parser.parse_args()
    
    # Create Docker runner
    runner = DockerRunner(timeout=args.timeout)
    
    # Run doctest
    results = runner.run_doctest(args.path, args.module)
    
    # Print results
    print(json.dumps(results, indent=2))