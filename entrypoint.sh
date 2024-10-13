#!/bin/bash

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started."

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Start the Django development server
exec "$@"
