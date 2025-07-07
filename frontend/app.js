// API Configuration
// For production, point to your domain or use localhost for local development
const API_URL = 'http://localhost:8000'; // Local development
// const API_URL = 'https://your-domain.com/api'; // Production API (update with your domain)
let API_KEY = localStorage.getItem('musicstream_api_key') || 'your_api_key_here';

// DOM Elements
const searchInput = document.getElementById('query');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('results');
const playerContainer = document.getElementById('player');
const currentSongDisplay = document.getElementById('currentSongDisplay');
const apiKeyInput = document.getElementById('apiKeyInput');
const toggleApiKeyBtn = document.getElementById('toggleApiKey');
const saveApiKeyBtn = document.getElementById('saveApiKey');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set API key from localStorage if available
    apiKeyInput.value = API_KEY;
    
    // Event listeners
    searchBtn.addEventListener('click', searchSongs);
    searchInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') searchSongs();
    });
    
    toggleApiKeyBtn.addEventListener('click', toggleApiKeyVisibility);
    saveApiKeyBtn.addEventListener('click', saveApiKey);
});

// Toggle API key visibility
function toggleApiKeyVisibility() {
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
        toggleApiKeyBtn.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        apiKeyInput.type = 'password';
        toggleApiKeyBtn.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

// Save API key to localStorage
function saveApiKey() {
    const newApiKey = apiKeyInput.value.trim();
    if (newApiKey) {
        API_KEY = newApiKey;
        localStorage.setItem('musicstream_api_key', API_KEY);
        
        // Show confirmation
        const originalText = saveApiKeyBtn.textContent;
        saveApiKeyBtn.textContent = 'Saved!';
        saveApiKeyBtn.style.backgroundColor = '#4cd964';
        
        setTimeout(() => {
            saveApiKeyBtn.textContent = originalText;
            saveApiKeyBtn.style.backgroundColor = '';
        }, 2000);
    }
}

// Format duration from seconds to MM:SS
function formatDuration(seconds) {
    if (!seconds) return '00:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Search for songs
async function searchSongs() {
    const query = searchInput.value.trim();
    if (!query) return;
    
    // Show loading state
    resultsContainer.innerHTML = '<div class="loading">Searching for songs...</div>';
    currentSongDisplay.innerHTML = '<h2>Searching...</h2><p>Looking for your requested song</p>';
    
    try {
        const response = await fetch(`${API_URL}/get-audio?query=${encodeURIComponent(query)}`, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to search for songs');
        }
        
        const data = await response.json();
        
        if (data.status === 'done') {
            // Update UI with search results
            displaySearchResults(data);
        } else {
            resultsContainer.innerHTML = '<div class="error-message">No songs found matching your search.</div>';
            currentSongDisplay.innerHTML = '<h2>No Results</h2><p>Try searching with different keywords</p>';
        }
    } catch (error) {
        console.error('Search error:', error);
        resultsContainer.innerHTML = `<div class="error-message">${error.message || 'An error occurred during search'}</div>`;
        currentSongDisplay.innerHTML = '<h2>Search Error</h2><p>There was a problem with your request. Please check your API key.</p>';
    }
}

// Display search results
function displaySearchResults(data) {
    currentSongDisplay.innerHTML = `<h2>Search Results</h2><p>Found song matching your query</p>`;
    
    // Create song card
    const songCard = document.createElement('div');
    songCard.className = 'song-card';
    songCard.innerHTML = `
        <img src="${data.thumbnail || 'https://via.placeholder.com/300?text=No+Image'}" alt="${data.title}">
        <div class="play-icon">
            <i class="fas fa-play"></i>
        </div>
        <div class="song-info">
            <div class="song-title">${data.title}</div>
            <div class="song-duration">${formatDuration(data.duration)}</div>
        </div>
    `;
    
    // Add click event to play the song
    songCard.addEventListener('click', () => playSong(data));
    
    // Clear previous results and display new ones
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(songCard);
}

// Play selected song
function playSong(song) {
    // Update current song display
    currentSongDisplay.innerHTML = `
        <h2>Now Playing</h2>
        <p>${song.title}</p>
    `;
    
    // Update player
    playerContainer.className = 'player active';
    playerContainer.innerHTML = `
        <div class="song-details">
            <img class="song-thumbnail" src="${song.thumbnail || 'https://via.placeholder.com/300?text=No+Image'}" alt="${song.title}">
            <div class="song-title-artist">
                <div class="song-name">${song.title}</div>
                <div class="song-artist">YouTube Audio</div>
            </div>
        </div>
        <div class="controls">
            <audio controls autoplay src="${song.link}"></audio>
        </div>
    `;
    
    // Add to recent plays (could be expanded to save to localStorage)
    addToRecents(song);
}

// Add song to recent plays
function addToRecents(song) {
    // This function could be expanded to store recent plays in localStorage
    console.log('Added to recents:', song.title);
}

// Download a song (if needed)
async function downloadSong(videoId) {
    try {
        const response = await fetch(`${API_URL}/api/song/${videoId}`, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to download song');
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Download error:', error);
        throw error;
    }
}
