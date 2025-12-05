#!/bin/bash
# Build script for Render deployment

set -o errexit

# Install dependencies
pip install -r Backend/requirements.txt

# Collect static files
cd Backend
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist (optional)
# python manage.py shell < ../scripts/create_superuser.py
