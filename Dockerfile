# Use a base image with Python and Nginx
FROM python:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80

# Start both Gunicorn and Nginx
CMD sh -c "gunicorn -w 4 -b 127.0.0.1:8000 --log-level debug --access-logfile - --error-logfile - main:app & nginx -g 'daemon off;'"