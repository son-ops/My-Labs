#!/bin/sh
set -e

until php artisan migrate
do
  sleep 3
done

php artisan db:seed

exec php artisan serve --host=0.0.0.0 --port="${PORT:-5000}"