#!/bin/bash
cd Backend
gunicorn elevateu_backend.wsgi:application --bind 0.0.0.0:10000
