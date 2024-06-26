#!/bin/sh

echo "Checking postgres is ready..."

until pg_isready -d "$DATABASE_URL"
do
    sleep 
done

echo "Postgres is ready!"

python manage.py collectstatic --no-input
python manage.py migrate --no-input

exec "$@"
