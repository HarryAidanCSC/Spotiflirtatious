# 🎵 Spotiflirtatious

A real-time Spotify dashboard built with [Dash](https://dash.plotly.com/) that shows what you're currently listening to — complete with album art, a blurred background, and artist details.

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-2.18-00B4D8?logo=plotly&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify_API-1DB954?logo=spotify&logoColor=white)

---

## Features

- **Live playback tracking** — polls your Spotify account for the currently-playing track
- **Dynamic blurred background** — album art is fetched and Gaussian-blurred to create an immersive backdrop
- **Artist panel** — displays the lead artist's name and photo alongside the track
- **Auto-caching** — skips redundant API calls when the track hasn't changed

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | Dash, Plotly, HTML/CSS              |
| Backend   | Python, Spotipy, Pandas, Pillow     |
| Auth      | Spotify OAuth 2.0 (via Spotipy)     |

## Prerequisites

- **Python 3.13+**
- A **Spotify account** (free or premium)
- A **Spotify Developer application** — create one at [developer.spotify.com](https://developer.spotify.com/)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/ChuckleScriptCraft/Spotiflirtatious.git
   cd Spotiflirtatious
   ```

2. **Create a `.env` file** in the project root (see [`.env.example`](.env.example) for the template):

   ```
   SPOTIPY_CLIENT_ID='your_client_id_here'
   SPOTIPY_CLIENT_SECRET='your_client_secret_here'
   SPOTIPY_REDIRECT_URI='your_redirect_uri_here'
   ```

   > The redirect URI can be any valid URL (e.g. `http://localhost:8080`). It must match the one configured in your Spotify Developer Dashboard.

3. **Install dependencies** (using [Poetry](https://python-poetry.org/)):

   ```bash
   poetry install
   ```

4. **Run the app**

   ```bash
   poetry run python run.py
   ```

   The dashboard will be available at `http://127.0.0.1:8050`. On first launch, Spotify will open a browser window for OAuth authorisation.

## Project Structure

```
Spotiflirtatious/
├── app/
│   ├── assets/
│   │   ├── favicon.ico
│   │   ├── favicon.png
│   │   └── style.css          # Dashboard styles
│   ├── backend/
│   │   └── backend.py         # Spotify client, data fetching, image processing
│   └── app.py                 # Dash layout and callbacks
├── .env.example                # Environment variable template
├── .gitignore
├── pyproject.toml              # Project metadata and dependencies
├── poetry.lock
├── run.py                      # Application entry point
└── README.md
```