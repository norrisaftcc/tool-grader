# Python Autograder Documentation

Welcome to the Python Autograder documentation. This system provides automated grading for Python assignments through GitHub Classroom and Canvas LMS integration.

## Quick Start

1. [Setup Canvas API Access](setup/canvas_setup.md)
2. [Configure GitHub Classroom](setup/github_setup.md)
3. [Create Your First Assignment](examples/readme-examples.md)
4. [Run the Autograder](README.md#basic-usage)

## Documentation Structure

### [Architecture](architecture/)
- [Research Report](architecture/research_report.md) - Technical feasibility study
- System design and architecture decisions
- Security considerations

### [Setup Guides](setup/)
- [Canvas API Setup](setup/canvas_setup.md)
- [GitHub Classroom Setup](setup/github_setup.md)
- Environment configuration

### [Examples](examples/)
- [Configuration Examples](examples/python-autograder-config.md)
- [Dockerfile Example](examples/python-autograder-dockerfile.txt)
- [Test Runner Implementation](examples/python-autograder-test-runner.py)
- [Assignment Examples](examples/readme-examples.md)

### [API Documentation](api/)
- [API Overview](api/README.md)
- Canvas API integration
- GitHub API integration
- Webhook endpoints

### [Development](development/)
- [Development Guide](development/README.md)
- Testing guidelines
- Contribution workflow
- Debugging tips

## Key Features

- **Secure Execution**: Docker containers isolate student code
- **Automatic Grading**: Doctest-based evaluation
- **LMS Integration**: Seamless Canvas grade posting
- **GitHub Integration**: Works with GitHub Classroom
- **Scalable**: Queue-based architecture handles peak loads

## System Requirements

- Python 3.8+
- Docker
- Canvas LMS with API access
- GitHub organization with Classroom enabled

## Getting Help

- Check the [Troubleshooting Guide](development/README.md#troubleshooting)
- Review [Common Issues](setup/canvas_setup.md#troubleshooting)
- Submit issues on GitHub

## Contributing

See our [Development Guide](development/README.md) for information on:
- Setting up a development environment
- Code style guidelines
- Testing requirements
- Pull request process

## License

This project is licensed under the MIT License - see the LICENSE file for details.