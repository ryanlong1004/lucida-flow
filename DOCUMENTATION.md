# Lucida Flow - Complete Documentation

## Table of Contents

- [Installation](#installation)
- [CLI Usage](#cli-usage)
- [API Usage](#api-usage)
- [API Examples](#api-examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Installation

### Requirements

- Python 3.8+
- pip

### Install

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install separately
pip install -r requirements-cli.txt  # CLI only
pip install -r requirements-api.txt  # API only
```

## CLI Usage

### Commands

#### search

Search for music on a specific service

```bash
python cli.py search "query" --service SERVICE [--limit NUMBER]
```

Available services: `tidal`, `qobuz`, `spotify`, `deezer`, `soundcloud`, `amazon_music`, `yandex_music`

Examples:

```bash
python cli.py search "daft punk get lucky" --service tidal
python cli.py search "radiohead" --service spotify --limit 20
python cli.py search "pink floyd dark side" -s qobuz
```

#### download

Download a track from URL

```bash
python cli.py download URL [--output PATH]
```

Examples:

```bash
python cli.py download "https://tidal.com/browse/track/123456"
python cli.py download "https://open.qobuz.com/track/123456" --output ./music/song.flac
python cli.py download "https://open.spotify.com/track/123456" -o downloads/track.mp3
```

#### info

Get detailed track information

```bash
python cli.py info URL
```

Example:

```bash
python cli.py info "https://tidal.com/browse/track/123456"
```

#### services

List available streaming services

```bash
python cli.py services
```

#### config

Show current configuration

```bash
python cli.py config
```

### Make CLI Executable (Optional)

```bash
chmod +x cli.py
./cli.py search "your query"
```

## API Usage

### Starting the Server

```bash
python api_server.py
```

Server will run on `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

### API Endpoints

#### GET /

Root endpoint - API information

Response:

```json
{
  "name": "Lucida Flow API",
  "version": "1.0.0",
  "endpoints": {
    "GET /health": "Health check",
    "GET /services": "List available services",
    "POST /search": "Search for music",
    "POST /info": "Get track information",
    "POST /download": "Download track"
  }
}
```

#### GET /health

Health check

Response:

```json
{
  "status": "healthy",
  "service": "Lucida Flow API",
  "base_url": "https://lucida.to"
}
```

#### GET /services

List available streaming services

Response:

```json
{
  "services": [
    "tidal",
    "qobuz",
    "spotify",
    "deezer",
    "soundcloud",
    "amazon_music",
    "yandex_music"
  ],
  "count": 7
}
```

#### POST /search

Search for music

Request:

```json
{
  "query": "search term",
  "service": "tidal",
  "limit": 10
}
```

Response:

```json
{
  "query": "daft punk",
  "service": "tidal",
  "tracks": [
    {
      "name": "Get Lucky",
      "artist": "Daft Punk",
      "album": "Random Access Memories",
      "url": "https://..."
    }
  ],
  "albums": [],
  "artists": []
}
```

#### POST /info

Get track information

Request:

```json
{
  "url": "https://tidal.com/browse/track/123456"
}
```

Response:

```json
{
  "url": "https://tidal.com/browse/track/123456",
  "name": "Track Name",
  "artist": "Artist Name",
  "album": "Album Name",
  "duration": 240,
  "quality": "FLAC"
}
```

#### POST /download

Download track and get file info

Request:

```json
{
  "url": "https://tidal.com/browse/track/123456",
  "output_path": "./downloads/song.flac"
}
```

Response:

```json
{
  "success": true,
  "filepath": "./downloads/song.flac",
  "size": 12345678,
  "size_mb": 11.77
}
```

#### POST /download-file

Download track and return file

Request:

```json
{
  "url": "https://tidal.com/browse/track/123456"
}
```

Response: Binary audio file (Content-Type: audio/flac, audio/mpeg, or audio/mp4)

## API Examples

### cURL Examples

**Search:**

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "daft punk", "service": "tidal", "limit": 5}'
```

**Get info:**

```bash
curl -X POST http://localhost:8000/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tidal.com/browse/track/123456"}'
```

**Download (save info):**

```bash
curl -X POST http://localhost:8000/download \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tidal.com/browse/track/123456"}'
```

**Download (get file):**

```bash
curl -X POST http://localhost:8000/download-file \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tidal.com/browse/track/123456"}' \
  --output track.flac
```

### Python Examples

```python
import requests

# Search
response = requests.post('http://localhost:8000/search', json={
    'query': 'daft punk',
    'service': 'tidal',
    'limit': 10
})
results = response.json()
print(f"Found {len(results['tracks'])} tracks")

# Get track info
response = requests.post('http://localhost:8000/info', json={
    'url': 'https://tidal.com/browse/track/123456'
})
track_info = response.json()
print(f"Track: {track_info['name']} by {track_info['artist']}")

# Download track
response = requests.post('http://localhost:8000/download-file', json={
    'url': 'https://tidal.com/browse/track/123456'
})
with open('track.flac', 'wb') as f:
    f.write(response.content)
print("Downloaded successfully")
```

### JavaScript/TypeScript Examples

```javascript
// Search
const searchResponse = await fetch("http://localhost:8000/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "daft punk", service: "tidal", limit: 10 }),
});
const searchResults = await searchResponse.json();
console.log(`Found ${searchResults.tracks.length} tracks`);

// Get track info
const infoResponse = await fetch("http://localhost:8000/info", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "https://tidal.com/browse/track/123456",
  }),
});
const trackInfo = await infoResponse.json();
console.log(`Track: ${trackInfo.name} by ${trackInfo.artist}`);

