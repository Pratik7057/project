FROM python:3.9-slim

# Install FFmpeg and nginx
RUN apt-get update && apt-get install -y ffmpeg nginx certbot python3-certbot-nginx && apt-get clean

WORKDIR /app

# Copy backend files
COPY ./backend /app/

# Copy frontend files
COPY ./frontend /usr/share/nginx/html/

# Install requirements
RUN pip install -r requirements.txt

# Create directories
RUN mkdir -p /app/downloads
RUN mkdir -p /app/ssl

# Configure nginx
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 8000 80 443

# Run the server and nginx
CMD ["bash", "-c", "echo 'Starting services for radhaapi.me and api.radhaapi.me' && service nginx start && uvicorn main:app --host 0.0.0.0 --port 8000"]
