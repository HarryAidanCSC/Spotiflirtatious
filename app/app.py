"""Dash application layout and callbacks for the Spotiflirtatious dashboard."""

import dash
from dash import html, callback, dcc
from dash.dependencies import Input, Output, State

from app.backend.backend import create_spotify_client, get_current_playback, blur_image

MAX_TRACK_NAME_LENGTH = 52

sp = create_spotify_client()

app = dash.Dash(__name__, title="Spotiflirtatious")

BACKGROUND_STYLE = {
    "backgroundImage": "none",
    "backgroundSize": "cover",
    "backgroundPosition": "center",
    "height": "100vh",
    "width": "100%",
    "position": "absolute",
    "top": 0,
    "left": 0,
    "zIndex": -1,
    "border": "none",
    "margin": "0",
    "padding": "0",
}

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(id="background-div", style=BACKGROUND_STYLE),
                html.H1("What are you currently playing?", className="heading-text"),
                html.Button("Refresh", id="refresh-button", className="refresh-button"),
                dcc.Store(id="track-id", data=[]),
                html.P(id="track-name", children="", className="track-name"),
                html.Img(id="track-img", src="", className="album-art-image"),
            ],
            className="main-div",
        ),
        html.Div(
            [
                html.H2("Main Artist", id="artist-block"),
                html.P(id="artist-name", children=""),
                html.Img(id="artist-img", src=""),
            ],
            className="artist-div",
        ),
    ]
)


@callback(
    [
        Output("track-img", "src"),
        Output("track-name", "children"),
        Output("background-div", "style"),
        Output("artist-name", "children"),
        Output("artist-img", "src"),
        Output("track-id", "data"),
    ],
    [
        Input("refresh-button", "n_clicks"),
        Input("track-id", "data"),
    ],
    State("background-div", "style"),
)
def update_output(_n_clicks, cached_state, current_style):
    """Refresh the dashboard with the currently-playing track."""
    track_df, artist_df = get_current_playback(sp)

    if track_df is None:
        return dash.no_update

    img_url = track_df["track_img_href"].iloc[0]
    prev_img_url = cached_state[0] if cached_state else ""

    if img_url == prev_img_url:
        # Track hasn't changed - return cached values
        return (
            cached_state[0],
            cached_state[1],
            cached_state[2],
            cached_state[3],
            cached_state[4],
            cached_state,
        )

    # New track — fetch fresh data
    img_base64 = blur_image(img_url)

    track_name = track_df["track_name"].iloc[0]
    if len(track_name) > MAX_TRACK_NAME_LENGTH:
        track_name = track_name[:MAX_TRACK_NAME_LENGTH] + "..."

    updated_style = {
        **current_style,
        "backgroundImage": f"url(data:image/jpeg;base64,{img_base64})",
    }

    artist_name = artist_df["artist_name"].iloc[0]
    artist_url = artist_df["artist_img_href"].iloc[0]

    new_state = [img_url, track_name, updated_style, artist_name, artist_url]

    return (img_url, track_name, updated_style, artist_name, artist_url, new_state)
