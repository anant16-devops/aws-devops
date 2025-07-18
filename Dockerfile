FROM python:3.9-slim

# Set up directories
WORKDIR /app

# Install dependencies
COPY my-flask-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and NGINX config
COPY my-flask-app/app/ /app/
COPY my-flask-app/nginx/nginx.conf /etc/nginx/nginx.conf

# Install NGINX
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy start scripts
COPY scripts/start.sh /start.sh
COPY scripts/stop.sh /stop.sh
RUN chmod +x /start.sh /stop.sh

# Expose ports
EXPOSE 80

# Start NGINX and Gunicorn
CMD ["/start.sh"]
