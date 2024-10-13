#!/bin/bash

# Pull the latest code
git pull origin main

# Build the production Docker containers
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose exec web python manage.py migrate --noinput

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Start the production server using gunicorn
docker-compose exec web gunicorn --bind 0.0.0.0:8000 authAPI.wsgi:application --workers 3

echo "Production setup completed!"
