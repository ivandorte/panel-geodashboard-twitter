import holoviews as hv
import hvplot.pandas
from bokeh.models import HoverTool


def get_tweet_points(in_data):
    '''
    Returns a rasterized graph of tweet locations.
    '''

    # Define a custom Hover tool for the points
    points_hover = HoverTool(
        tooltips=[('Tweets', '@image')],
        point_policy="follow_mouse"
        )

    # Plot the tweet locations, apply rasterization and dynspread
    out_points = in_data.hvplot.points(x='x',
                                       y='y',
                                       rasterize=True,
                                       dynspread=True,
                                       cmap='viridis',
                                       cnorm='eq_hist',
                                       tools=[points_hover],
                                       responsive=True,
                                       min_height=300
                                       )

    # Additional plot options
    out_points.opts(xaxis=None,
                    yaxis=None,
                    active_tools=['wheel_zoom']
                    )
    return out_points


def get_tweet_map(tweet_points):
    '''
    This function combines the rasterized
    tweet locations with CartoDark tiles.
    '''

    # Get the CartoDark tiles
    carto_tiles = hv.element.tiles.CartoDark()

    # Combine the tweet locations with CartoDark tiles
    tweet_map = carto_tiles * tweet_points
    return tweet_map
