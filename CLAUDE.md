# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tool Grader is a Python autograding system designed to integrate GitHub Classroom assignments with Canvas LMS for automatic grading of student submissions. It uses Docker containers for secure code execution and doctest for evaluating Python assignments.

## Architecture

The system follows a webhook-based architecture:
1. Students push code to GitHub Classroom repositories
2. GitHub webhooks notify the autograder service
3. Student code is pulled and executed in secure Docker containers
4. Test results are collected using doctest
5. Grades and feedback are posted back to Canvas LMS

## Development Commands

### Docker Management
```bash
# Build the autograder container
cd docker
docker build -t python-autograder .

# Run docker-compose for local development
docker-compose up
```

### Python Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Setup package
pip install -e .
```

### Running the Autograder
```bash
# Start webhook service (production mode)
python -m src.webhook.app

# Manual grading via CLI
python -m src.cli.commands grade --repo-url <github-url> --assignment-id <canvas-id>

# Test the Docker runner directly
python -m src.autograder.test_runner <path-to-student-code>
```

### Testing
```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality
```bash
# Format code with black
black src tests

# Lint with flake8
flake8 src tests

# Type checking
mypy src
```

## Repository Structure

```
tool-grader/
├── src/                    # Source code
│   ├── autograder/        # Core grading logic
│   ├── webhook/           # Webhook service
│   └── cli/               # Command-line interface
├── tests/                  # Test suite
├── docker/                 # Docker configuration
├── docs/                   # Documentation
│   ├── architecture/      # System design docs
│   ├── setup/            # Setup guides
│   ├── api/              # API documentation
│   ├── development/      # Development guides
│   └── examples/         # Example configurations
├── templates/             # Assignment templates
└── CLAUDE.md             # This file
```

## Key Components

### Core Modules
- `src/autograder/`: Main autograding logic
  - `config.py`: Configuration management
  - `canvas_api.py`: Canvas LMS integration
  - `github_api.py`: GitHub API client
  - `docker_runner.py`: Docker container management
  - `test_runner.py`: Doctest execution and result collection
  - `grader.py`: Core grading orchestration

### Webhook Service
- `src/webhook/`: Flask-based webhook handler
  - `app.py`: Flask application setup
  - `handlers.py`: GitHub webhook event processing

### CLI Interface
- `src/cli/`: Command-line tools
  - `commands.py`: CLI commands for manual operations

## Security Considerations

All student code runs with these security measures:
- Isolated Docker containers
- Resource limits (CPU, memory, execution time)
- Network access disabled during execution
- Non-root user execution
- Minimal container capabilities

## Configuration

The system uses environment variables and YAML configuration files:
- `.env`: API keys and service endpoints
- `autograder_config.yml`: Assignment-specific settings
  - Test parameters
  - Resource limits
  - Canvas integration settings
  - Feedback options

## Documentation

- [Main Documentation](docs/index.md)
- [Architecture Overview](docs/architecture/research_report.md)
- [Canvas Setup Guide](docs/setup/canvas_setup.md)
- [GitHub Setup Guide](docs/setup/github_setup.md)
- [Development Guide](docs/development/README.md)
- [API Documentation](docs/api/README.md)