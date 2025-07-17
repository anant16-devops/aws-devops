#!/bin/bash
# Kill Gunicorn and NGINX
pkill gunicorn || true
pkill nginx || true
