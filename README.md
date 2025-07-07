# 🎵 Music Streaming API & Frontend

This project provides a complete solution for creating a Music Streaming API with a modern frontend interface.

## 📁 Project Structure

```
project/
│
├── docker-compose.yml      # Docker Compose configuration for local deployment
├── Dockerfile              # Docker configuration with Nginx integration
├── deploy.bat              # Windows deployment script
├── deploy.sh               # Linux deployment script
│
├── nginx/                  # Nginx configuration
│   └── nginx.conf          # Nginx server configuration
│
├── backend/                # FastAPI Backend
│   ├── main.py             # API Logic (yt-dlp + YouTube)
│   ├── downloads/          # Audio Downloads (empty directory)
│   ├── requirements.txt    # Python Dependencies
│   └── api_keys.json       # API keys storage
│
├── frontend/               # Music Frontend
│   ├── index.html          # Modern Search & Play UI
│   ├── app.js              # API Integration
│   ├── styles.css          # Modern UI Styling
│   ├── api-key/            # API key generation interface
│   └── package.json        # Frontend dependencies
│
└── README.md               # Project Guide
```

## 🔧 Getting Started

### Prerequisites

Before starting, ensure you have the following installed:

* Python 3.9 or higher
* Node.js (optional, for frontend development)
* FFmpeg (for audio conversion)

### Running the Backend

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Running the Frontend

For local development, simply open the `frontend/index.html` file in a web browser, or set up a simple HTTP server:

```bash
# Python 3
python -m http.server -d frontend 8080
```

## 🚀 Local Deployment

This project is configured for local deployment with:
- API at http://localhost:8000 (nginx disabled for simplicity)
- Frontend served by FastAPI backend
- Single service deployment

### Configuration Management

Use the config management tool to control deployment and API status:

```bash
# Show current status
config.bat status

# Activate both deployment and API
config.bat activate

# Deactivate everything (safety mode)
config.bat deactivate

# Control deployment only
config.bat activate-deploy
config.bat deactivate-deploy

# Control API only
config.bat activate-api
config.bat deactivate-api
```

### Deployment Steps:

1. Clone or download your project to your local machine:
   ```bash
   git clone https://github.com/Pratik7057/project.git
   cd project
   ```

2. Configure the system (optional):
   ```bash
   # Check current status
   config.bat status
   
   # Activate if needed
   config.bat activate
   ```

3. Run the deployment script:
   ```bash
   # On Windows
   deploy.bat
   
   # On Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. The services will be available at:
   - API & Frontend: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

The frontend and backend API are both accessible at `http://localhost:8000`.

## 🔌 API Endpoints

The API is hosted at `http://localhost:8000` with these endpoints:

| Endpoint                           | Description                               |
| ---------------------------------- | ----------------------------------------- |
| `http://localhost:8000/get-audio`  | Search Song by Query (Returns Audio Link) |
| `http://localhost:8000/song/{video_id}` | Download Song by Video ID          |
| `http://localhost:8000/download/{filename}` | Download File                  |
| `http://localhost:8000/generate-api-key` | Generate API Key                  |
| `http://localhost:8000/health`     | API Health Check                          |

## 🔒 Security Notes

* The default API key is set to "your_api_key_here" and should be changed
* API keys are stored in a JSON file (`api_keys.json`)
* Always use HTTPS in production

## 🔧 Environment Configuration

For local deployment, create an `.env` file in the project root with these variables:

```
DOMAIN=localhost
API_DOMAIN=localhost
PORT=8000
HOST=0.0.0.0
API_STATUS=ACTIVATED
```

### 🔒 Configuration Control

The project includes safety mechanisms to prevent accidental deployment:

1. **Deployment Scripts**: Check `CONFIG_STATUS` in `deploy.bat` and `deploy.sh`
2. **API Backend**: Checks `API_STATUS` environment variable
3. **Config File**: Use `config.env` to manage all settings

**To enable deployment:**
- Change `CONFIG_STATUS=ACTIVATED` in deployment scripts
- Set `API_STATUS=ACTIVATED` in environment or docker-compose.yml
- Or use the config.env file for centralized configuration

## 📊 Publishing to GitHub

Follow these steps to publish your project to GitHub:

1. Create a new repository on GitHub:
   - Go to [GitHub](https://github.com) and sign in
   - Click the "+" icon in the top-right corner and select "New repository"
   - Name your repository (e.g., "music-streaming-api")
   - Add a description (optional)
   - Choose public or private repository
   - Click "Create repository"

2. Initialize Git in your local project:
   ```bash
   # Navigate to your project directory
   cd d:\api\project

   # Initialize Git repository
   git init

   # Add all files to Git
   git add .

   # Commit the files
   git commit -m "Initial commit of Music Streaming API"
   ```

3. Connect to GitHub and push:
   ```bash
   # Add the GitHub repository as a remote
   git remote add origin https://github.com/yourusername/music-streaming-api.git

   # Push your code to GitHub
   git push -u origin main
   ```

4. Protect sensitive data:
   - Make sure to add any sensitive files to .gitignore
   - Consider using environment variables for API keys and credentials
   - The project already includes a .gitignore file

## 🔧 Environment Configuration

For local deployment, create an `.env` file in the project root with these variables:

```
# API Configuration
ADMIN_KEY=your_secure_admin_key_here

# Server Configuration (these are set in docker-compose.yml)
# PORT=8000
# HOST=0.0.0.0
# TZ=UTC
# DOMAIN=localhost
# API_DOMAIN=localhost

# Optional: MongoDB Connection (if using external database)
# MONGODB_URI=mongodb://username:password@host:port/database
```

These environment variables will be used by the Docker container when deploying with docker-compose on your VPS.

## 🔑 API Key Generation

To generate a new API key for your music bot locally:

1. **Using the Web Interface**:
   - Visit `http://localhost/api-key/` in your browser
   - Enter your admin secret key (default: "Pratik@143")
   - Copy and save your new API key

2. **Using the Command Line**:
   ```bash
   # If using Docker
   docker exec -it project_music-api_1 python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # If running manually
   cd backend
   python -c "import secrets; print('Generated API Key:', secrets.token_urlsafe(32))"
   ```

3. **Using Direct API Call**:
   ```bash
   curl -X POST "http://localhost:8000/generate-api-key" \
     -H "Content-Type: application/json" \
     -d '{"admin_key": "your_admin_secret_here"}'
   ```

## 🧩 Frontend Features

* Modern, Spotify-inspired UI
* Responsive design for mobile and desktop
* Local storage for API key persistence
* Audio player with controls
* Search functionality
