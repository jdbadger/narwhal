#!/bin/sh

echo "Checking postgres is ready..."

until pg_isready -d "$DATABASE_URL"
do
    sleep 2
done

echo "Postgres is ready!"

python manage.py flush --no-input
python manage.py migrate --no-input
python manage.py createsuperuser --no-input

exec "$@"

