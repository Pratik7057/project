FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app

# Copy backend files
COPY . /app/

# Create directory for frontend files
RUN mkdir -p /usr/share/nginx/html

# Install requirements
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
