# MusicStream Frontend

This is the frontend application for the MusicStream API system.

## Features

- Song search and playbook interface
- API key management
- Responsive design for desktop and mobile
- Direct integration with the MusicStream backend API

## Deployment

This frontend can be deployed locally or on any web server.

## Configuration

- Backend API URL is configured in `app.js` and `api-key/index.html`
- Currently points to: http://localhost:8000

## Files

- `index.html`: Main application page
- `app.js`: Application logic
- `styles.css`: Styling for the application
- `api-key/index.html`: Page for generating API keys
- `package.json`: Node.js package configuration

## Integration

This frontend connects to the MusicStream backend API, which must be running and accessible for the application to function properly. The backend handles:

- Song search via YouTube
- Audio processing and streaming
- API key generation and validation

## Development

To run this frontend locally:

1. Clone the repository
2. Modify the API_URL in app.js to point to your local backend
3. Open index.html in your browser or use a local server:
   ```bash
   python -m http.server -d frontend 8080
   ```

## Local Deployment

This frontend is designed for local development:

1. Make sure the backend is running on http://localhost:8000
2. Open the frontend files in any web browser
3. Or use Docker for full containerized deployment with `deploy.bat` or `deploy.sh`
