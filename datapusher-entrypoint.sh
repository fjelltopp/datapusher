#!/bin/bash
set -e
pip install --no-deps -e /var/www/datapusher
python datapusher/main.py deployment/datapusher_settings.py
