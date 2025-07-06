# MusicStream Frontend

This is the frontend application for the MusicStream API system. It's designed to be accessed at www.Radhapi.me.

## Features

- Song search and playback interface
- API key management
- Responsive design for desktop and mobile
- Direct integration with the MusicStream backend API

## Deployment

This frontend is configured to be deployed on a VPS with a custom domain (www.Radhapi.me).

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
3. Open index.html in your browser

## VPS Deployment

To deploy this frontend on a VPS, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Radhaapi/Radhaapi-Frontend
   cd Radhaapi-Frontend
   ```

2. Set up Nginx or Apache to serve the static files:

   ```bash
   # Example Nginx configuration
   server {
       listen 80;
       server_name www.Radhapi.me;
       root /var/www/Radhaapi-Frontend;
       index index.html;
       
       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

3. Configure SSL with Let's Encrypt:

   ```bash
   sudo certbot --nginx -d www.Radhapi.me
   ```

4. Upload your files to the server:

   ```bash
   # Using rsync
   rsync -avz --exclude 'node_modules' ./ user@your-vps:/var/www/Radhaapi-Frontend/
   ```

5. Update your DNS settings to point your domain to your VPS IP address.
