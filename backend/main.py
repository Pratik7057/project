from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import json
import secrets
import yt_dlp
from fastapi.staticfiles import StaticFiles

# File-based API key storage (since MongoDB might not be available)
API_KEYS_FILE = "api_keys.json"
ADMIN_KEY = os.getenv("ADMIN_KEY", "Pratik@143")  # Get from environment or use default

# Initialize API keys storage
def setup_api_keys():
    if not os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, "w") as f:
            json.dump({
                "keys": [{
                    "key": ADMIN_KEY,
                    "is_admin": True,
                    "created_at": datetime.now().isoformat(),
                    "description": "Default admin key"
                }]
            }, f)
    
    # Make sure the downloads directory exists
    os.makedirs("downloads", exist_ok=True)

# Run setup on import
setup_api_keys()

# Initialize FastAPI
app = FastAPI(
    title="Music Bot API", 
    description="A complete solution for creating a Music Streaming API"
)

# CORS Configuration
# Get allowed origins from environment or use default
allowed_origins = os.getenv("ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to block sensitive paths
@app.middleware("http")
async def block_sensitive_paths(request: Request, call_next):
    blocked_paths = ["/.env", "/config.env", "/.git", "/.htaccess", "/.dockerignore"]
    if request.url.path in blocked_paths:
        raise HTTPException(status_code=404, detail="Not found")
    return await call_next(request)

# Legacy file-based API key management (kept for backward compatibility)
API_KEYS_FILE = "api_keys.json"

# Create API keys file if it doesn't exist for backward compatibility
if not os.path.exists(API_KEYS_FILE):
    with open(API_KEYS_FILE, "w") as f:
        json.dump({"keys": ["your_api_key_here"]}, f)

# Models
class SongQuery(BaseModel):
    query: str

class ApiKeyRequest(BaseModel):
    admin_key: str = "Pratik@143"  # Admin key for authentication
    description: Optional[str] = "API Key"
    expires_in_days: Optional[int] = None  # None means no expiration

class ApiKeyResponse(BaseModel):
    api_key: str
    expires_at: Optional[datetime] = None
    description: str
    message: str

class ApiKeyList(BaseModel):
    keys: List[Dict[str, Any]]

# File-based API Key functions
async def get_api_key(key: str) -> Optional[dict]:
    """Get API key details from the file"""
    try:
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)
            for key_doc in data.get("keys", []):
                if key_doc["key"] == key:
                    return key_doc
    except:
        pass
    return None

async def is_valid_api_key(key: str) -> bool:
    """Check if API key exists and is valid"""
    api_key = await get_api_key(key)
    if not api_key:
        return False
    
    # Check if key has expired
    if "expires_at" in api_key:
        expiry_time = datetime.fromisoformat(api_key["expires_at"])
        if expiry_time < datetime.now():
            return False
        
    return True

async def verify_admin_key(admin_key: str) -> bool:
    """Verify if the provided key is a valid admin key"""
    if admin_key == ADMIN_KEY:  # Quick check for the default admin key
        return True
        
    api_key = await get_api_key(admin_key)
    return api_key is not None and api_key.get("is_admin", False)

async def add_api_key(description: str = "API Key", expires_in_days: Optional[int] = None) -> dict:
    """Add a new API key to the file"""
    new_key = secrets.token_urlsafe(32)
    
    key_doc = {
        "key": new_key,
        "description": description or "API Key",
        "created_at": datetime.now().isoformat(),
        "is_admin": False
    }
    
    if expires_in_days:
        key_doc["expires_at"] = (datetime.now() + timedelta(days=expires_in_days)).isoformat()
    
    # Read existing keys
    try:
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {"keys": []}
    
    # Add new key
    data["keys"].append(key_doc)
    
    # Save back to file
    with open(API_KEYS_FILE, "w") as f:
        json.dump(data, f)
        
    return key_doc