// Download track
const downloadResponse = await fetch("http://localhost:8000/download-file", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "https://tidal.com/browse/track/123456",
  }),
});
const audioBlob = await downloadResponse.blob();
// Save or play the blob
```

## Configuration

Create a `.env` file (optional):

```env
# Download directory
DOWNLOAD_DIR=./downloads

# API server settings
API_HOST=0.0.0.0
API_PORT=8000

# Lucida.to settings
LUCIDA_BASE_URL=https://lucida.to
REQUEST_TIMEOUT=30

# Rate limiting (seconds between requests)
RATE_LIMIT_DELAY=1.0
```

## Troubleshooting

### Installation Issues

**Module not found:**

```bash
pip install -r requirements.txt
```

**Permission denied:**

```bash
pip install --user -r requirements.txt
```

### Download Issues

**Download fails:**

- Verify the URL is valid and supported
- Check internet connection
- Lucida.to may be temporarily unavailable
- Try again in a few minutes

**File write errors:**

- Ensure you have write permissions in the download directory
- Check available disk space
- Try specifying a different output path

### API Issues

**Port already in use:**

```bash
# Change port in .env
API_PORT=8001
```

**Cannot access API:**

- Check firewall settings
- Verify the server is running
- Try accessing via 127.0.0.1 instead of localhost

### Rate Limiting

The client includes automatic rate limiting (1 second between requests). If you still encounter rate limit errors:

- Reduce request frequency
- Wait a few minutes before retrying
- Lucida.to may have additional rate limiting

### Web Scraping Issues

**Parsing errors:**

- Lucida.to's HTML structure may have changed
- Report the issue with details
- Wait for an update to the scraping logic

**No results found:**

- Try a different search query
- The service may not have indexed that content
- Try searching on Lucida.to directly to verify

## Development

### Running in Development

**CLI:**

```bash
python cli.py search "test"
```

**API with auto-reload:**

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure

```
lucida_flow/
├── lucida_client.py        # Core scraping client
├── cli.py                  # CLI application
├── api_server.py           # FastAPI REST API
├── requirements.txt        # All dependencies
├── requirements-cli.txt    # CLI only
├── requirements-api.txt    # API only
├── .env                    # Configuration
├── .gitignore
├── README.md
└── DOCUMENTATION.md        # This file
```

## Legal & Ethics

### Disclaimer

This tool is for **educational and personal use only**. Users must:

- Respect Lucida.to's terms of service
- Respect streaming platforms' terms of service
- Comply with copyright laws in their jurisdiction
- Not use for commercial purposes or redistribution

### Ethical Use

- Download only content you have rights to access
- Support artists by purchasing music when possible
- Use for personal archival/backup only
- Do not share or redistribute downloaded content

## Support

- **Issues**: Check existing issues or create a new one
- **Lucida.to**: [Discord](https://lucida.to/discord) | [Telegram](https://lucida.to/telegram)
- **Documentation**: This file and README.md

## Notes

### Web Scraping Limitations

- May break if Lucida.to changes their website structure
- Less robust than using official Lucida library
- Performance may vary
- Some features may be limited

### Alternative

If you have service API credentials, consider using the official [Lucida library](https://git.gay/lucida/lucida) for more robust functionality.
