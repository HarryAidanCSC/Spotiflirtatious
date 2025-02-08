# %% Load modules
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import sys
import pandas as pd
import base64
import requests
from PIL import Image, ImageFilter
from io import BytesIO


# Generate spotify client with pre-defined scope
def create_spotify_client():
    root = os.path.abspath(os.path.join(os.getcwd(), ".."))
    sys.path.insert(2, root)

    # Load the .env file
    load_dotenv()

    # Create a Spotify client
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=[
                "user-library-read",
                "user-read-private",
                "user-read-playback-state",
                "user-read-email",
            ]
        )
    )
    return sp


# Get current playback info
def usr_current_playback(sp):

    # Get current playback info
    current_playback = sp.current_playback()

    # If track is playing call API
    if (
        current_playback
        and current_playback.get("is_playing")
        and current_playback["item"]
    ):

        # ---------- Get Track Info ---------- #
        track = current_playback["item"]

        # Link to track
        track_img_url = (
            track["album"]["images"][0]["url"] if track["album"]["images"] else None
        )

        # Create DF for track info
        track_df = pd.DataFrame(
            {
                "track_name": [track["name"]],
                "track_href": [track["external_urls"]["spotify"]],
                "track_img_href": [track_img_url],
            }
        )

        # ---------- Get Artist Info ---------- #
        artists = {c["name"]: c["id"] for c in current_playback["item"]["artists"]}

        # Initialise DF for artist info
        artist_df = pd.DataFrame(
            columns=["artist_name", "artist_id", "artist_img_href", "artist_href"]
        )

        # Loop through artists
        for i, (artist, artist_id) in enumerate(artists.items()):
            # Get info from artist
            artist_info = sp.artist(artist_id)

            # Get image url
            img_url = artist_info["images"][0]["url"] if artist_info["images"] else None

            # Get artist url
            artist_url = artist_info["external_urls"]["spotify"]

            # Create new row
            new_row = [artist, artist_id, img_url, artist_url]
            artist_df.loc[i] = new_row  # Append to existing DF

        return track_df, artist_df
    else:
        return None, None


def blur_image(img_url):
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))

    # Apply Gaussian Blur
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=20))

    # Save the blurred image to a buffer
    buffered = BytesIO()
    blurred_image.save(buffered, format="JPEG")
    # Encode the image as base64
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_base64