async def list_api_keys() -> List[dict]:
    """List all API keys from the file"""
    try:
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)
            keys = data.get("keys", [])
            
            # Don't return the actual admin keys
            for key in keys:
                if key.get("is_admin", False):
                    key["key"] = "***ADMIN KEY***"
            
            return keys
    except:
        return []

async def delete_api_key(key: str) -> bool:
    """Delete an API key from the file"""
    try:
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)
        
        initial_count = len(data.get("keys", []))
        data["keys"] = [k for k in data.get("keys", []) if k.get("key") != key or k.get("is_admin", False)]
        
        with open(API_KEYS_FILE, "w") as f:
            json.dump(data, f)
            
        return len(data["keys"]) < initial_count
    except:
        return False

# API key verification middleware
async def verify_api_key(authorization: str = Header(...)):
    api_key = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    
    # Check if the API key is valid
    if await is_valid_api_key(api_key):
        return api_key
    
    raise HTTPException(status_code=403, detail="Invalid API Key")

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

@app.get("/get-audio")
async def get_audio(query: str, request: Request, authorization: str = Header(...)):
    # Verify API key
    await verify_api_key(authorization)
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if result and 'entries' in result and len(result['entries']) > 0:
                video = result['entries'][0]
                video_id = video.get('id', '')
                
                # Get the base URL of the request to construct the download link
                host_url = str(request.base_url).rstrip('/')
                
                # Get the best thumbnail available or fallback to maxresdefault
                thumbnail_url = ''
                if video.get('thumbnails'):
                    # Try to find the highest quality thumbnail
                    for thumbnail in sorted(video.get('thumbnails', []), 
                                          key=lambda x: x.get('height', 0) if x.get('height') else 0, 
                                          reverse=True):
                        if thumbnail.get('url'):
                            thumbnail_url = thumbnail.get('url')
                            break
                
                if not thumbnail_url:
                    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                
                return {
                    "status": "done", 
                    "title": video.get('title', 'Unknown Title'),
                    "duration": video.get('duration', 0),
                    "link": f"{host_url}/download/{video_id}.mp3",
                    "thumbnail": thumbnail_url,
                    "video_id": video_id
                }
            else:
                raise HTTPException(status_code=404, detail="Song not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/song/{video_id}")
