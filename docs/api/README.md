# API Documentation

This directory contains API documentation for the Python Autograder system.

## Available APIs

### Canvas API Integration
- [Canvas API Reference](canvas_api.md)
- Grade posting endpoints
- Assignment retrieval methods

### GitHub API Integration  
- [GitHub API Reference](github_api.md)
- Repository access methods
- Webhook event handling

### Webhook API
- [Webhook Endpoints](webhook_api.md)
- Event payload formats
- Security and authentication

### Internal APIs
- [Grader API](grader_api.md)
- [Docker Runner API](docker_api.md)
- [Test Runner API](test_runner_api.md)

## API Standards

All APIs follow these conventions:
- RESTful design principles
- JSON request/response format
- Standard HTTP status codes
- Bearer token authentication where applicable

## Error Handling

All APIs return errors in this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

## Rate Limiting

External API calls are rate-limited:
- Canvas API: 3,000 requests/hour
- GitHub API: 5,000 requests/hour (authenticated)
- Webhook endpoints: 100 requests/minute