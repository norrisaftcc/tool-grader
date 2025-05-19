# Tool Grader Kanban Board

This file serves as a simple Markdown-based Kanban board for tracking project tasks. For a more interactive experience, please use the GitHub Projects interface.

## GitHub Projects Setup (Recommended)

To set up a proper Kanban board using GitHub Projects:

1. Go to the [tool-grader repository](https://github.com/norrisaftcc/tool-grader)
2. Click on the "Projects" tab
3. Click "New project"
4. Choose "Board" from the templates
5. Name the project "Tool Grader Development"
6. Click "Create"

Once created, set up the following columns:
- **Backlog**: Tasks that need to be done but aren't actively being worked on yet
- **Ready**: Tasks that are ready to be picked up
- **In Progress**: Tasks that are currently being worked on
- **Testing**: Tasks that are completed but need verification
- **Done**: Completed tasks

You can then populate the board with issues from the repository.

## Simple Markdown Kanban (Alternative)

Below is a simplified Kanban board in Markdown format:

### 📋 Backlog

- Set up Docker containerization
  - Create Dockerfile based on examples
  - Configure resource limits
  - Test security isolation
- Implement Canvas API integration
  - Set up authentication
  - Create grade submission endpoint
  - Test with sample courses
- Implement GitHub integration
  - Set up webhooks
  - Create repository fetching mechanisms
  - Test with sample repositories
- Create additional test assignments
  - Add data structures examples
  - Create loop-focused problems
  - Add file I/O examples

### 🔍 Ready

- Set up project structure as per docs/README.md
- Create src/autograder/ package with basic modules
- Set up pytest framework for testing

### 🏗️ In Progress

- Improve MVP demo with additional assignments
- Document autograder architecture in detail
- Create webhook handlers

### 🧪 Testing

- Test functions assignment with multiple student examples
- Validate receipt calculation logic
- Test rectangle comparison doctest evaluation

### ✅ Done

- Create CLAUDE.md for AI guidance
- Organize documentation structure
- Create MVP demo with local folder-based grading
- Convert CSC-134 assignments to Python
- Create project meeting notes

## Next Actions

1. Prioritize Docker containerization as the next major feature
2. Set up GitHub Projects for better task tracking
3. Focus on implementing core autograder logic
4. Begin working on Canvas API integration

## Development Sprints

### Sprint 1 (May 19 - June 2, 2025)
- Complete MVP demo ✅
- Organize documentation ✅
- Set up basic project structure
- Begin Docker implementation

### Sprint 2 (June 3 - June 16, 2025)
- Complete Docker implementation
- Create GitHub webhook handler
- Begin Canvas API integration
- Expand test suite

### Sprint 3 (June 17 - June 30, 2025)
- Complete Canvas integration
- Implement end-to-end workflow
- Create admin interface
- Add advanced test features