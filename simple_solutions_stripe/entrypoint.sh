#!/bin/sh
python3 manage.py collectstatic --noinput --settings=simple_solutions_stripe.settings_prod
python3 manage.py makemigrations --noinput --settings=simple_solutions_stripe.settings_prod
python3 manage.py migrate --noinput --settings=simple_solutions_stripe.settings_prod
exec "$@"