#!/bin/sh
./wait-for-it.sh db:5432
python manage.py makemigrations
python manage.py migrate
python manage.py get_logs http://www.almhuette-raith.at/apache-log/access.log
python manage.py runserver 0.0.0.0:8000
