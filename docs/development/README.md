# Development Guide

This guide covers development practices for the Python Autograder project.

## Getting Started

### Prerequisites
- Python 3.8+
- Docker
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/tool-grader.git
   cd tool-grader
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install package in development mode
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Build Docker image:
   ```bash
   cd docker
   docker build -t python-autograder .
   ```

## Project Structure

```
tool-grader/
├── src/                    # Source code
│   ├── autograder/        # Core grading logic
│   ├── webhook/           # Webhook service
│   └── cli/               # Command-line interface
├── tests/                  # Test suite
├── docker/                 # Docker configuration
├── docs/                   # Documentation
└── templates/             # Assignment templates
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_grader.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests
pytest tests/integration/
```

### Writing Tests

Follow these conventions:
- Use pytest for all tests
- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Mock external services (Canvas, GitHub)
- Aim for >80% test coverage

Example test:
```python
def test_grade_submission(mock_docker):
    """Test grading a student submission."""
    grader = Grader()
    result = grader.grade_submission("path/to/code")
    assert result.score == 100
    assert result.feedback is not None
```

## Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable names

### Tools
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking
- `isort` for import sorting

Run all checks:
```bash
make lint  # or manually:
black src tests
flake8 src tests
mypy src
isort src tests
```

## Docker Development

### Building Images

```bash
# Build development image
docker build -f docker/Dockerfile.dev -t autograder-dev .

# Build production image
docker build -f docker/Dockerfile -t autograder:latest .
```

### Testing Container Security

```bash
# Run security scan
docker scan autograder:latest

# Test resource limits
docker run --memory="256m" --cpus="0.5" autograder:latest
```

## Debugging

### Local Debugging
1. Use VS Code or PyCharm debugger
2. Add breakpoints in code
3. Run in debug mode

### Container Debugging
```bash
# Run container with shell
docker run -it --entrypoint /bin/bash autograder:latest

# View container logs
docker logs <container-id>

# Inspect running container
docker exec -it <container-id> /bin/bash
```

### Webhook Debugging
Use ngrok for local webhook testing:
```bash
ngrok http 5000
# Use the ngrok URL in GitHub webhook settings
```

## Contributing

### Git Workflow

1. Create feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

3. Push and create PR:
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description if needed

### Pull Request Guidelines
1. Update tests for new features
2. Update documentation
3. Ensure CI passes
4. Request review from maintainers

## Performance Optimization

### Profiling
```python
import cProfile
import pstats

# Profile code execution
cProfile.run('grader.grade_submission()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization Tips
- Cache Canvas API responses
- Reuse Docker containers when possible
- Implement connection pooling
- Use async operations for I/O

## Security Considerations

### Code Security
- Never commit secrets
- Use environment variables
- Implement rate limiting
- Validate all inputs
- Use parameterized queries

### Container Security
- Run as non-root user
- Drop unnecessary capabilities
- Disable network access during grading
- Set resource limits
- Use security scanning tools

## Monitoring

### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Starting grade process")
logger.error("Failed to connect to Canvas", exc_info=True)
```

### Metrics
Track these key metrics:
- Grading time per submission
- API call rates
- Error rates
- Container resource usage

## Deployment

See [Deployment Guide](deployment.md) for production deployment instructions.

## Troubleshooting

Common issues and solutions:

### Docker Build Fails
- Check Dockerfile syntax
- Verify base image exists
- Clear Docker cache: `docker builder prune`

### API Connection Issues
- Verify credentials in `.env`
- Check network connectivity
- Review API rate limits

### Memory Issues
- Increase container memory limits
- Optimize code for memory usage
- Implement garbage collection

## Resources

- [Python Best Practices](https://docs.python-guide.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Canvas API Reference](https://canvas.instructure.com/doc/api/)
- [GitHub API Documentation](https://docs.github.com/en/rest)