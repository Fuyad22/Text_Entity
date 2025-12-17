FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for building wheels)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements file from the context (project root)
COPY requirements.txt .

# Install Python dependencies and Spacy model
# We split this to cache the expensive install steps
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
