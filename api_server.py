"""
Lucida Flow API Server
FastAPI REST API for Lucida.to music downloads
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import os
from dotenv import load_dotenv
from lucida_client import LucidaClient
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lucida Flow API",
    description="REST API for downloading music via Lucida.to",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global client instance
lucida_client = LucidaClient()


# Request/Response Models
class SearchRequest(BaseModel):
    query: str
    service: str
    limit: Optional[int] = 10


class TrackInfoRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    output_path: Optional[str] = None


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Lucida Flow API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "GET /services": "List available services",
            "POST /search": "Search for music",
            "POST /info": "Get track information",
            "POST /download": "Download track",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Lucida Flow API",
        "base_url": lucida_client.base_url,
    }


@app.get("/services")
async def get_services():
    """Get list of available streaming services"""
    services = lucida_client.get_available_services()
    return {"services": services, "count": len(services)}


@app.post("/search")
async def search(request: SearchRequest):
    """
    Search for music on a specific streaming service

    - **query**: Search query string
    - **service**: Music service (tidal, qobuz, spotify, deezer, soundcloud, amazon_music, yandex_music)
    - **limit**: Maximum number of results (default: 10)
    """
    try:
        results = lucida_client.search(
            request.query, service=request.service, limit=request.limit or 10
        )

        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/info")
async def get_track_info(request: TrackInfoRequest):
    """
    Get detailed information about a track

    - **url**: URL to the track (from Tidal, Qobuz, Spotify, etc.)
    """
    try:
        info = lucida_client.get_track_info(request.url)

        if "error" in info:
            raise HTTPException(status_code=500, detail=info["error"])

        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download")
async def download_track(request: DownloadRequest):
    """
    Download a track and return file information

    - **url**: URL to the track
    - **output_path**: Optional output path for the file
    """
    try:
        result = lucida_client.download_track(
            request.url, output_path=request.output_path
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=500, detail=result.get("error", "Download failed")
            )

        return {
            "success": True,
            "filepath": result["filepath"],
            "size": result["size"],
            "size_mb": round(result["size"] / 1024 / 1024, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download-file")
async def download_track_file(request: DownloadRequest):
    """
    Download a track and return the audio file directly

    - **url**: URL to the track
    """
    try:
        # Download to temporary location
        result = lucida_client.download_track(request.url)

        if not result.get("success"):
            raise HTTPException(
                status_code=500, detail=result.get("error", "Download failed")
            )

        filepath = result["filepath"]

        # Read file content
        with open(filepath, "rb") as f:
            content = f.read()

        # Determine content type
        if filepath.endswith(".flac"):
            media_type = "audio/flac"
        elif filepath.endswith(".mp3"):
            media_type = "audio/mpeg"
        elif filepath.endswith(".m4a"):
            media_type = "audio/mp4"
        else:
            media_type = "application/octet-stream"

        filename = os.path.basename(filepath)

        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    print(f"Starting Lucida Flow API on {host}:{port}")
    print(f"API Documentation: http://{host}:{port}/docs")

    uvicorn.run(app, host=host, port=port)
