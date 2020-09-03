#!/bin/bash
export PORTFOLIO_SETTINGS="settings.cfg"
export FLASK_APP=wsgi.py
python -m flask run