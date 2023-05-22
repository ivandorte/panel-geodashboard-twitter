import holoviews as hv
from bokeh.models import HoverTool
from holoviews.operation.datashader import dynspread, rasterize
from scipy import spatial


def get_tweet_points(in_data):
    """
    Returns a rasterized graph of tweet locations.
    """

    # Define a custom Hover tool for the points
    points_hover = HoverTool(
        tooltips=[("tweets", "@image")],
    )

    # Plot the tweet locations, apply rasterization and dynspread
    out_points = dynspread(rasterize(hv.Points(in_data, ["x", "y"]))).opts(
        frame_width=600,
        frame_height=400,
        cmap="viridis",
        cnorm="eq_hist",
        xaxis=None,
        yaxis=None,
        tools=[points_hover],
    )
    return out_points


def get_data_boundary(in_data):
    """This function draws a convex hull for a set of points"""

    # Get xy coordinates as numpy array
    xy = in_data[["x", "y"]].to_numpy()

    # Get the ConvexHull from the points
    xy_convhull = spatial.ConvexHull(xy)

    # Get ConvexHull vertices
    vertices = [xy[vert_idx] for vert_idx in xy_convhull.vertices]

    # Close the curve
    vertices.append(vertices[0])

    # Draw the ConvexHull
    map_boundary = hv.Curve(vertices).opts(color="white", alpha=0.5)

    return map_boundary


def get_tweet_map(tweet_points, data_boundary):
    """
    This function combines the rasterized
    tweet locations with CartoDark tiles.
    """

    # Get the CartoDark tiles
    carto_tiles = hv.element.tiles.CartoDark()

    # Combine the tweet locations with CartoDark tiles
    tweet_map = carto_tiles * data_boundary * tweet_points
    return tweet_map
