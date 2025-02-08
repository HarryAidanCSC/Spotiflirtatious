import dash
from dash import html, callback
from dash.dependencies import Input, Output, State
from app.backend.backend import create_spotify_client, usr_current_playback, blur_image


# Get spotify client
sp = create_spotify_client()

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                # Background div with the background image
                html.Div(
                    id="background-div",
                    style={
                        "backgroundImage": "url(data:image/jpeg;base64, YOUR_BASE64_ENCODED_IMAGE)",  # Update background with base64 image
                        "background-size": "cover",
                        "background-position": "center",
                        "height": "100vh",  # Take up full viewport height
                        "width": "100%",  # Take up full viewport width
                        "position": "absolute",  # Absolute position to fill the viewport
                        "top": 0,  # Align it at the top
                        "left": 0,  # Align it at the left
                        "z-index": -1,  # Ensure background is behind the content
                        "border": "none",
                        "margin": "0",  # Remove any margin
                        "padding": "0",  # Remove any padding
                    },
                ),
                # Heading text positioned over the background
                html.H1(
                    "What are you currently playing?",
                    className="heading-text",
                ),
                # Button to refresh the image
                html.Button(
                    "Click to refresh",
                    id="submit-val",
                    n_clicks=0,
                    className="refresh-button",
                ),
                # Track name
                html.P(id="track-name", children="", className="track-name"),
                # The main album art image positioned on top of the background
                html.Img(
                    id="track-img",
                    src="",
                    className="album-art-image",
                ),
            ],
            className="main-div",
        ),
        # Artist Information Section
        html.Div(
            [
                html.H2("Main Artist", id="Artist block"),
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
    ],
    Input("submit-val", "n_clicks"),
    State("background-div", "style"),
)
def update_output(n_clicks, current_style):
    # Ignore the n_clicks value, just refresh the image
    track_df, artist_df = usr_current_playback(sp)
    img_url = track_df["track_img_href"][0]

    img_base64 = blur_image(img_url)

    # Get Track Name
    track_name = track_df["track_name"][0]

    updated_style = current_style.copy()  # Make a copy of the current style
    updated_style["backgroundImage"] = (
        f"url(data:image/jpeg;base64,{img_base64})"  # Update backgroundImage
    )

    # Get artist's name (lead)
    artist_name = artist_df["artist_name"][0]

    # Get artist's image (lead)
    artist_url = artist_df["artist_img_href"][0]

    # Return the updated values
    return img_url, track_name, updated_style, artist_name, artist_url