async def download_song(video_id: str, request: Request, authorization: str = Header(...)):
    # Verify API key
    await verify_api_key(authorization)
    try:
        # Use video_id as the filename to match the format in get-audio endpoint
        filename = f"{video_id}.mp3"
        output_path = os.path.join("downloads", filename)
        
        # Check if file already exists
        if os.path.exists(output_path):
            title = "Cached Song"  # We could store titles in a separate file if needed
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"downloads/{video_id}.%(ext)s",
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
                
                title = "Unknown Title"
                if info and isinstance(info, dict):
                    title = info.get('title', 'Unknown Title')
        
        # Get the base URL of the request
        host_url = str(request.base_url).rstrip('/')
                
        return {
            "status": "done", 
            "message": "Download successful",
            "title": title,
            "video_id": video_id,
            "filename": filename,
            "download_url": f"{host_url}/download/{filename}"
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Download audio file by filename. This endpoint supports both direct access (for music bots)
    and authenticated access for API users.
    """
    file_path = os.path.join("downloads", filename)
    
    # If file doesn't exist and filename looks like a video ID (no extension), try to download it
    if not os.path.exists(file_path) and '.' not in filename:
        video_id = filename
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"downloads/{video_id}.%(ext)s",
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
                
            # Update file path to include mp3 extension
            file_path = os.path.join("downloads", f"{video_id}.mp3")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error downloading audio: {str(e)}")
    
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='audio/mpeg'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found or failed to download")

@app.post("/generate-api-key", response_model=ApiKeyResponse)
async def generate_api_key(request: ApiKeyRequest):
    # Verify admin key
    is_admin = await verify_admin_key(request.admin_key)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized - Invalid admin key")
    
    try:
        # Add new API key to MongoDB
        key_data = await add_api_key(
            description=request.description if request.description else "API Key",
            expires_in_days=request.expires_in_days
        )
        
        # Also add to file-based system for backward compatibility
        try:
            # Read existing keys
            with open(API_KEYS_FILE, "r") as f:
                data = json.load(f)
                keys_list = data.get("keys", [])
            
            # Add new key
            keys_list.append(key_data["key"])
            
            # Save updated keys
            with open(API_KEYS_FILE, "w") as f:
                json.dump({"keys": keys_list}, f)
        except:
            pass  # Ignore file errors, MongoDB is primary storage
        
        return {
            "api_key": key_data["key"],
            "expires_at": key_data.get("expires_at"),
            "description": key_data["description"],
            "message": "API key generated successfully. Include this key in the Authorization header as: 'Bearer YOUR_API_KEY'"
        }
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail="Failed to generate unique API key, please try again")
        else:
            raise HTTPException(status_code=500, detail=f"Error generating API key: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api-keys", response_model=ApiKeyList)
async def list_keys(admin_key: str):
    """List all API keys (admin only)"""
    is_admin = await verify_admin_key(admin_key)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized - Invalid admin key")
    
    keys = await list_api_keys()
    return {"keys": keys}

@app.delete("/api-key/{key}")
async def delete_key(key: str, admin_key: str):
    """Delete an API key (admin only)"""
    is_admin = await verify_admin_key(admin_key)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized - Invalid admin key")
    
    # Prevent deleting admin keys
    api_key = await get_api_key(key)
    if api_key and api_key.get("is_admin", False):
        raise HTTPException(status_code=400, detail="Cannot delete admin keys")
    
    success = await delete_api_key(key)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Also remove from file-based system
    try:
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)
            if key in data.get("keys", []):
                data["keys"].remove(key)
                with open(API_KEYS_FILE, "w") as f2:
                    json.dump(data, f2)
    except:
        pass  # Ignore file errors
    
    return {"message": "API key deleted successfully"}

@app.get("/validate-api-key")
async def validate_key(key: str):
    """Validate if an API key is valid"""
    is_valid = await is_valid_api_key(key)
    
    # Check file-based system as fallback
    if not is_valid:
        try:
            pass
        except:
            pass
    
    return {
        "valid": is_valid,
        "message": "API key is valid" if is_valid else "API key is invalid or expired"
    }

@app.get("/download/{video_id}.mp3")
async def download_by_video_id(video_id: str, request: Request, authorization: Optional[str] = Header(None)):
    """
    Download a song directly using its video_id, which matches the format provided in the get-audio response.
    This endpoint allows direct playback in music bots or applications.
    """
    # No API key required for this endpoint to support direct playback in music bots
    
    # Check if the file already exists in downloads
    file_path = os.path.join("downloads", f"{video_id}.mp3")
    
    # If file doesn't exist, download it
    if not os.path.exists(file_path):
        pass
    
    # Return the file
    if os.path.exists(file_path):
        pass

# Mount the frontend static files - should be placed at the end of the file
# Check if we're in a Docker environment by looking for frontend in different locations
frontend_dir = "/usr/share/nginx/html"  # Default Docker path for frontend files

# If running locally (not in Docker), use the relative path
if not os.path.exists(frontend_dir):
    # Get the parent directory of the current file (backend dir)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the backend dir (project root)
    project_root = os.path.dirname(backend_dir)
    # Path to the frontend directory
    frontend_dir = os.path.join(project_root, "frontend")

# Create a function to serve the index.html for any non-API routes
@app.get("/", include_in_schema=False)
async def serve_frontend_root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/api-key", include_in_schema=False)
async def serve_api_key_page():
    return FileResponse(os.path.join(frontend_dir, "api-key", "index.html"))

# Mount the frontend static files
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
