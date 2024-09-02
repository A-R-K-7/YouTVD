import subprocess

from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO, emit
import yt_dlp
import ffmpeg
import os
import eventlet
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)
DOWNLOAD_DIR = 'downloads'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


def download_video(url, download_type, resolution):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'format': 'bestvideo[height<={resolution}]+bestaudio/best',
        'noplaylist': True,
    }

    if download_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    else:
        # Ensure resolution is a valid integer string or set a default
        resolution = resolution if resolution and resolution.isdigit() else '720'
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Notify the client the download is complete
    socketio.emit('download_progress', {'progress': 100}, namespace='/download')

    # Optionally, return the path to the downloaded files
    info_dict = ydl.extract_info(url, download=False)
    return os.path.join(DOWNLOAD_DIR, f"{info_dict['title']}.mp4")


def merge_files(video_file, audio_file, output_file):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    subprocess.run(command, check=True)


def hook(d):
    if d['status'] == 'downloading':
        progress = {
            'downloaded_bytes': d.get('downloaded_bytes', 0),
            'total_bytes': d.get('total_bytes', 0)
        }
        socketio.emit('progress', progress)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    resolution = request.form['resolution']
    download_type = request.form['downloadType']
    only_audio = download_type == 'audio'

    thread = Thread(target=download_video, args=(url, resolution, only_audio))
    thread.start()

    return jsonify({'status': 'Download started'})


@app.route('/download/<filename>')
def serve_file(filename):
    return send_file(os.path.join(DOWNLOAD_DIR, filename), as_attachment=True)


if __name__ == '__main__':
    # Use eventlet with SocketIO
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
