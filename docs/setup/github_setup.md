# GitHub Classroom Setup Guide

This guide walks you through setting up GitHub Classroom integration for the Python Autograder.

## Prerequisites

- GitHub account with organization access
- GitHub Classroom enabled for your organization
- GitHub personal access token or GitHub App

## Step 1: Create a GitHub Organization

1. Go to https://github.com/organizations/new
2. Choose the free plan for educational use
3. Name your organization (e.g., "cs101-fall-2025")
4. Invite co-instructors if needed

## Step 2: Enable GitHub Classroom

1. Visit https://classroom.github.com
2. Click "Sign in with GitHub"
3. Select your organization
4. Follow the setup wizard

## Step 3: Generate GitHub Access Token

### Option A: Personal Access Token (Simpler)

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Name it "Python Autograder"
4. Select these scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
   - `read:org` (Read org and team membership)
5. Copy the generated token

### Option B: GitHub App (More Secure, Advanced)

1. Go to your organization settings
2. Navigate to Developer settings → GitHub Apps
3. Create a new GitHub App with:
   - Repository permissions: Read & Write
   - Organization permissions: Read
   - Webhook permissions as needed

## Step 4: Configure Webhooks

1. In your GitHub organization settings
2. Go to Webhooks → Add webhook
3. Set the payload URL to your autograder endpoint:
   ```
   https://your-autograder.com/webhook/github
   ```
4. Content type: `application/json`
5. Secret: Generate a secure secret and save it
6. Select events:
   - Push events
   - Pull request events (optional)

## Step 5: Configure the Autograder

Update your `.env` file:

```bash
GITHUB_TOKEN=your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
GITHUB_ORG=your-organization-name
```

## Step 6: Create Assignment Template

1. Create a new repository in your organization
2. Name it with `-template` suffix (e.g., `python-functions-template`)
3. Add starter code and test files
4. Include `.github/workflows/classroom.yml`:

```yaml
name: GitHub Classroom Workflow

on: 
  push:
    branches: [ main ]

jobs:
  run-autograding-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: education/autograding@v1
```

## Step 7: Create an Assignment

1. Go to https://classroom.github.com
2. Click "New assignment"
3. Configure assignment settings:
   - Title: "Python Functions Assignment"
   - Repository prefix: "python-functions"
   - Visibility: Private
   - Template repository: Select your template
4. Enable autograding tests
5. Add test cases

## Step 8: Test the Integration

1. Accept the assignment as a test student
2. Push code to trigger autograding
3. Verify webhook delivery in GitHub settings
4. Check autograder logs

## Configuring Autograding Tests

### Basic Test Configuration

Create `.github/classroom/autograding.json`:

```json
{
  "tests": [
    {
      "name": "Test add function",
      "setup": "",
      "run": "python -m doctest functions.py",
      "input": "",
      "output": "",
      "comparison": "included",
      "timeout": 60,
      "points": 25
    }
  ]
}
```

### Python-Specific Tests

For doctest-based grading:

```json
{
  "tests": [
    {
      "name": "Doctest validation",
      "run": "python -m doctest -v *.py",
      "timeout": 30,
      "points": 100
    }
  ]
}
```

## Security Considerations

1. Use repository secrets for sensitive data
2. Limit token permissions to minimum required
3. Rotate tokens regularly
4. Use webhook secrets for verification
5. Enable two-factor authentication

## Troubleshooting

### Webhook Not Firing
- Check webhook configuration in GitHub
- Verify payload URL is accessible
- Check webhook recent deliveries for errors

### Permission Denied
- Verify token has correct scopes
- Check organization permissions
- Ensure repository access is granted

### Assignment Not Created
- Verify template repository exists
- Check organization quotas
- Ensure GitHub Classroom is enabled

## Best Practices

1. Use semantic versioning for templates
2. Test assignments before releasing to students
3. Document expected behavior clearly
4. Provide example solutions separately
5. Use branch protection rules

## Integration with Canvas

To link GitHub Classroom with Canvas:

1. Use external tool (LTI) integration
2. Add assignment links to Canvas
3. Configure grade passback if available

## Next Steps

- [Canvas Setup](canvas_setup.md)
- [Creating Your First Assignment](../examples/readme-examples.md)
- [Configuring Docker Environment](../examples/python-autograder-dockerfile.txt)