#!/bin/bash
set -e
pip install --no-deps -e /var/www/datapusher

exec "$@"
