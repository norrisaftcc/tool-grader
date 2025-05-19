"""
Canvas LMS API Integration for Tool Grader

This module handles integration with the Canvas LMS API for grade reporting.
"""

import logging
from pathlib import Path

from canvasapi import Canvas
from canvasapi.exceptions import CanvasException

from .config import get_config

# Set up logging
logger = logging.getLogger(__name__)


class CanvasIntegration:
    """Handles integration with Canvas LMS API."""
    
    def __init__(self, api_url=None, api_token=None, course_id=None):
        """
        Initialize Canvas API integration.
        
        Args:
            api_url: Canvas API URL
            api_token: Canvas API token
            course_id: Canvas course ID
        """
        config = get_config()
        
        # Load from config or use parameters
        self.api_url = api_url or config.get("canvas_api", "url")
        self.api_token = api_token or config.get("canvas_api", "token")
        self.course_id = course_id or config.get("canvas_api", "course_id")
        
        if not self.api_url or not self.api_token:
            logger.warning("Canvas API URL or token not configured")
            self.canvas = None
            self.course = None
        else:
            try:
                self.canvas = Canvas(self.api_url, self.api_token)
                self.course = self.canvas.get_course(self.course_id) if self.course_id else None
            except CanvasException as e:
                logger.error(f"Failed to initialize Canvas API: {e}")
                self.canvas = None
                self.course = None
    
    def is_configured(self):
        """Check if Canvas API is configured."""
        return self.canvas is not None
    
    def get_assignment(self, assignment_id):
        """
        Get assignment by ID.
        
        Args:
            assignment_id: Canvas assignment ID
            
        Returns:
            Canvas Assignment object or None
        """
        if not self.is_configured() or not self.course:
            logger.error("Canvas API not configured or course not set")
            return None
        
        try:
            return self.course.get_assignment(assignment_id)
        except CanvasException as e:
            logger.error(f"Failed to get assignment {assignment_id}: {e}")
            return None
    
    def get_student_submission(self, assignment_id, student_id):
        """
        Get student submission for an assignment.
        
        Args:
            assignment_id: Canvas assignment ID
            student_id: Canvas student ID
            
        Returns:
            Canvas Submission object or None
        """
        assignment = self.get_assignment(assignment_id)
        if not assignment:
            return None
        
        try:
            submissions = assignment.get_submissions()
            for submission in submissions:
                if submission.user_id == student_id:
                    return submission
        except CanvasException as e:
            logger.error(f"Failed to get submission for assignment {assignment_id}, student {student_id}: {e}")
        
        return None
    
    def post_grade(self, assignment_id, student_id, grade, comment=None):
        """
        Post grade for a student submission.
        
        Args:
            assignment_id: Canvas assignment ID
            student_id: Canvas student ID
            grade: Grade to post
            comment: Optional comment to post
            
        Returns:
            True if successful, False otherwise
        """
        submission = self.get_student_submission(assignment_id, student_id)
        if not submission:
            return False
        
        try:
            submission.edit(submission={'posted_grade': grade})
            
            if comment:
                submission.edit(comment={'text_comment': comment})
            
            return True
        except CanvasException as e:
            logger.error(f"Failed to post grade for assignment {assignment_id}, student {student_id}: {e}")
            return False
    
    def post_feedback(self, assignment_id, student_id, feedback_file, feedback_format="markdown"):
        """
        Post feedback for a student submission from a file.
        
        Args:
            assignment_id: Canvas assignment ID
            student_id: Canvas student ID
            feedback_file: Path to feedback file
            feedback_format: Format of feedback (markdown, html, text)
            
        Returns:
            True if successful, False otherwise
        """
        # Read feedback from file
        path = Path(feedback_file)
        if not path.exists():
            logger.error(f"Feedback file {feedback_file} does not exist")
            return False
        
        try:
            with open(path, 'r') as f:
                feedback = f.read()
        except Exception as e:
            logger.error(f"Failed to read feedback file {feedback_file}: {e}")
            return False
        
        # Format comment based on feedback format
        if feedback_format.lower() == "markdown":
            comment = feedback
        elif feedback_format.lower() == "html":
            comment = f"<div>{feedback}</div>"
        else:  # text
            comment = feedback
        
        # Post comment
        submission = self.get_student_submission(assignment_id, student_id)
        if not submission:
            return False
        
        try:
            submission.edit(comment={'text_comment': comment})
            return True
        except CanvasException as e:
            logger.error(f"Failed to post feedback for assignment {assignment_id}, student {student_id}: {e}")
            return False


def test_canvas_connection():
    """Test connection to Canvas API."""
    canvas = CanvasIntegration()
    
    if not canvas.is_configured():
        print("Canvas API not configured")
        return False
    
    try:
        # Test if we can get the course
        if canvas.course:
            print(f"Connected to course: {canvas.course.name}")
            return True
        else:
            print("Course not found or not configured")
            return False
    except Exception as e:
        print(f"Error testing Canvas connection: {e}")
        return False


if __name__ == "__main__":
    """Simple CLI for testing."""
    import argparse
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Test Canvas API integration")
    parser.add_argument("--test", action="store_true", help="Test Canvas connection")
    parser.add_argument("--assignment", type=int, help="Get assignment by ID")
    
    args = parser.parse_args()
    
    if args.test:
        test_canvas_connection()
    elif args.assignment:
        canvas = CanvasIntegration()
        assignment = canvas.get_assignment(args.assignment)
        if assignment:
            print(f"Assignment: {assignment.name}")
            print(f"Points possible: {assignment.points_possible}")
            print(f"Due date: {assignment.due_at}")
        else:
            print(f"Assignment {args.assignment} not found")
    else:
        print("No action specified")
        parser.print_help()