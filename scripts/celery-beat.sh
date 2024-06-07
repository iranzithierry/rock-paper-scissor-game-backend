#!/bin/sh

set -e

celery -A app.celery beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
