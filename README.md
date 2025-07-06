# 🎵 Music Streaming API & Frontend for radhaapi.me

This project provides a complete solution for creating a Music Streaming API with a modern frontend interface, deployed at https://radhaapi.me with the API endpoint at https://api.radhaapi.me.

## 📁 Project Structure

```
project/
│
├── docker-compose.yml      # Docker Compose configuration for VPS deployment
├── Dockerfile              # Docker configuration with Nginx integration
├── deploy.bat              # Windows deployment script
├── deploy.sh               # Linux deployment script
│
├── nginx/                  # Nginx configuration
│   └── nginx.conf          # Nginx server configuration for radhaapi.me
│
├── backend/                # FastAPI Backend
│   ├── main.py             # API Logic (yt-dlp + YouTube)
│   ├── downloads/          # Audio Downloads (empty directory)
│   ├── requirements.txt    # Python Dependencies
│   └── api_keys.json       # API keys storage
│
├── frontend/               # Music Frontend (served at radhaapi.me)
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

## 🚀 VPS Deployment

This project is configured for a single VPS deployment with:
- Frontend at https://radhaapi.me
- API at https://api.radhaapi.me
- Both running on the same server

### Deployment Steps:

1. Upload your project to the VPS:
   ```bash
   # Using SCP (replace with your server details)
   scp -r project/ user@your-vps-ip:/home/user/radhaapi
   
   # OR use SFTP or any other method to transfer files
   ```

2. SSH into your VPS and run the deployment script:
   ```bash
   ssh user@your-vps-ip
   cd /home/user/radhaapi
   
   # Make the script executable
   chmod +x deploy.sh
   
   # Run the deployment
   ./deploy.sh
   ```

3. Set up SSL certificates with Let's Encrypt:
   ```bash
   # After the container is running, get the container ID from the deploy script output
   docker exec -it [container_id] certbot --nginx -d radhaapi.me -d www.radhaapi.me -d api.radhaapi.me
   ```

4. Update your DNS settings:
   - Point radhaapi.me to your VPS IP address
   - Create an A record for api.radhaapi.me pointing to the same IP address

The frontend will be served at `https://radhaapi.me` and the backend API will be accessible at `https://api.radhaapi.me`.

## 🔌 API Endpoints

The API is hosted at `https://api.radhaapi.me` with these endpoints:

| Endpoint                           | Description                               |
| ---------------------------------- | ----------------------------------------- |
| `https://api.radhaapi.me/get-audio`| Search Song by Query (Returns Audio Link) |
| `https://api.radhaapi.me/song/{video_id}` | Download Song by Video ID          |
| `https://api.radhaapi.me/download/{filename}` | Download File                  |
| `https://api.radhaapi.me/generate-api-key` | Generate API Key                  |
| `https://api.radhaapi.me/health`   | API Health Check                          |

## 🔒 Security Notes

* The default API key is set to "your_api_key_here" and should be changed
* API keys are stored in a JSON file (`api_keys.json`)
* Always use HTTPS in production

## 🔧 Environment Configuration

For deployment on your VPS with domain radhaapi.me, create an `.env` file in the project root with these variables:

```
DOMAIN=radhaapi.me
API_DOMAIN=api.radhaapi.me
PORT=8000
HOST=0.0.0.0
```

## 📊 Publishing to GitHub

Follow these steps to publish your project to GitHub:

