# YouTube Music Downloader

A sleek web application to search and download music from YouTube Music with preview functionality.

## Features

- 🔍 Search songs from YouTube Music
- 🎵 Preview songs before downloading
- ⬇️ Download in M4A or WebM format
- 🎨 Minimalist black & white UI
- 📱 Responsive design

## Tech Stack

- Backend: Flask + ytmusicapi + yt-dlp
- Frontend: Vanilla JavaScript
- Deployment: Render

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open http://localhost:5000

## Deployment

This app is configured for Render deployment. Simply:

1. Push to GitHub
2. Connect to Render
3. Deploy automatically

## Note

Downloads are stored in the `downloads/` directory on the server.
