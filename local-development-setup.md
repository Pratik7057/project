# Local Development Setup

This project is designed for local development and deployment. No external servers or SSH keys required.

## Local Development Requirements

1. **Docker Desktop** - For containerized deployment
2. **Python 3.9+** - For local backend development
3. **Git** - For version control

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd project
   ```

2. Run locally using Docker:
   ```bash
   # On Windows
   deploy.bat
   
   # On Linux/Mac
   ./deploy.sh
   ```

3. Or run manually:
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   
   # Frontend (in another terminal)
   cd frontend
   python -m http.server 8080
   ```

## Access URLs

- Frontend: http://localhost (when using Docker) or http://localhost:8080 (manual)
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Security Notes

- This setup is for local development only
- Use environment variables for any sensitive configuration
- For production deployment, configure proper security measures
