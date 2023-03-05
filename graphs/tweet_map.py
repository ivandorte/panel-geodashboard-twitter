import holoviews as hv
import hvplot.pandas
from bokeh.models import CustomJSHover, HoverTool
from scipy import spatial


def get_tweet_points(in_data):
    """
    Returns a rasterized graph of tweet locations.
    """

    # This function hide the tooltip when the bin value is NaN
    hide_nan = CustomJSHover(
        code="""
        var value;
        var tooltips = document.getElementsByClassName("bk-tooltip");
        if (isNaN(value)) {
            tooltips[0].hidden=true;
        } else {
            tooltips[0].hidden=false;
        }
            return value;
        """
    )

    # Define a custom Hover tool for the points
    points_hover = HoverTool(
        tooltips=[("tweets", "@image{custom}")],
        formatters={"@image": hide_nan},
    )

    # Plot the tweet locations, apply rasterization and dynspread
    out_points = in_data.hvplot.points(
        x="x",
        y="y",
        rasterize=True,
        dynspread=True,
        cmap="viridis",
        cnorm="eq_hist",
        colorbar=False,
        tools=[points_hover],
        frame_width=600,
        frame_height=400,
    )

    # Additional plot options
    out_points.opts(xaxis=None, yaxis=None, active_tools=["wheel_zoom"])
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
