# TODO List for Tool Grader

## Documentation & Setup
- [x] Create CLAUDE.md for AI guidance
- [x] Organize documentation structure from `/docs/unsorted`
- [x] Create missing setup guides (Canvas, GitHub)
- [x] Create development documentation
- [x] Create API documentation structure

## MVP Demo Implementation
- [x] Create simple demo of the system
  - [x] Use local folders for grading (without external integrations)
  - [x] Make grading portion visible for testing
  - [x] Create example student submissions
  - [x] Demonstrate doctest evaluation

## Core Infrastructure
- [ ] Set up basic project structure as per docs/README.md
- [ ] Create src/autograder/ package
  - [ ] config.py - Configuration management
  - [ ] canvas_api.py - Canvas LMS integration (using https://pypi.org/project/canvasapi/#documentation)
  - [ ] github_api.py - GitHub API client
  - [ ] docker_runner.py - Docker container management
  - [ ] test_runner.py - Doctest execution (example exists in docs/examples/)
  - [ ] grader.py - Core grading logic
- [ ] Create src/webhook/ package
  - [ ] app.py - Flask web service
  - [ ] handlers.py - Event handlers
- [ ] Create src/cli/ package
  - [ ] commands.py - CLI commands

## Docker Setup
- [ ] Create docker/Dockerfile (example in docs/examples/)
- [ ] Create docker/entrypoint.sh (example in docs/examples/)
- [ ] Create docker-compose.yml for local development
- [ ] Test container security and resource limits

## Templates
- [ ] Create assignment templates structure
- [ ] Add example assignment configurations
- [ ] Create GitHub Classroom workflow templates

## Testing
- [ ] Set up pytest framework
- [ ] Create unit tests for core modules
- [ ] Create integration tests
- [ ] Add CI/CD pipeline

## External Integrations
- [ ] Canvas API integration using canvasapi library
- [ ] GitHub API integration
- [ ] Webhook setup and security

## Security
- [ ] Implement Docker security measures
- [ ] Add input validation
- [ ] Set up secrets management
- [ ] Configure rate limiting

## Future Enhancements
- [ ] Support for pytest testing
- [ ] LLM-generated test cases
- [ ] Student dashboard
- [ ] Instructor analytics
- [ ] Queue-based submission processing

## Notes
- Canvas API documentation: https://pypi.org/project/canvasapi/#documentation
- Use existing example files in docs/examples/ as reference
- Follow the architecture described in docs/architecture/research_report.md