1. Create a new repository on GitHub:
   - Go to [GitHub](https://github.com) and sign in
   - Click the "+" icon in the top-right corner and select "New repository"
   - Name your repository (e.g., "radhaapi-music-streaming")
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
   git commit -m "Initial commit of Music Streaming API for radhaapi.me"
   ```

3. Connect to GitHub and push:
   ```bash
   # Add the GitHub repository as a remote
   git remote add origin https://github.com/yourusername/radhaapi-music-streaming.git

   # Push your code to GitHub
   git push -u origin main
   ```

4. Protect sensitive data:
   - Make sure to add any sensitive files to .gitignore
   - Consider using environment variables for API keys and credentials
   - The project already includes a .gitignore file in the frontend directory

5. Setting up GitHub Actions (optional):
   Create a `.github/workflows/deploy.yml` file for automated deployment to your VPS.

```
# API Configuration
ADMIN_KEY=your_secure_admin_key_here

# Server Configuration (these are set in docker-compose.yml)
# PORT=8000
# HOST=0.0.0.0
# TZ=UTC
# DOMAIN=radhaapi.me
# API_DOMAIN=api.radhaapi.me

# Optional: MongoDB Connection (if using external database)
# MONGODB_URI=mongodb://username:password@host:port/database
```

These environment variables will be used by the Docker container when deploying with docker-compose on your VPS.

## 🔑 API Key Generation

To generate a new API key for your music bot on your VPS:

1. **Using the Web Interface**:
   - Visit `https://radhaapi.me/api-key/` in your browser
   - Enter your admin secret key (configured in your .env file)
   - Copy and save your new API key

2. **Using the Command Line**:
   ```bash
   # SSH into your VPS
   ssh user@your-vps-ip
   
   # If using Docker
   docker exec -it project_music-api_1 python -c "import main; print(main.generate_api_key())"
   
   # If using manual deployment
   cd /var/www/radhaapi.me/backend
   source venv/bin/activate
   python -c "import main; print(main.generate_api_key())"
   ```

3. **Using Direct API Call**:
   ```bash
   curl -X POST "https://api.radhaapi.me/generate-api-key" \
     -H "Content-Type: application/json" \
     -d '{"admin_key": "your_admin_secret_here"}'
   ```

## 🐳 VPS Deployment Details

This project uses Docker for easy deployment on a single VPS with:
- Frontend at https://radhaapi.me
- API endpoint at https://api.radhaapi.me
- Both running on the same VPS

### Docker Compose Deployment (Recommended)

Our docker-compose.yml is already configured for deployment:

```yaml
version: '3'

services:
  music-api:
    build: .
    ports:
      - "80:80"      # For frontend (radhaapi.me)
      - "443:443"    # For secure frontend (https)
      - "8000:8000"  # For direct API access
    volumes:
      - ./backend/downloads:/app/downloads  # Persistent storage
      - ./ssl:/app/ssl                      # SSL certificates
    restart: unless-stopped
    environment:
      - TZ=UTC
      - DOMAIN=radhaapi.me
      - API_DOMAIN=api.radhaapi.me
      - PORT=8000
      - HOST=0.0.0.0
```

To deploy:

```bash
# 1. On your VPS
cd /path/to/project

# 2. Create .env file with your configuration (optional)
cat > .env << EOF
ADMIN_KEY=your_secure_admin_key
TZ=UTC
EOF

# 3. Build and start the services
docker-compose up -d

# 4. Check the logs
docker-compose logs -f
```

### What's Happening During Deployment

1. The Dockerfile builds a single container that:
   - Installs Python, FFmpeg, and Nginx
   - Sets up the backend API on port 8000
   - Configures Nginx to serve frontend at radhaapi.me
   - Routes API requests to api.radhaapi.me → localhost:8000

2. Nginx configuration:
   - Serves static frontend files from /usr/share/nginx/html
   - Routes API requests from api.radhaapi.me to the FastAPI backend

3. SSL/HTTPS setup:
   - After deployment, you'll need to run the certbot command
   - This adds HTTPS support for both domains

### Manual VPS Deployment (Alternative)

If you prefer not to use Docker:

1. Copy the project to your VPS:
```bash
# Using SCP to transfer files
scp -r /path/to/project root@your-vps-ip:/var/www/radhaapi.me
ssh root@your-vps-ip
cd /var/www/radhaapi.me
```

2. Install dependencies:
```bash
# Install system dependencies
apt update
apt install -y python3 python3-pip python3-venv ffmpeg nginx certbot python3-certbot-nginx

# Install Python dependencies
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up systemd service for backend:
```bash
cat > /etc/systemd/system/radhaapi.service << EOF
[Unit]
Description=Radha Music API Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/radhaapi.me/backend
ExecStart=/var/www/radhaapi.me/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
Environment="ADMIN_KEY=your_secure_admin_key"
Environment="DOMAIN=radhaapi.me"
Environment="API_DOMAIN=api.radhaapi.me"

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl enable radhaapi
systemctl start radhaapi
```

4. Configure Nginx:
```bash
# Frontend site configuration
cat > /etc/nginx/sites-available/radhaapi.me << EOF
server {
    listen 80;
    server_name radhaapi.me www.radhaapi.me;
    
    # Redirect to HTTPS
    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name radhaapi.me www.radhaapi.me;
    
    ssl_certificate /etc/letsencrypt/live/radhaapi.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/radhaapi.me/privkey.pem;
    
    # Serve frontend static files
    location / {
        root /var/www/radhaapi.me/frontend;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }
}

# API subdomain configuration
cat > /etc/nginx/sites-available/api.radhaapi.me << EOF
server {
    listen 80;
    server_name api.radhaapi.me;
    
    # Redirect to HTTPS
    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name api.radhaapi.me;
    
    ssl_certificate /etc/letsencrypt/live/radhaapi.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/radhaapi.me/privkey.pem;
    
    # API endpoints
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
    
    # Direct access to downloaded files
    location /downloads/ {
        alias /var/www/radhaapi.me/backend/downloads/;
    }
}
EOF

# Enable site and restart nginx
ln -sf /etc/nginx/sites-available/radhaapi.me /etc/nginx/sites-enabled/
systemctl restart nginx
```

5. Set up SSL with Certbot:
```bash
# We already installed certbot earlier
certbot --nginx -d radhaapi.me -d www.radhaapi.me -d api.radhaapi.me
```

## 🧩 Frontend Features

* Modern, Spotify-inspired UI
* Responsive design for mobile and desktop
* Local storage for API key persistence
* Audio player with controls
* Search functionality
