FROM python:3.9-slim

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

# Set up directories
# Copy your application files
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r my-flask-app/app/requirements.txt

# Copy app and NGINX config
COPY nginx.conf /etc/nginx/nginx.conf

# Install NGINX
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        curl \
        && rm -rf /var/lib/apt/lists/* \
        && apt-get clean

# Copy start scripts
# COPY scripts/start.sh /start.sh
# COPY scripts/stop.sh /stop.sh
RUN chmod +x scripts/start.sh scripts/stop.sh

# Expose ports
EXPOSE 80

# Start NGINX and Gunicorn
CMD ["scripts/start.sh"]
