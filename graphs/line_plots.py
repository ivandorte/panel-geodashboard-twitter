import hvplot.pandas  # noqa
import numpy as np
from bokeh.models import HoverTool, WheelZoomTool
from graphs.no_data_utils import EMPTY_LINE_PLOT_DTWS, EMPTY_LINE_PLOT_DUU
from pd_utils.utils import filter_df_by_bbox

LINE_COLOR = "#03DAC6"


def get_daily_tweets(in_data, x_range, y_range):
    """
    Returns a line plot showing the number of tweets
    per day within the current map extent.
    """

    def hook(plot, element):
        """
        Custom hook for disabling zoom on axis
        """

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        return EMPTY_LINE_PLOT_DTWS

    # Define a custom Hover tool
    tweets_hover = HoverTool(
        tooltips=[("Day", "@tweet_date{%F}"), ("Tweets", "@tweet_id")],
        formatters={"@tweet_date": "datetime"},
        point_policy="follow_mouse",
    )

    # Get the number of tweets on daily basis
    tweets_df = out_data.resample("D")["tweet_id"].count()
    tweets_df = tweets_df.replace(0, np.nan)
    tweets_df = tweets_df.reset_index()

    # Number of tweets
    total_tweets = tweets_df["tweet_id"].sum()

    # Create the line plot
    tweets_plt = tweets_df.hvplot.line(
        title=f"Total: {int(total_tweets)}",
        x="tweet_date",
        y="tweet_id",
        xlabel="Time [Days]",
        ylabel="Tweets",
        yformatter="%.0f",
        color=LINE_COLOR,
        alpha=0.7,
        tools=[tweets_hover],
        min_height=300,
        min_width=300,
        responsive=True,
    )

    # Additional plot options
    tweets_plt.opts(
        hooks=[hook],
    )

    return tweets_plt


def get_daily_unique_users(in_data, x_range, y_range):
    """
    Returns a line plot showing the number of
    Unique users per day within the current
    map extent.
    """

    def hook(plot, element):
        """
        Custom hook for disabling zoom on axis
        """

        # Disable zoom on axis
        for tool in plot.state.toolbar.tools:
            if isinstance(tool, WheelZoomTool):
                tool.zoom_on_axis = False
                break

    # Filter the tweet locations by bounding box
    out_data = filter_df_by_bbox(in_data, x_range, y_range)

    # Check if out_data is empty
    if out_data.shape[0] == 0:
        return EMPTY_LINE_PLOT_DUU

    # Define a custom Hover tool
    uu_hover = HoverTool(
        tooltips=[("Day", "@tweet_date{%F}"), ("UU", "@user_id")],
        formatters={"@tweet_date": "datetime"},
        point_policy="follow_mouse",
    )

    # Get the number of unique users on daily basis
    uu_df = out_data.drop_duplicates(["user_id"])
    uu_df = uu_df.resample("D")["user_id"].count()
    uu_df = uu_df.replace(0, np.nan)
    uu_df = uu_df.reset_index()

    # Number of unique users
    unique_users = uu_df["user_id"].sum()

    # Create the line plot
    uu_plt = uu_df.hvplot.line(
        title=f"Total: {int(unique_users)}",
        x="tweet_date",
        y="user_id",
        xlabel="Time [Days]",
        ylabel="Unique Users [UU]",
        yformatter="%.0f",
        color=LINE_COLOR,
        alpha=0.7,
        tools=[uu_hover],
        min_height=300,
        min_width=300,
        responsive=True,
    )

    # Additional plot options
    uu_plt.opts(hooks=[hook])

    return uu_plt
