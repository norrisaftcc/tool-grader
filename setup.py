"""
Setup script for tool-grader package.
"""

from setuptools import setup, find_packages

setup(
    name="tool-grader",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml>=5.1",
        "flask>=2.0.0",
        "docker>=5.0.0",
        "canvasapi>=2.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "flake8>=3.9.0",
            "mypy>=0.812",
        ]
    },
    author="Tool Grader Team",
    author_email="example@example.com",
    description="A Python autograding system integrating GitHub Classroom and Canvas LMS",
    keywords="education, grading, docker, canvas, github",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "tool-grader=cli.commands:main",
        ],
    },
)