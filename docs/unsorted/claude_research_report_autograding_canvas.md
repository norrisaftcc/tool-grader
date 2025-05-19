# Python autograding system: Technically feasible with clear implementation path

A cloud-based autograding system integrating Canvas, GitHub, and containerized test execution is not only feasible within two semesters but has multiple successful precedents at educational institutions. The combination of GitHub Classroom's repository management, Docker's security isolation, and Canvas API's grade integration provides a proven architecture for delivering automatic feedback on Python assignments.

## The technology stack breakdown

**GitHub Classroom** offers the most direct path for assignment distribution and repository management, providing built-in autograding through GitHub Actions with three testing approaches:
- Input/output comparison tests
- Python test framework integration (pytest)
- Run command tests checking for successful execution

**Docker containers** emerge as the essential security layer, creating isolated environments that prevent student code from accessing system resources or persisting beyond the grading process. All successful educational autograding implementations use containerization to:
- Limit CPU, memory, and process usage
- Prevent network access during testing
- Run code with non-root permissions
- Enforce execution timeouts

**Canvas integration** requires working with their REST API, which provides comprehensive endpoints for:
- Fetching student submissions (via the GitHub repo links)
- Posting grades back to the gradebook
- Adding detailed feedback as submission comments

**Cloud hosting options** include:

| Provider | Key Services | Education Pricing |
|------------|--------------|-------------------|
| AWS | Lambda, ECS, Fargate | Up to 85% discount |
| Azure | Functions, Container Instances | Up to 90% discount |
| GCP | Cloud Run, GKE | Up to 80% discount |

The **testing framework** roadmap should follow a progressive complexity model:
1. Begin with doctest for simple validation (lowest barrier to entry)
2. Advance to pytest for more comprehensive checking
3. Introduce LLM-generated test cases to increase coverage

## Core implementation challenges

**Security isolation** requires multiple protective layers:
- Container boundary (Docker)
- Resource limits (memory, CPU, processes)
- Execution timeouts
- Network restrictions
- Non-root execution

**Integration complexity** emerges at the boundary points:
- Canvas OAuth authentication
- Webhook setup between GitHub and grading infrastructure 
- Persistence of grade data across systems

**Student experience** considerations include:
- Clear feedback on test failures
- Appropriate visibility of test cases
- Self-service testing before final submission

## Recommended implementation approach

A **hybrid architecture** balances security, performance, and student experience:

1. **GitHub Classroom** for assignment distribution and initial testing
2. **Custom grading service** deployed on cloud infrastructure for:
   - Running more comprehensive tests in isolated Docker containers
   - Processing submissions asynchronously via a queue
   - Reporting grades back to Canvas
   - Providing detailed feedback on test failures

This architecture provides the most flexibility while leveraging existing platforms for their strengths.

## Implementation timeline

### Phase 1: Prototype and Proof of Concept (2-3 months)
- Set up GitHub Classroom with basic autograding via GitHub Actions
- Create simple Docker container for Python assignment testing
- Implement Canvas API authentication and basic grade posting
- Test with simple assignments using doctest
- Proof of concept with 1-2 assignments in a small controlled environment

### Phase 2: Core Infrastructure (3-4 months)
- Develop queue-based submission processing system
- Improve Docker container security and resource management
- Create comprehensive pytest test suites for assignments
- Build webhook integration between GitHub and grading system
- Implement Canvas API grade reporting with detailed feedback
- Deploy basic system for broader internal testing

### Phase 3: Enhanced Features (2-3 months)
- Add LLM-generated test capabilities
- Implement student-facing test execution environment
- Create instructor dashboard for monitoring submissions
- Add performance optimization for high-volume periods
- Fine-tune feedback mechanisms based on student experience
- Prepare documentation and training materials

### Phase 4: Pilot Launch (1-2 months)
- Deploy to production environment
- Conduct pilot with selected Python courses
- Collect feedback and make adjustments
- Scale resources based on actual usage patterns
- Create sustainability plan for ongoing maintenance

## Existing systems to learn from

Several established systems provide valuable templates:

1. **Otter Grader** (UC Berkeley): Modular Python-based framework with strong data science focus

2. **GitHub Classroom Autograder**: Native GitHub Actions integration but limited test visibility control

3. **CodeGrade**: Commercial platform with deep Canvas LTI integration and comprehensive testing options

4. **Gradescope**: Established platform with Docker-based execution and multiple testing frameworks

The most successful implementations share key characteristics:
- Containerized testing environments
- Graduated test complexity (simple tests first, comprehensive tests later)
- Clear feedback mechanisms
- Balanced security and usability

## Key recommendations 

1. **Start with GitHub Classroom's native autograding** for the simplest assignments, then extend capabilities with custom infrastructure.

2. **Use AWS as the cloud platform** due to:
   - Educational discounts
   - Lambda for simple tests
   - ECS/Fargate for complex testing environments
   - SQS for submission queueing

3. **Implement a three-layer testing approach**:
   - Public tests students can run locally
   - Basic tests that run on every submission
   - Comprehensive hidden tests for final grading

4. **Build a queue-based architecture** to handle submission spikes near deadlines.

5. **Develop clear, actionable feedback** mechanisms to maximize educational value.

The implementation timeline of two semesters is realistic for a functional pilot system, particularly if prioritizing core functionality first and adding advanced features incrementally.

## Next steps

1. Create a detailed requirements document specifying exactly what functionality is needed for the pilot

2. Set up development environments with GitHub Classroom integration

3. Build a prototype Docker container for running Python tests securely

4. Implement basic Canvas API integration for retrieving assignments and posting grades

5. Develop a small pilot assignment to test the end-to-end workflow

With careful planning and a phased approach, this autograding system is not only feasible but could significantly enhance the educational experience for both Python students and instructors.