from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import requests
from urllib.parse import urlparse

app = Flask(__name__)

def download_tiktok(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return {
                'success': True,
                'path': ydl.prepare_filename(info),
                'title': info['title']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

def download_youtube(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return {
                'success': True,
                'path': ydl.prepare_filename(info),
                'title': info['title']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

def download_instagram(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return {
                'success': True,
                'path': ydl.prepare_filename(info),
                'title': info['title']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    domain = urlparse(url).netloc
    
    if 'tiktok.com' in domain:
        result = download_tiktok(url)
    elif 'youtube.com' in domain or 'youtu.be' in domain:
        result = download_youtube(url)
    elif 'instagram.com' in domain:
        result = download_instagram(url)
    else:
        return jsonify({'success': False, 'error': 'Unsupported platform'})

    if result['success']:
        return jsonify({
            'success': True,
            'download_path': result['path'],
            'title': result['title']
        })
    else:
        return jsonify({'success': False, 'error': result['error']})

@app.route('/get-video/<path:filename>')
def get_video(filename):
    try:
        file_path = os.path.join(os.getcwd(), filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
