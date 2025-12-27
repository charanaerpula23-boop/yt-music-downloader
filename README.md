# YouTube Music Downloader

A sleek web application to search and download music from YouTube Music with preview functionality.

## Features

- 🔍 Search songs from YouTube Music
- 🎵 Preview songs before downloading
- ⬇️ Download in M4A or WebM format
- 🎨 Minimalist black & white UI
- 📱 Responsive design
- 🍪 Multiple authentication strategies with cookie support

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

## Cookie Authentication (Optional)

If you encounter "Sign in to confirm you're not a bot" errors, you can add cookies for authentication:

### Method 1: Export cookies.txt file
1. Install browser extension "Get cookies.txt LOCALLY" for [Chrome](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
2. Go to YouTube Music (music.youtube.com) and sign in
3. Click the extension icon and export cookies
4. Save the file as `cookies.txt` in the project root directory
5. Restart the application

### Method 2: Auto-detect browser cookies
The app will automatically try to use cookies from Chrome and Firefox if available on the server.

## Deployment to Render

1. Push to GitHub
2. Connect repository to Render
3. Render will auto-deploy using `render.yaml`
4. (Optional) Upload `cookies.txt` via Render dashboard for authentication

## How It Works

The app uses a multi-strategy fallback system:
1. Cookie-based authentication (if cookies.txt exists)
2. Android embedded client
3. iOS client
4. TV embedded client  
5. Web client with enhanced headers
6. Browser cookies (Chrome/Firefox)

One of these strategies will work to bypass restrictions!

## Note

- Downloads are stored in the `downloads/` directory
- Preview feature works best with cookie authentication
- Some videos may require authentication depending on YouTube's restrictions
