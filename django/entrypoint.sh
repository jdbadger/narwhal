#!/bin/sh

echo "Checking postgres is ready..."

until pg_isready -d "$DJANGO_DATABASE_URL"
do
    sleep 2
done

echo "Postgres is ready!"

python manage.py migrate --no-input

if [ "$DJANGO_SETTINGS_MODULE" = "core.settings.dev" ]
then
    python manage.py createsuperuser --no-input
fi

if [ "$DJANGO_SETTINGS_MODULE" = "core.settings.prod" ]
then
    python manage.py collectstatic --no-input
fi

exec "$@"
