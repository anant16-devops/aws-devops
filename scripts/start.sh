#!/bin/bash
# Start NGINX and Gunicorn
service nginx start
nohup gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app &
