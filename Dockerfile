FROM python:3.9-slim

# Install FFmpeg only (nginx disabled)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app

# Copy backend files
COPY ./backend /app/

# Copy frontend files (for static serving by FastAPI)
COPY ./frontend /usr/share/nginx/html/

# Install requirements
RUN pip install -r requirements.txt

# Create directories
RUN mkdir -p /app/downloads

# Expose only backend port
EXPOSE 8000

# Run only the backend server (nginx disabled)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
