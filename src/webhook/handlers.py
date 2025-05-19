"""
Webhook Event Handlers for Tool Grader

This module provides handlers for GitHub webhook events.
"""

import os
import tempfile
import subprocess
import re
from pathlib import Path
import logging

from autograder.config import get_config

# Set up logging
logger = logging.getLogger(__name__)


def handle_push_event(payload):
    """
    Handle GitHub push event.
    
    Args:
        payload: GitHub webhook payload
    
    Returns:
        Dictionary with processing result
    """
    # Extract repository information
    repo_name = payload.get("repository", {}).get("full_name")
    if not repo_name:
        return {
            "status": "error",
            "message": "Repository name not found in payload"
        }
    
    # Extract branch information
    ref = payload.get("ref")
    if not ref:
        return {
            "status": "error",
            "message": "Branch reference not found in payload"
        }
    
    # Check if this is a branch we care about
    branch = ref.replace("refs/heads/", "")
    
    logger.info(f"Received push event for {repo_name} on {branch}")
    
    # Check if this is a student repository
    if not _is_student_repository(repo_name):
        return {
            "status": "skipped",
            "message": f"Not a student repository: {repo_name}"
        }
    
    # Clone repository to temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone repository
        clone_result = _clone_repository(repo_name, temp_dir)
        if "error" in clone_result:
            return clone_result
        
        # Find assignment configuration
        assignment_config = _find_assignment_config(temp_dir)
        if not assignment_config:
            return {
                "status": "error",
                "message": "Assignment configuration not found"
            }
        
        # TODO: Process submission
        # For now, just return success
        return {
            "status": "success",
            "message": f"Processed push event for {repo_name} on {branch}",
            "repository": repo_name,
            "branch": branch
        }


def _is_student_repository(repo_name):
    """
    Check if a repository is a student submission.
    
    Args:
        repo_name: Repository name
    
    Returns:
        True if repository is a student submission, False otherwise
    """
    # TODO: Implement actual check
    # For now, just check if repository name matches pattern
    config = get_config()
    pattern = config.get("github", "repository_pattern", "")
    
    if pattern:
        return re.match(pattern, repo_name) is not None
    
    # Default to True for testing
    return True


def _clone_repository(repo_name, target_dir):
    """
    Clone a GitHub repository.
    
    Args:
        repo_name: Repository name (org/repo)
        target_dir: Target directory
    
    Returns:
        Dictionary with cloning result
    """
    # Get GitHub token from configuration
    config = get_config()
    github_token = config.get("github_api", "token")
    
    # Construct clone URL
    if github_token:
        clone_url = f"https://{github_token}@github.com/{repo_name}.git"
    else:
        clone_url = f"https://github.com/{repo_name}.git"
    
    try:
        # Clone the repository
        subprocess.run(
            ["git", "clone", clone_url, target_dir],
            check=True,
            capture_output=True,
            text=True
        )
        
        return {
            "status": "success",
            "message": f"Cloned repository {repo_name}"
        }
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone repository {repo_name}: {e}")
        return {
            "status": "error",
            "message": f"Failed to clone repository: {e.stderr}"
        }


def _find_assignment_config(repo_dir):
    """
    Find assignment configuration in repository.
    
    Args:
        repo_dir: Repository directory
    
    Returns:
        Path to assignment configuration file, or None if not found
    """
    # Check for common configuration file locations
    config_paths = [
        Path(repo_dir) / ".github" / "classroom" / "autograding.json",
        Path(repo_dir) / "autograder_config.yml",
        Path(repo_dir) / "autograder_config.yaml",
        Path(repo_dir) / "autograder_config.json",
    ]
    
    for path in config_paths:
        if path.exists():
            return path
    
    return None