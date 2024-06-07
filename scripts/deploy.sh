#!/bin/bash

set -e

# Execute manage.sh
./manage.py migrate
./manage.py collectstatic --noinput

# Create superuser
echo "
from django.db import IntegrityError
from app.users.models import User

try:
    User.objects.create_superuser('admin', 'admin@example.com', '1234')
    print('Superuser created successfully.')
except IntegrityError:
    print('Error: Superuser already exists.')
" | python manage.py shell


# Execute gunicorn.sh
gunicorn --bind 0.0.0.0:8000 --limit-request-line 6094 --workers 3 --access-logfile - app.wsgi:application
