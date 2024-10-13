#!/bin/bash

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: Docker is not installed.' >&2
  exit 1
fi

# Pull latest changes
echo "Pulling latest changes from GitHub..."
git pull origin main

# Build Docker containers
echo "Building Docker containers..."
docker-compose up --build -d

# Run migrations
echo "Running database migrations..."
docker-compose exec web python manage.py migrate

# Create a superuser (optional, can be commented out)
echo "Creating a superuser (for admin panel)..."
docker-compose exec web python manage.py createsuperuser

# Install dependencies (if needed)
echo "Installing Python dependencies..."
docker-compose exec web pip install -r requirements.txt

# Start the development server
echo "Starting the Django development server..."
docker-compose up

echo "Dev setup completed!"
