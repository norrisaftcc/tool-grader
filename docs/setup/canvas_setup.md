# Canvas API Setup Guide

This guide walks you through setting up Canvas API access for the Python Autograder.

## Prerequisites

- Admin or instructor access to your Canvas instance
- Canvas API token with appropriate permissions

## Step 1: Generate Canvas API Token

1. Log into your Canvas instance
2. Navigate to Account → Settings
3. Click on "+ New Access Token" under Approved Integrations
4. Name your token (e.g., "Python Autograder")
5. Set an expiration date if desired
6. Copy the generated token immediately (it won't be shown again)

## Step 2: Configure API Permissions

Ensure your API token has the following permissions:
- Read course information
- Read assignments
- Read submissions
- Update submission grades
- Add submission comments

## Step 3: Find Your Canvas URL

Your Canvas API base URL typically follows this format:
```
https://your-institution.instructure.com/api/v1/
```

## Step 4: Configure the Autograder

1. Copy the `.env.example` file to `.env`
2. Add your Canvas configuration:

```bash
CANVAS_API_TOKEN=your_canvas_api_token_here
CANVAS_API_URL=https://your-institution.instructure.com/api/v1/
CANVAS_COURSE_ID=your_course_id_here
```

## Step 5: Test Your Connection

Run the following command to verify your Canvas setup:

```bash
python -m src.cli.commands test-canvas
```

## Finding Canvas IDs

### Course ID
1. Navigate to your course in Canvas
2. Look at the URL: `https://canvas.example.com/courses/12345`
3. The course ID is `12345`

### Assignment ID
1. Navigate to the assignment in Canvas
2. Look at the URL: `https://canvas.example.com/courses/12345/assignments/67890`
3. The assignment ID is `67890`

## Troubleshooting

### Invalid API Token
- Ensure the token hasn't expired
- Verify you copied the entire token
- Check that the token has the necessary permissions

### Permission Denied
- Verify your account has instructor/admin privileges
- Ensure the API token has the required scopes

### Connection Issues
- Check your Canvas URL is correct
- Verify your institution's firewall allows API access
- Test with a simple curl command:
  ```bash
  curl -H "Authorization: Bearer YOUR_TOKEN" \
       https://your-canvas.instructure.com/api/v1/courses
  ```

## Security Best Practices

1. Never commit your API token to version control
2. Use environment variables for all sensitive data
3. Rotate API tokens regularly
4. Limit token permissions to only what's necessary
5. Monitor API usage through Canvas admin panel

## API Rate Limits

Canvas enforces rate limits on API requests:
- Default: 3,000 requests per hour
- Heavy endpoints: Lower limits may apply

The autograder implements exponential backoff to handle rate limiting gracefully.

## Next Steps

Once Canvas is configured, proceed to:
- [GitHub Classroom Setup](github_setup.md)
- [Creating Your First Assignment](../examples/readme-examples.md)