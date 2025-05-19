"""
Unit tests for the config module.
"""

import os
import tempfile
import yaml

import pytest

from autograder.config import Config, load_config, get_config


def test_default_config():
    """Test loading default configuration."""
    config = Config()
    
    # Check that default values are loaded
    assert config.get("docker", "image") == "python-autograder:latest"
    assert config.get("docker", "memory_limit") == "256m"
    assert config.get("docker", "cpu_limit") == 0.5
    assert config.get("docker", "timeout") == 30


def test_config_from_file():
    """Test loading configuration from a file."""
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as temp_file:
        # Write test configuration
        yaml.dump({
            "docker": {
                "image": "test-image:latest",
                "memory_limit": "512m"
            }
        }, temp_file)
        temp_file.flush()
        
        # Load configuration from file
        config = Config(temp_file.name)
        
        # Check that file values override defaults
        assert config.get("docker", "image") == "test-image:latest"
        assert config.get("docker", "memory_limit") == "512m"
        
        # Check that other defaults are preserved
        assert config.get("docker", "cpu_limit") == 0.5
        assert config.get("docker", "timeout") == 30


def test_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    # Set environment variables
    monkeypatch.setenv("DOCKER_IMAGE", "env-image:latest")
    monkeypatch.setenv("DOCKER_MEMORY_LIMIT", "1g")
    monkeypatch.setenv("CANVAS_API_TOKEN", "test-token")
    
    # Load configuration
    config = Config()
    
    # Check that environment values override defaults
    assert config.get("docker", "image") == "env-image:latest"
    assert config.get("docker", "memory_limit") == "1g"
    assert config.get("canvas_api", "token") == "test-token"
    
    # Check that other defaults are preserved
    assert config.get("docker", "cpu_limit") == 0.5
    assert config.get("docker", "timeout") == 30


def test_config_precedence(monkeypatch):
    """Test configuration loading precedence."""
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as temp_file:
        # Write test configuration
        yaml.dump({
            "docker": {
                "image": "file-image:latest",
                "memory_limit": "512m",
                "cpu_limit": 0.25
            }
        }, temp_file)
        temp_file.flush()
        
        # Set environment variables
        monkeypatch.setenv("DOCKER_IMAGE", "env-image:latest")
        
        # Load configuration
        config = Config(temp_file.name)
        
        # Check precedence: env > file > default
        assert config.get("docker", "image") == "env-image:latest"  # From env
        assert config.get("docker", "memory_limit") == "512m"  # From file
        assert config.get("docker", "cpu_limit") == 0.25  # From file
        assert config.get("docker", "timeout") == 30  # Default


def test_get_set_config():
    """Test getting and setting configuration values."""
    config = Config()
    
    # Set a value
    config.set("test", "key", "value")
    
    # Get the value
    assert config.get("test", "key") == "value"
    
    # Get a section
    assert config.get("test") == {"key": "value"}
    
    # Get a default value
    assert config.get("test", "nonexistent", "default") == "default"
    
    # Get a nonexistent section
    assert config.get("nonexistent") == {}


def test_load_get_config():
    """Test loading and getting global configuration."""
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml") as temp_file:
        # Write test configuration
        yaml.dump({
            "test": {
                "key": "value"
            }
        }, temp_file)
        temp_file.flush()
        
        # Load global configuration
        load_config(temp_file.name)
        
        # Get global configuration
        config = get_config()
        
        # Check that configuration is loaded
        assert config.get("test", "key") == "value"