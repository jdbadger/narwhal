#!/bin/sh

# echo "Waiting for postgres..."

# while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
#   sleep 0.1
# done

# echo "postgres started"

python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser --no-input --email super@example.com

exec "$@"
