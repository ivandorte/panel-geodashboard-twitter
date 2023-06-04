import holoviews as hv
from bokeh.models import HoverTool


def get_tweet_points(in_data):
    """
    Returns a rasterized graph of tweet locations.
    """

    # Define a custom Hover tool for the points
    points_hover = HoverTool(
        tooltips=[("tweets", "@image")],
    )

    # Plot the tweet locations, apply rasterization and dynspread
    out_points = in_data.hvplot.points(
        x="x",
        y="y",
        xaxis=None,
        yaxis=None,
        rasterize=True,
        dynspread=True,
        cmap="viridis",
        cnorm="eq_hist",
        colorbar=False,
        tools=[points_hover],
        frame_width=600,
        frame_height=400,
    )

    return out_points


def get_tweet_map(tweet_points):
    """
    This function combines the rasterized
    tweet locations with CartoDark tiles.
    """

    # Get the CartoDark tiles
    carto_tiles = hv.element.tiles.CartoDark()

    # Combine the tweet locations with CartoDark tiles
    tweet_map = carto_tiles * tweet_points
    return tweet_map
