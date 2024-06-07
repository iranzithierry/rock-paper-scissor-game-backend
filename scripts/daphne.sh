#!/bin/sh

set -e

daphne -b 0.0.0.0 -p 8008 app.asgi:application