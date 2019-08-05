#!/bin/bash

DJANGO_DIR=$(readlink -e "${0%/*}")


# . "$DJANGO_DIR"/atlas/configuration/settings.ini

echo "$DJANGO_DIR"

# activate the virtualenv
source $DJANGO_DIR/bin/activate

export PYTHONPATH=bin/python

cd $DJANGO_DIR/main

# Start your unicorn
exec gunicorn wsgi:application --error-log $DJANGO_DIR/log/errors_webapi.log --pid="webapi.pid" -w "4"  -b "0.0.00.0:5005"  -n "webapi"
