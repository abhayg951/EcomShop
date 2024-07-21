#!/bin/bash

NAME="EcomShop"
DJANGODIR=./
SOCKFILE=/run/gunicorn.sock
USER=altair
GROUP=altair
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=EcomShop.settings
DJANGO_WSGI_MODULE=EcomShop.wsgi

cd $DJANGODIR
echo "Starting $NAME as `whoami`"
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=localhost:8001 \
  --log-level=debug \
  --log-file=-