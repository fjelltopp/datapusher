#!/bin/bash
set -e
pip3 install --no-deps -e /var/www/datapusher
python3 datapusher/main.py deployment/datapusher_settings.py
