# YouTube Video Downloader and Converter

This project is a web application built using Flask and SocketIO that allows users to download and convert YouTube videos to MP4 format. It supports both single video downloads and playlists.

## Features

- **Download**: Directly download YouTube videos or playlists.
- **Conversion**: Convert downloaded files to MP4 format using ffmpeg.
- **Move to Downloads**: Automatically move the converted MP4 file to the user's system Downloads folder.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask (`pip install Flask`)
- Flask-SocketIO (`pip install flask-socketio`)
- yt-dlp (`pip install yt-dlp`)
- ffmpeg (for video conversion)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your/repository.git
   cd repository
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

1. Enter the YouTube video URL and select options (resolution, download type).
2. Click on the download button.
3. The application will download, convert (if necessary), and move the file to your system's Downloads folder.

## Configuration

- `DOWNLOAD_DIR`: Specifies the directory where downloaded files are temporarily stored.
- `ffmpeg`: Ensure ffmpeg is installed and accessible in your PATH for video conversion.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
