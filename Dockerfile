# Use Python 3.12 alpine for lightweight container
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY journal.py ./

# Create volume mount point for database
VOLUME ["/app/data"]

# Set database path to volume
ENV DATABASE_PATH=/app/data/journal.db

# Expose port
EXPOSE 8000

# Run FastAPI server
CMD ["uv", "run", "fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "journal.py"]
