FROM python:3.10-slim

LABEL maintainer="Tool Grader Team"
LABEL description="Python autograder execution container"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Create non-root user
RUN groupadd -r grader && useradd -r -g grader grader

# Create work directory
WORKDIR /code
RUN chown grader:grader /code

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER grader

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]