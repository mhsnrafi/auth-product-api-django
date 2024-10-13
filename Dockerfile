# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install netcat-openbsd (required for waiting for PostgreSQL)
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy project files into the container
COPY . /app/

# Set up the entrypoint to manage migrations and static files
ENTRYPOINT ["/app/entrypoint.sh"]
