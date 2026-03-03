# Music Downloader

A desktop application to download music from Spotify and YouTube as high-quality MP3 files.

---

## Features

- ✅ Download individual tracks from Spotify and YouTube
- ✅ Download entire playlists (Spotify & YouTube)
- ✅ Automatic metadata extraction (artist, title, album)
- ✅ Clean filename format: `Artist - Title.mp3`
- ✅ Modern dark-themed GUI
- ✅ Background downloading with progress tracking

---

## Prerequisites

- **Python 3.10+**
- **ffmpeg** (for audio conversion)
- **Spotify API credentials** (free from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard))

---

## Installation

### Method 1: Python Desktop App (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/music-download.git
cd music-download

# Install ffmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure Spotify API
cp .env.example .env
# Edit .env and add your credentials:
# SPOTIFY_CLIENT_ID=your_client_id
# SPOTIFY_CLIENT_SECRET=your_client_secret

# Run application
python desktop_app.py
```

### Method 2: Docker

```bash
# Clone repository
git clone https://github.com/yourusername/music-download.git
cd music-download

# Configure Spotify API
cp .env.example .env
# Edit .env with your credentials

# Start services
docker-compose up -d

# Access web interface at http://localhost:8000
```

---

## Usage

### Desktop App (PyQt6)

1. Launch: `python desktop_app.py`
2. Paste Spotify or YouTube URL
3. Click "Download"
4. Files saved to: `~/Music/Music Downloader/`

### Docker (Web Interface)

1. Navigate to `http://localhost:8000`
2. Submit download URL via API
3. Files saved in Docker volume

---

## Supported URLs

```bash
# Spotify
https://open.spotify.com/track/...       # Single track
https://open.spotify.com/playlist/...    # Playlist

# YouTube
https://youtube.com/watch?v=...          # Single video
https://youtube.com/playlist?list=...    # Playlist
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.12 |
| **Desktop GUI** | PyQt6 |
| **Web API** | FastAPI (Docker only) |
| **Task Queue** | Celery + Redis (Docker only) |
| **Spotify API** | spotipy |
| **YouTube** | yt-dlp |
| **Audio Processing** | ffmpeg |
| **Data Validation** | Pydantic |

---

## Project Structure

```
music-download/
├── app/
│   ├── gui/
│   │   └── main_window.py       # PyQt6 desktop app
│   ├── services/
│   │   ├── spotify_service.py   # Spotify API client
│   │   └── youtube_service.py   # YouTube downloader
│   ├── utils/
│   │   └── downloader.py        # yt-dlp wrapper
│   └── models.py                # Data models
├── desktop_app.py               # Desktop launcher
├── main.py                      # FastAPI server (Docker)
├── docker-compose.yml           # Docker setup
├── requirements.txt             # Python dependencies
└── .env                         # API credentials
```

---

## Getting Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in and click **"Create app"**
3. Fill in app details:
   - **App name**: Music Downloader
   - **Redirect URI**: `http://localhost:8888/callback`
4. Copy **Client ID** and **Client Secret**
5. Paste into `.env` file

---

## Configuration

Create a `.env` file in the project root:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

---

## Dependencies

```txt
# GUI (Desktop App)
PyQt6==6.6.1

# Spotify Integration
spotipy==2.23.0
python-dotenv==1.0.0

# YouTube & Download
yt-dlp==2023.12.30
requests==2.31.0
beautifulsoup4==4.12.2

# Web API (Docker only)
fastapi==0.104.1
celery==5.3.4
redis==5.0.1

# Data Validation
pydantic==2.5.0
```

---

## Troubleshooting

### FFmpeg not found

```bash
# Install ffmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS
```

### Spotify API errors

- Verify credentials in `.env` file
- Check credentials at [Spotify Dashboard](https://developer.spotify.com/dashboard)

### PyQt6 installation issues

```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install PyQt6
```

---

## License

Creative Commons Attribution-NonCommercial 4.0 International Public License (see [LICENSE](LICENSE) file)

---

## Contributing

Pull requests are welcome! Please ensure your code follows the existing style.