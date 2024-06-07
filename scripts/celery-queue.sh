#!/bin/sh

set -e

celery -A app.celery worker --loglevel=debug --concurrency=4
