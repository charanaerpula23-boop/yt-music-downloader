from flask import Flask, render_template, request, jsonify, send_file
from ytmusicapi import YTMusic
import yt_dlp
import re
import os
from pathlib import Path

app = Flask(__name__)
ytmusic = YTMusic()

# Create downloads directory
DOWNLOADS_DIR = Path('downloads')
DOWNLOADS_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json.get('query', '')
        if not query:
            return jsonify({'error': 'Please enter a search query'}), 400
        
        # Search for songs
        results = ytmusic.search(query, filter='songs', limit=20)
        
        # Format the results
        songs = []
        for item in results:
            # Get the highest quality thumbnail (last in array is usually highest res)
            thumbnails = item.get('thumbnails', [])
            thumbnail_url = ''
            if thumbnails:
                # Get the largest thumbnail
                thumbnail_url = max(thumbnails, key=lambda x: x.get('width', 0) * x.get('height', 0)).get('url', '')
                
                # Replace size parameters with high quality settings
                # YouTube Music uses parameters like =w60-h60, replace with =w600-h600 or remove them
                thumbnail_url = re.sub(r'=w\d+-h\d+', '=w600-h600', thumbnail_url)
                # If no size parameter exists, add one
                if '=' not in thumbnail_url.split('/')[-1]:
                    thumbnail_url += '=w600-h600'
            
            song = {
                'title': item.get('title', 'Unknown'),
                'artist': ', '.join([artist['name'] for artist in item.get('artists', [])]) if item.get('artists') else 'Unknown Artist',
                'album': item.get('album', {}).get('name', 'Unknown Album') if item.get('album') else 'Unknown Album',
                'duration': item.get('duration', 'N/A'),
                'thumbnail': thumbnail_url,
                'videoId': item.get('videoId', '')
            }
            songs.append(song)
        
        return jsonify({'songs': songs})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        video_id = request.json.get('videoId', '')
        title = request.json.get('title', 'song')
        format_type = request.json.get('format', 'm4a')
        
        if not video_id:
            return jsonify({'error': 'Video ID is required'}), 400
        
        # Clean filename
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        
        # yt-dlp options based on format
        if format_type == 'm4a':
            format_selector = 'bestaudio[ext=m4a]/bestaudio'
        else:  # webm
            format_selector = 'bestaudio[ext=webm]/bestaudio'
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': str(DOWNLOADS_DIR / f'{safe_title}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        # Download the song
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://music.youtube.com/watch?v={video_id}', download=True)
            downloaded_file = ydl.prepare_filename(info)
        
        # Get the actual filename
        filename = os.path.basename(downloaded_file)
        
        return jsonify({
            'success': True,
            'message': f'Downloaded: {filename}',
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview():
    try:
        video_id = request.json.get('videoId', '')
        
        if not video_id:
            return jsonify({'error': 'Video ID is required'}), 400
        
        # Extract audio stream URL using yt-dlp
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://music.youtube.com/watch?v={video_id}', download=False)
            
            # Get the direct audio URL
            audio_url = info.get('url', '')
            
            if not audio_url:
                return jsonify({'error': 'Could not extract audio URL'}), 500
        
        return jsonify({
            'success': True,
            'streamUrl': audio_url
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
