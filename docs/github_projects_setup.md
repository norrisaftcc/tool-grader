# Setting Up GitHub Projects for Tool Grader

This guide walks through setting up a Kanban board using GitHub Projects for the Tool Grader repository.

## Creating the Project Board

1. Navigate to the [Tool Grader repository](https://github.com/norrisaftcc/tool-grader)
2. Click on the "Projects" tab
3. Click "New project"
4. Choose "Board" from the templates
5. Name the project "Tool Grader Development"
6. Click "Create"

## Configuring the Board

### Setting Up Columns

1. By default, you'll have "Todo," "In Progress," and "Done" columns
2. Click "+" to add additional columns
3. Set up the following columns in order:
   - **Backlog**
   - **Ready**
   - **In Progress**
   - **Testing**
   - **Done**

### Adding Custom Fields

Add the following custom fields to track additional information:

1. **Priority**
   - Click "+ Add field" → "Single select"
   - Name it "Priority"
   - Add options: "Low" (🟢), "Medium" (🟡), "High" (🔴)

2. **Epic**
   - Click "+ Add field" → "Single select"
   - Name it "Epic"
   - Add options based on major work areas:
     - "Core Infrastructure"
     - "Docker Setup"
     - "Canvas Integration"
     - "GitHub Integration"
     - "Testing"
     - "Security"
     - "UI Development"
     - "Content Development"
     - "Performance"
     - "DevOps"

3. **Sprint**
   - Click "+ Add field" → "Single select"
   - Name it "Sprint"
   - Add options:
     - "Sprint 1" (May 19 - June 2)
     - "Sprint 2" (June 3 - June 16)
     - "Sprint 3" (June 17 - June 30)

4. **Story Points**
   - Click "+ Add field" → "Number"
   - Name it "Story Points"

## Importing Tasks

To quickly populate the board with our predefined tasks:

1. In the Project view, click the "..." menu
2. Select "Import items"
3. Upload the `docs/tasks.csv` file
4. Map the columns to the appropriate fields
5. Click "Import"

## Automating Workflows

Set up some helpful automations to reduce manual work:

1. In the Project view, click "Workflows" in the toolbar
2. Set up the following automations:
   - When issues are closed, move to "Done"
   - When pull requests are merged, move to "Done"
   - When items are assigned, move to "In Progress" 
   - When draft pull requests are created, move to "In Progress"

## Linking Issues and Pull Requests

To get the most out of GitHub Projects:

1. Create GitHub Issues for each task on the board
2. When creating branches or PRs, reference the issue number (e.g., "#12")
3. Use the GitHub project board view when planning sprints
4. Reference the project in commit messages when applicable

## Recommended Views

Set up these saved views to help with project management:

1. **Kanban Board** (default)
   - Group by: Status
   - Sort by: Priority

2. **Sprint Planning**
   - Group by: Sprint
   - Sort by: Priority

3. **Epics View**
   - Group by: Epic
   - Sort by: Status

4. **By Assignee**
   - Group by: Assignee
   - Sort by: Status

## Best Practices

1. Update task status regularly to keep the board current
2. Add new tasks as GitHub Issues first, then add to the project
3. Use the "Convert to issue" feature for draft items
4. Review and update the board at least weekly
5. Use the board during standups and team meetings

## Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [GitHub Issues Documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
- [Project Planning Best Practices](https://github.blog/2022-02-11-10-github-features-every-developer-should-know/)