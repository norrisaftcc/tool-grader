"""
Configuration Management for Tool Grader

This module handles loading and validating configuration from various sources:
- Environment variables
- Configuration files
- Default values
"""

import os
import yaml
from pathlib import Path


class Config:
    """Configuration manager for Tool Grader."""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        "docker": {
            "image": "python-autograder:latest",
            "memory_limit": "256m",
            "cpu_limit": 0.5,
            "timeout": 30
        },
        "grading": {
            "show_test_names": True,
            "show_expected_output": True,
            "show_test_docstrings": True,
            "show_full_traceback": False
        },
        "canvas": {
            "post_grades": False,
            "post_feedback": False,
            "update_existing": True,
            "feedback_format": "markdown"
        }
    }
    
    def __init__(self, config_path=None):
        """
        Initialize configuration from multiple sources.
        
        Args:
            config_path: Optional path to configuration file
        """
        # Start with default configuration
        self.config = self.DEFAULT_CONFIG.copy()
        
        # Load configuration from file if provided
        if config_path:
            self._load_from_file(config_path)
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_file(self, config_path):
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
        """
        path = Path(config_path)
        if not path.exists():
            return
        
        try:
            with open(path, 'r') as f:
                file_config = yaml.safe_load(f)
                
            # Update configuration with file values
            if file_config:
                for section, values in file_config.items():
                    if section in self.config:
                        self.config[section].update(values)
                    else:
                        self.config[section] = values
        except Exception as e:
            print(f"Error loading configuration from {config_path}: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Docker configuration
        if os.environ.get('DOCKER_IMAGE'):
            self.config['docker']['image'] = os.environ.get('DOCKER_IMAGE')
        if os.environ.get('DOCKER_MEMORY_LIMIT'):
            self.config['docker']['memory_limit'] = os.environ.get('DOCKER_MEMORY_LIMIT')
        if os.environ.get('DOCKER_CPU_LIMIT'):
            self.config['docker']['cpu_limit'] = float(os.environ.get('DOCKER_CPU_LIMIT', 0.5))
        if os.environ.get('DOCKER_TIMEOUT'):
            self.config['docker']['timeout'] = int(os.environ.get('DOCKER_TIMEOUT', 30))
        
        # Canvas API configuration
        if os.environ.get('CANVAS_API_TOKEN'):
            if 'canvas_api' not in self.config:
                self.config['canvas_api'] = {}
            self.config['canvas_api']['token'] = os.environ.get('CANVAS_API_TOKEN')
        if os.environ.get('CANVAS_API_URL'):
            if 'canvas_api' not in self.config:
                self.config['canvas_api'] = {}
            self.config['canvas_api']['url'] = os.environ.get('CANVAS_API_URL')
        if os.environ.get('CANVAS_COURSE_ID'):
            if 'canvas_api' not in self.config:
                self.config['canvas_api'] = {}
            self.config['canvas_api']['course_id'] = os.environ.get('CANVAS_COURSE_ID')
        
        # GitHub API configuration
        if os.environ.get('GITHUB_TOKEN'):
            if 'github_api' not in self.config:
                self.config['github_api'] = {}
            self.config['github_api']['token'] = os.environ.get('GITHUB_TOKEN')
        if os.environ.get('GITHUB_WEBHOOK_SECRET'):
            if 'github_api' not in self.config:
                self.config['github_api'] = {}
            self.config['github_api']['webhook_secret'] = os.environ.get('GITHUB_WEBHOOK_SECRET')
        if os.environ.get('GITHUB_ORG'):
            if 'github_api' not in self.config:
                self.config['github_api'] = {}
            self.config['github_api']['org'] = os.environ.get('GITHUB_ORG')
    
    def get(self, section, key=None, default=None):
        """
        Get configuration value(s).
        
        Args:
            section: Configuration section
            key: Optional key within section
            default: Default value if key not found
            
        Returns:
            Configuration value or section dict
        """
        if section not in self.config:
            return {} if key is None else default
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key, default)
    
    def set(self, section, key, value):
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Key within section
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value


# Global configuration instance
config = Config()


def load_config(config_path=None):
    """
    Load configuration from file or environment.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Config instance
    """
    global config
    config = Config(config_path)
    return config


def get_config():
    """
    Get the current configuration instance.
    
    Returns:
        Config instance
    """
    global config
    return config