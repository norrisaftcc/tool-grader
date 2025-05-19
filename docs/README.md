# Python Autograder

A lightweight, secure Python assignment autograding system integrating GitHub Classroom and Canvas LMS.

## Overview

Python Autograder provides a simple, secure solution for automatically grading Python programming assignments. It connects GitHub Classroom repositories with Canvas LMS, enabling instructors to create programming assignments that can be automatically tested and graded with results seamlessly reported back to the Canvas gradebook.

### Key Features (MVP)

- GitHub Classroom integration for assignment distribution and collection
- Secure Docker-based execution environment for student code
- Canvas LMS integration for grade reporting
- Support for doctest-based grading criteria
- Simple webhook-based architecture for assignment submission processing

## Repository Structure

```
python-autograder/
├── .github/                    # GitHub CI/CD configurations
│   └── workflows/
│       └── ci.yml             # Basic CI pipeline
│
├── docker/                     # Docker configuration
│   ├── Dockerfile             # Base grading container
│   ├── entrypoint.sh          # Container entrypoint script
│   └── docker-compose.yml     # Local development setup
│
├── docs/                       # Documentation
│   ├── canvas_setup.md        # Canvas API setup instructions
│   └── github_setup.md        # GitHub Classroom setup guide
│
├── src/                        # Source code
│   ├── autograder/            # Main package
│   │   ├── __init__.py        
│   │   ├── config.py          # Configuration management
│   │   ├── canvas_api.py      # Canvas LMS integration
│   │   ├── github_api.py      # GitHub API client
│   │   ├── docker_runner.py   # Docker container management
│   │   ├── test_runner.py     # Test execution logic
│   │   └── grader.py          # Core grading logic
│   │
│   ├── webhook/               # Webhook service
│   │   ├── __init__.py
│   │   ├── app.py             # Flask web service
│   │   └── handlers.py        # Event handlers
│   │
│   └── cli/                   # Command line interface
│       ├── __init__.py
│       └── commands.py        # CLI commands
│
├── templates/                  # Templates for assignments & tests
│   ├── assignment_template/   # Basic assignment structure
│   │   ├── README.md
│   │   ├── .github/workflows/classroom.yml
│   │   └── tests/
│   │       └── test_sample.py
│   │
│   └── autograder_config.yml  # Example configuration
│
├── tests/                      # Tests for the autograder itself
│   ├── unit/
│   │   └── test_grader.py
│   │
│   └── integration/
│       └── test_workflow.py
│
├── .env.example                # Example environment variables
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── README.md                   # This file
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker
- Canvas LMS instance with API access
- GitHub account with Classroom access

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-org/python-autograder.git
   cd python-autograder
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy the example environment file and edit with your settings:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Build the Docker container:
   ```
   cd docker
   docker build -t python-autograder .
   ```

### Configuration

1. Set up Canvas API access (see `docs/canvas_setup.md`)
2. Configure GitHub Classroom (see `docs/github_setup.md`)
3. Configure webhook endpoint on GitHub or run in polling mode

## Basic Usage

### Creating an Assignment

1. Use the template in `templates/assignment_template/` as a starting point
2. Add your doctest-based test cases in Python files
3. Push to GitHub Classroom
4. Create corresponding assignment in Canvas

### Running the Autograder

#### Option 1: Webhook Mode (Recommended for production)

```
# Start the webhook service
python -m src.webhook.app
```

#### Option 2: Manual/CLI Mode (For testing)

```
# Grade a specific submission
python -m src.cli.commands grade --repo-url https://github.com/org/repo --assignment-id 12345
```

## Architecture

The autograder follows a simple flow:

1. Student pushes code to GitHub Classroom repository
2. GitHub webhook notifies autograder service
3. Autograder pulls student code from GitHub
4. Code is executed in a secure Docker container
5. Tests are run and results are collected
6. Grades and feedback are posted back to Canvas
7. Results are logged for instructor review

## Security Considerations

- All student code runs in isolated Docker containers
- Resource limits are enforced (CPU, memory, execution time)
- Network access is disabled during test execution
- Containers run with minimal permissions

## Future Roadmap

This MVP focuses on the core functionality with minimal features. Future enhancements include:

- Support for pytest-based testing
- LLM-generated test cases
- Student-authored tests
- Instructor dashboard
- Submission queue for handling high loads
- Comprehensive analytics
- Multiple language support

## Contributing

We welcome contributions! Please see our contributing guidelines before submitting a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was developed as a teaching tool for Python courses
- Special thanks to the GitHub Classroom and Canvas API teams