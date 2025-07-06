FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app

# Copy backend files
COPY . /app/

# Create directory for frontend files
RUN mkdir -p /app/frontend

# Assuming frontend files will be copied in via a volume or during build
# You need to run this Dockerfile from the project root, not from the backend directory
COPY ../frontend /app/frontend/

# Install requirements
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
