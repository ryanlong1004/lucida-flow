<div align="center">
  <img src="lucida_flow.png" alt="Lucida Flow Logo" width="600"/>
  
  # Lucida Flow
  
  A Python CLI tool and REST API for downloading high-quality music from various streaming services using [Lucida.to](https://lucida.to), with Amazon Music as the default service.
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![GitHub Stars](https://img.shields.io/github/stars/ryanlong1004/lucida-flow.svg)](https://github.com/ryanlong1004/lucida-flow/stargazers)
  
</div>

## Features

- 🎵 **Amazon Music Focus**: Optimized for Amazon Music with fallback support for other services
- 🔍 **Search Functionality**: Search for tracks across multiple services
- 💻 **CLI Tool**: Easy-to-use command-line interface with beautiful output
- 🌐 **REST API**: FastAPI-based HTTP API for integration
- 🕷️ **Web Scraping**: No service credentials required - uses Lucida.to's web interface
- 📦 **High Quality**: Download in FLAC, MP3, AAC, and other formats
- 🎨 **Beautiful Output**: Rich terminal formatting with colored tables

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Quick Start

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Install Playwright browsers (required for downloads):**

```bash
playwright install chromium
```

3. **Try the CLI:**

```bash
# Search uses Amazon Music by default
python cli.py search "hotel california"
python cli.py search "daft punk" --limit 5

# List available services
python cli.py services
```

4. **Start the API:**

```bash
python api_server.py
# Visit http://localhost:8000/docs for interactive API documentation
```

## CLI Usage

### Search for Music

```bash
# Search Amazon Music (default)
python cli.py search "hotel california"
python cli.py search "shape of you" --limit 5

# Search other services
python cli.py search "daft punk get lucky" --service tidal
python cli.py search "album name" -s qobuz
```

### Download Music

```bash
python cli.py download "https://tidal.com/browse/track/123456"
python cli.py download "https://open.qobuz.com/track/123456" -o ./my-music/song.flac
```

### Get Track Information

```bash
python cli.py info "https://tidal.com/browse/track/123456"
```

### List Available Services

```bash
python cli.py services
```

## API Usage

### Start Server

```bash
python api_server.py
```

API docs: `http://localhost:8000/docs`

### Example Requests

**Search:**

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "daft punk", "service": "tidal", "limit": 5}'
```

**Download:**

```bash
curl -X POST http://localhost:8000/download-file \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tidal.com/browse/track/123456"}' \
  --output track.flac
```

See full documentation in [DOCUMENTATION.md](DOCUMENTATION.md)

## Project Structure

```
lucida_flow/
├── lucida_client.py        # Core web scraping client
├── cli.py                  # CLI application
├── api_server.py           # FastAPI server
├── requirements.txt        # Dependencies
├── .env                    # Configuration (optional)
└── downloads/              # Default download directory
```

## Configuration (Optional)

Create `.env` file:

```env
DOWNLOAD_DIR=./downloads
API_HOST=0.0.0.0
API_PORT=8000
LUCIDA_BASE_URL=https://lucida.to
REQUEST_TIMEOUT=30
```

## How It Works

This tool uses browser automation (Playwright) to interact with Lucida.to's web interface for downloads, and web scraping for search. No service credentials required!

**Technical Details:**

- **Search**: Uses HTTP requests + BeautifulSoup to parse Lucida.to search results
- **Downloads**: Uses Playwright to automate a headless Chrome browser that clicks the download button on Lucida.to
- **Rate Limiting**: Enterprise-grade sliding window algorithm (30 req/min, 500 req/hour, 2s min delay)

## Disclaimer

For educational and personal use only. Respect copyright laws and terms of service.

## Credits

- Built for [Lucida.to](https://lucida.to)
- Lucida library by [hazycora](https://hazy.gay/)

## License

MIT License
