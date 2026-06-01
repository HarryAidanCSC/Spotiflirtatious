"""Spotify API client and data-fetching utilities."""

import base64
from io import BytesIO

import pandas as pd
import requests
import spotipy
from dotenv import load_dotenv
from PIL import Image, ImageFilter
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_SCOPES = [
    "user-library-read",
    "user-read-private",
    "user-read-playback-state",
    "user-read-email",
]


def create_spotify_client() -> spotipy.Spotify:
    """Authenticate with Spotify and return an authorised client."""
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SPOTIFY_SCOPES))


def get_current_playback(sp: spotipy.Spotify) -> tuple[pd.DataFrame, pd.DataFrame] | tuple[None, None]:
    """Fetch the user's currently-playing track and artist metadata.

    Returns a (track_df, artist_df) tuple, or (None, None) when nothing is playing.
    """
    playback = sp.current_playback()

    if not (playback and playback.get("is_playing") and playback.get("item")):
        return None, None

    track = playback["item"]

    # --- Track info ---
    track_img_url = track["album"]["images"][0]["url"] if track["album"]["images"] else None
    track_df = pd.DataFrame({
        "track_name": [track["name"]],
        "track_href": [track["external_urls"]["spotify"]],
        "track_img_href": [track_img_url],
    })

    # --- Artist info (one row per credited artist) ---
    artist_rows = []
    for artist_stub in track["artists"]:
        info = sp.artist(artist_stub["id"])
        artist_rows.append({
            "artist_name": artist_stub["name"],
            "artist_id": artist_stub["id"],
            "artist_img_href": info["images"][0]["url"] if info["images"] else None,
            "artist_href": info["external_urls"]["spotify"],
        })

    artist_df = pd.DataFrame(artist_rows)
    return track_df, artist_df


def blur_image(img_url: str, radius: int = 20) -> str:
    """Download an image, apply a Gaussian blur, and return it as a base64-encoded JPEG."""
    response = requests.get(img_url, timeout=10)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    blurred = image.filter(ImageFilter.GaussianBlur(radius=radius))

    buffer = BytesIO()
    blurred.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
